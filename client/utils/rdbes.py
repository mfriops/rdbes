#!/usr/local/bin/python3
# coding: utf-8

from __future__ import annotations

import re
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry
from shapely.wkt import loads as wkt_loads
from typing import Iterable, Protocol, runtime_checkable


def rdbes_existence():
    return True


def vessel_length_category(p_length: float | int | None) -> str:
    """
    Classify a vessel’s overall length into the RDBES code buckets.

    Parameters
    ----------
    p_length : float | int | None
        Length in metres. Pass None to get the 'NK' (not known) code.

    Returns
    -------
    str
        One of the codes:
        ─ VL0006  – 0 ≤ L < 6 m
        ─ VL0612  – 6 ≤ L < 12 m
        ─ VL1218  – 12 ≤ L < 18 m
        ─ VL1824  – 18 ≤ L < 24 m
        ─ VL2440  – 24 ≤ L < 40 m
        ─ VL40XX  – 40 m ≤ L
        ─ NK      – length unknown or invalid
    """
    # Handle None or non-numeric values up front
    if p_length is None:
        return "NK"

    try:
        # Ensure we can compare as a number
        length = float(p_length)
    except (TypeError, ValueError):
        return "NK"

    if length < 6:
        return "VL0006"
    elif length < 12:
        return "VL0612"
    elif length < 18:
        return "VL1218"
    elif length < 24:
        return "VL1824"
    elif length < 40:
        return "VL2440"
    elif length >= 40:
        return "VL40XX"
    else:  # This branch is practically unreachable, but mirrors the PL/SQL structure
        return "NK"



@runtime_checkable
class HasGeometry(Protocol):
    """Duck-type for whatever row/record object you fetch."""

    code: str
    location: str | BaseGeometry  # WKT string or a Shapely geometry
    valid: int


def d2area(
    lat: float | int | None,
    lon: float | int | None,
    fishing_area: str = "27%",
    rows: Iterable[HasGeometry] | None = None,
) -> str:
    """
    Classify a point (lat, lon) into an FAO Major Fishing Area.

    Parameters
    ----------
    lat, lon
        The geographic coordinates in WGS-84 (EPSG:4326).
        If either is ``None`` the function returns **'NULL VALUE'**.
    fishing_area
        SQL-style LIKE pattern that limits the search
        (default ``'27%'`` ⇢ North-East Atlantic).
    rows
        An iterable containing records with ``code``, ``location`` and ``valid``.
        If you pass ``None``, you must plug in your own query function
        (see the *Database helper* below).

    Returns
    -------
    str
        * a single matching **code**
        * **'NOT FOUND'**  – no polygon contains the point
        * **'TOO MANY'**   – more than one polygon matches
        * **'NULL VALUE'** – bad or missing coordinates
    """
    # 1.  Bail early if we have no usable coordinates
    if lat is None or lon is None:
        return "NULL VALUE"

    # 2.  Translate SQL LIKE → regex once
    #     "27%"   → r"^27.*$"
    #     "3_1%"  → r"^3.1.*$"
    like_regex = (
        "^"
        + re.escape(fishing_area)
        .replace(r"\%", ".*")  # % → .*
        .replace(r"\_", ".")  # _ → .
        + "$"
    )
    code_filter = re.compile(like_regex)

    # 3.  Fetch candidate polygons if the caller didn’t supply them -------------
    if rows is None:
        rows = fetch_area_rows(fishing_area)  # <── Implement for your DB

    # 4.  Build the point once
    point = Point(float(lon), float(lat))

    # 5.  Find matches
    matches: list[str] = []
    for row in rows:
        if row.valid != 1 or not code_filter.match(row.code):
            continue

        geom: BaseGeometry
        if isinstance(row.location, BaseGeometry):
            geom = row.location
        else:  # assume WKT text
            geom = wkt_loads(row.location)

        if geom.contains(point):
            matches.append(row.code)

    # 6.  Mirror the original PL/SQL branches
    if not matches:
        return "NOT FOUND"
    if len(matches) > 1:
        return "TOO MANY"
    return matches[0]






@runtime_checkable
class HasMetierRow(Protocol):
    """Shape of the rows coming from rdbes.metier."""
    area_code: str
    gear_type: str
    target_assemblage: str
    mesh_size_from: float | int | None
    mesh_size_to: float | int | None
    metier: str
    valid: int


def metier6(
    area_code: str,
    gear_type: str,
    target_assemblage: str,
    mesh_size: float | int | None,
    rows: Iterable[HasMetierRow] | None = None,
) -> str:
    """
    Resolve (area, gear, assemblage, mesh) ➜ *METIER6* code.

    Mirrors the logic of the PL/SQL `rdbes.metier6` function:

    ─ If *mesh_size* **is not None**:
      • Match rows whose (mesh_size_from ≤ mesh < mesh_size_to).
      • Treat NULL ⇢ 0 for the *from* bound and NULL ⇢ 999 for the *to* bound.
      • Require at least one of the bounds to be not-null.
    ─ If *mesh_size* **is None**:
      • Match only rows where both bounds are NULL.

    Returns
    -------
    str
        • the single `metier` code if exactly one row matches
        • `'NOT FOUND'`  – no matching row
        • `'TOO MANY'`   – > 1 matching row
    """
    # ------------------------------------------------------------------
    # 1.  Fetch the candidate rows if the caller didn’t supply them
    # ------------------------------------------------------------------
    if rows is None:
        rows = fetch_metier_rows(area_code, gear_type, target_assemblage)

    # ------------------------------------------------------------------
    # 2.  Apply the filter in pure Python
    # ------------------------------------------------------------------
    matches: list[str] = []

    for r in rows:
        if r.valid != 1:
            continue
        if (
            r.area_code != area_code
            or r.gear_type != gear_type
            or r.target_assemblage != target_assemblage
        ):
            continue

        if mesh_size is not None:
            lo = 0 if r.mesh_size_from is None else float(r.mesh_size_from)
            hi = 999 if r.mesh_size_to is None else float(r.mesh_size_to)
            # Must have at least ONE bound defined, like the PL/SQL clause
            if r.mesh_size_from is None and r.mesh_size_to is None:
                continue
            if lo <= mesh_size < hi:
                matches.append(r.metier)
        else:  # mesh_size is None  →  only rows with both bounds NULL
            if r.mesh_size_from is None and r.mesh_size_to is None:
                matches.append(r.metier)

    # ------------------------------------------------------------------
    # 3.  Reproduce PL/SQL exception branches
    # ------------------------------------------------------------------
    if not matches:
        return "NOT FOUND"
    if len(matches) > 1:
        return "TOO MANY"
    return matches[0]


# ---------------------------------------------------------------------------
# Optional: a tiny helper to pull the data from your spatial table
# ---------------------------------------------------------------------------
# import psycopg2  # or sqlalchemy… adjust to your stack

#
# def fetch_area_rows(fishing_area: str) -> Iterable[Tuple[str, str, int]]:
#     """
#     Yields (code, location_wkt, valid) from table rdbes.area
#     whose code LIKE *fishing_area*.
#     """
#     conn = psycopg2.connect("dbname=… user=… password=… host=…")
#     with conn, conn.cursor() as cur:
#         cur.execute(
#             """
#             SELECT code, ST_AsText(location) AS wkt, valid
#             FROM rdbes.area
#             WHERE location IS NOT NULL
#               AND valid = 1
#               AND code LIKE %s
#             """,
#             (fishing_area,),
#         )
#         yield from cur.fetchall()
#
#
#
# # ----------------------------------------------------------------------
# # Optional helper: pull rows from your DB  (adjust to your own stack)
# # ----------------------------------------------------------------------
# # import psycopg2  # cx_Oracle / sqlalchemy equally fine
#
#
# def fetch_metier_rows(
#     area_code: str,
#     gear_type: str,
#     target_assemblage: str,
# ) -> Iterable[tuple]:
#     """
#     Yields rows with the six columns the function needs.
#
#     The WHERE clause already fixes *area_code* / *gear_type* /
#     *target_assemblage* so the in-Python loop only deals with mesh-size logic.
#     """
#     sql = """
#         SELECT
#             area_code,
#             gear_type,
#             target_assemblage,
#             mesh_size_from,
#             mesh_size_to,
#             metier,
#             valid
#         FROM rdbes.metier
#         WHERE area_code = %s
#           AND gear_type = %s
#           AND target_assemblage = %s
#           AND valid = 1
#     """
#     conn = psycopg2.connect("dbname=… user=… password=… host=…")
#     with conn, conn.cursor() as cur:
#         cur.execute(sql, (area_code, gear_type, target_assemblage))
#         yield from cur.fetchall()
