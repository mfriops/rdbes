#!/usr/local/bin/python3
# coding: utf-8

"""
RDBES Flask micro-service – Oracle edition (schema-aware)

• One **POST** endpoint per RDBES table         →  JSON payload ↦ INSERT
• Three **GET** endpoints (harbour / area / metier) →  list reference data
• Identifiers are **case-insensitive** on inserts – any JSON key casing
  is mapped to the proper Oracle column name.

──────────────────────────────────────────────────────────────────────────────
Quick start
──────────
1. Required env-vars::

       export DB_RDBES_USR=rdbes
       export DB_RDBES_PWD=…      # never commit!
       export DB_RDBES_DSN="dbhost:1521/ORCLPDB1"
       # Optional – only if you connect with another user:
       export DB_RDBES_SCHEMA=RDBES

2. Install deps and run::

       pip install flask sqlalchemy oracledb
       python app.py

3. Insert a row::

       curl -X POST http://localhost:5042/design \
            -H "Content-Type: application/json" \
            -d '{"label":"Q123", "DErecordType":"DE", … }'

4. List reference data::

       curl http://localhost:5042/harbour
       curl http://localhost:5042/area
       curl http://localhost:5042/metier
──────────────────────────────────────────────────────────────────────────────
"""
from __future__ import annotations

import os
import oracledb                      # Oracle Python driver
from typing import Any, Dict, List
from datetime import datetime
from flask import Flask, abort, jsonify, request
from sqlalchemy import (
    MetaData,
    Table,
    create_engine,
    text,
    select,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session

from server.common.helper import to_dict, _payload_to_values, parse_int_list
from server.common.geo import get_fao_area
from server.common.fetch import fetch_many
from server.services.rdbes.models import Harbour

# ---------------------------------------------------------------------------
# Create Session
# ---------------------------------------------------------------------------

# ───────────────────────────── connection ──────────────────────────────
CONNECT_ARGS: Dict[str, Any] = {
    "user": os.getenv("DB_RDBES_USR"),
    "password": os.getenv("DB_RDBES_PWD"),
    "dsn": os.getenv("DB_RDBES_DSN"),
    "cclass": "RDBES_API",
    "purity": oracledb.ATTR_PURITY_SELF,
}

SCHEMA = (
    os.getenv("DB_RDBES_SCHEMA", CONNECT_ARGS["user"]).upper()
    if CONNECT_ARGS["user"]
    else None
)

_missing: List[str] = [k for k, v in CONNECT_ARGS.items() if not v]
if _missing:
    raise RuntimeError(f"Missing env vars: {', '.join(_missing)}")

engine = create_engine(
    "oracle+oracledb://",           # credentials via connect_args
    connect_args=CONNECT_ARGS,
    future=True,
    pool_pre_ping=True,
    echo=False,
)

# ───────────────────────────── metadata ────────────────────────────────
metadata = MetaData(schema=SCHEMA)
TABLES = [
    "design",
    "fishing_trip",
    "fishing_operation",
    "species_selection",
    "sample",
    "sampling_details",
    "vessel_details",
    "individual_species",
    "species_list",
    "frequency_measure",
    "biological_variable",
    "commercial_landing",
    "commercial_effort",
]
for t in TABLES:
    Table(t, metadata, autoload_with=engine, schema=SCHEMA)

# ───────────────────── ORM & read-only reference tables ────────────────
Session = scoped_session(
    sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
)

SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine, future=True, expire_on_commit=False)


# ---------------------------------------------------------------------------
# One‑table SELECT helpers
# ---------------------------------------------------------------------------

def fetch_one(model, column, value):
    """Generic helper to fetch a single record by column == value."""
    stmt = select(model).where(column == value)
    with SessionLocal() as session:
        rec = session.scalars(stmt).first()
        return to_dict(rec) if rec else None


# def fetch_many(
#     model,
#     column=None,
#     values=None,
#     *,
#     where_clauses=None,
#     limit=None,
#     offset=None,
#     order_by=None,
# ):
#     """
#     Generic helper to fetch one or many records.
#
#     Parameters
#     ----------
#     model : sqlalchemy.orm.DeclarativeMeta
#         The mapped class you want to query.
#     column : InstrumentedAttribute | None
#         A model attribute to filter on (e.g. `User.id`, `User.email`).
#         Leave it None if you only want to apply `where_clauses`.
#     values : Any | Iterable[Any] | None
#         Value or iterable of values to match against `column`.
#     where_clauses : Iterable[sqlalchemy.sql.expression.ClauseElement] | None
#         Extra SQLAlchemy conditions you’d like to AND together.
#     limit : int | None
#     offset : int | None
#     order_by : sqlalchemy.sql.expression.ClauseElement | Sequence[...]
#         Order criteria (e.g. `User.created_at.desc()`).
#
#     Returns
#     -------
#     list[dict]
#         A list of `to_dict(record)` results (empty list if nothing matched).
#     """
#     stmt = select(model)
#
#     # Primary filter (column == value or column.in_(values))
#     if column is not None and values is not None:
#         if isinstance(values, (list, tuple, set)):
#             stmt = stmt.where(column.in_(values))
#         else:
#             stmt = stmt.where(column == values)
#
#     # Optional extra predicates
#     if where_clauses:
#         stmt = stmt.where(and_(*where_clauses))
#
#     # Optional sorting / paging
#     if order_by is not None:
#         stmt = stmt.order_by(order_by)
#     if limit is not None:
#         stmt = stmt.limit(limit)
#     if offset is not None:
#         stmt = stmt.offset(offset)
#
#     with SessionLocal() as session:
#         records = session.scalars(stmt).all()
#         return [to_dict(r) for r in records]



# --- Harbour ----------------------------------------------------------------
def get_harbour(port_nos: list[int] | int) -> str:
    return fetch_many(SessionLocal, Harbour, Harbour.port_no, port_nos)


# --- Area ----------------------------------------------------------------
def get_area(lat: float, lon: float) -> str:

    with SessionLocal() as session:
        try:
            query = text("""
                SELECT code FROM rdbes.area
                 WHERE SDO_CONTAINS(
                    location,
                    SDO_GEOMETRY(
                        2001, 4326,
                        SDO_POINT_TYPE(:lon, :lat, NULL),
                        NULL, NULL
                    )
                ) = 'TRUE'
                   AND valid = 1
            """)
            result = session.execute(query, {"lat": lat, "lon": lon}).fetchone()
            session.close()
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    if result and result[0]:
        return jsonify({"code": result[0]})
    else:
        return jsonify({"code": None, "message": "No matching area found"})



# --- Metier ----------------------------------------------------------------
def get_metier(area_code: str, gear_type: str, target_assemblage: str, mesh_size: int)-> str:

    with SessionLocal() as session:
        try:
            query = text("""
                SELECT metier FROM rdbes.metier
                 WHERE area_code  = :area_code
                   AND gear_type = :gear_type
                   AND target_assemblage = :target_assemblage
                   AND nvl(mesh_size_from,0) <= :mesh_size
                   AND nvl(mesh_size_to,10000) >= :mesh_size
                   AND valid = 1
            """)
            result = session.execute(query, {"area_code": area_code, "gear_type": gear_type, "target_assemblage": target_assemblage, "mesh_size": mesh_size}).fetchone()
            session.close()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if result and result[0]:
        return jsonify({"metier": result[0]})
    else:
        return jsonify({"metier": None})


# ───────────────────────────── app ─────────────────────────────────────
app = Flask(__name__)


@app.get("/health")
def health():
    """Liveness/readiness probe."""
    current_timestamp = datetime.now().isoformat()
    response = {
        "rdbes-service Status": "200 OK",
        "timestamp": current_timestamp
    }

    return jsonify(response), 200


@app.route('/DBhealth', methods = ['GET'])
def DBhealth_check():

    with SessionLocal() as session:
        try:
            query = text("""
                            SELECT ora_database_name "db_name", to_char(sysdate,'yyyy-mm-dd hh24:mi:ss') "timestamp" FROM dual
                         """)
            result = session.execute(query, None).fetchone()
            session.close()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if result and result[0]:
        return jsonify({"RDBES DB-status": '200 OK', "DB-name": result[0], "DB-timestamp": result[1]})
    else:
        return jsonify({"error": True, "message": result[1].get('error', 'Unknown error occurred'), "code": "RDBES.HEALTH_QUERY_FAILED"})


# -------- read-only reference endpoints ---------------------------------

# --- Harbour -------------------------------------------------------------
@app.get("/harbour")
def harbour_endpoint():
    port_nos = parse_int_list(request.args.get("port_no"), param_name="port_no")
    data = get_harbour(port_nos)
    return jsonify(data) if data else abort(404, "Harbour not found")


# --- Area -------------------------------------------------------------
@app.get("/area")
def area_endpoint():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "Missing 'lat' or 'lon' parameter"}), 400

    # code = get_area(lat, lon)
    code = { "code": get_fao_area(lat, lon) }
    return code if code else abort(404, "Area code not found")


# --- Metier -------------------------------------------------------------
@app.get("/metier")
def metier_endpoint()-> str:
    area_code = request.args.get("area_code", type=str)
    gear_type = request.args.get("gear_type", type=str)
    target_assemblage = request.args.get("target_assemblage", type=str)
    mesh_size = request.args.get("mesh_size", type=int)

    if None in [area_code, gear_type, target_assemblage, mesh_size]:
        return jsonify({
            "error": "Missing one or more required parameters: 'area_code', 'gear_type', 'target_assemblage', 'mesh_size'"
        }), 400

    metier = get_metier(area_code, gear_type, target_assemblage, mesh_size)
    return metier if metier else abort(404, "Metier not found")


# -------- insert-only dynamic endpoints ---------------------------------
for tbl_name in TABLES:
    table_obj: Table = metadata.tables[f"{SCHEMA}.{tbl_name}"]
    endpoint_name = f"insert_{tbl_name}"

    def _make_view(table: Table):  # capture via closure
        def view():  # type: ignore[return-value]
            try:
                payload = request.get_json(force=True, silent=False)
            except Exception as exc:  # bad JSON
                return jsonify(error="Invalid JSON", detail=str(exc)), 400

            if not isinstance(payload, dict):
                return jsonify(error="Payload must be a JSON object"), 400

            values = _payload_to_values(table, payload)
            if not values:
                return (
                    jsonify(
                        error="No valid columns found in payload",
                        allowed=[col.name for col in table.columns],
                    ),
                    400,
                )

            try:
                with engine.begin() as conn:  # implicit commit/rollback
                    stmt = table.insert().values(**values)
                    # if PK is single column we can RETURNING
                    if table.primary_key and len(table.primary_key.columns) == 1:
                        pk_col = next(iter(table.primary_key.columns))
                        stmt = stmt.returning(pk_col)
                        result = conn.execute(stmt)
                        pk_value = result.scalar()
                        return jsonify(message="inserted", id=pk_value), 201
                    else:
                        conn.execute(stmt)
                        return jsonify(message="inserted"), 201
            except SQLAlchemyError as db_err:
                return (
                    jsonify(error="database error", detail=str(db_err.orig)),
                    500,
                )

        view.__name__ = f"view_insert_{tbl_name}"  # unique fn name
        return view

    app.add_url_rule(
        f"/{tbl_name}",
        view_func=_make_view(table_obj),
        methods=["POST"],
        endpoint=endpoint_name,
    )

    # --- Select/GET endpoint per table (all rows or filtered by query params) ---
    def _make_select_view(table: Table):
        def view():
            try:
                filters = []
                for col in table.columns:
                    val = request.args.get(col.name)
                    if val is not None:
                        filters.append(col == val)

                stmt = select(table)
                if filters:
                    stmt = stmt.where(*filters)

                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    rows = [dict(row._mapping) for row in result]
                    return jsonify(rows), 200
            except SQLAlchemyError as db_err:
                return jsonify(error="database error", detail=str(db_err.orig)), 500

        view.__name__ = f"view_select_{tbl_name}"  # unique fn name
        return view

    app.add_url_rule(
        f"/{tbl_name}",
        view_func=_make_select_view(table_obj),
        methods=["GET"],
        endpoint=f"select_{tbl_name}",
    )


# ───────────────────────────── entry-point ─────────────────────────────
if __name__ == "__main__":

    host = "0.0.0.0"
    port = int(os.getenv("PORT", 5048))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug)
