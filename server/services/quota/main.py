#!/usr/local/bin/python3
# coding: utf-8

"""
oracle_to_flask_service.py
==================================
Read‑only Flask micro‑service exposing one GET endpoint for every table that
appears in the original Oracle query (cruise, station, sample, measure, species,
sexual_maturity, otolith, harbour, vessel, gear).

* No DDL — assumes tables already exist in Oracle.
* Connection parameters come from env‑vars (see below).
* Each endpoint returns a thin JSON object with the columns defined here.
* SQLAlchemy 2.x, typing friendly, future‑style sessions.

Required environment variables
------------------------------
DB_RDBES_USR   Oracle user name
DB_RDBES_PWD   Oracle password
DB_RDBES_DSN   DSN, e.g. ``HOST:PORT/SERVICE`` or EZConnect
FLASK_HOST     Optional (default ``0.0.0.0``)
FLASK_PORT     Optional (default ``8000``)
FLASK_DEBUG    ``1`` to enable Flask debug mode

Quick start
-----------
::

    export DB_RDBES_USR=myuser
    export DB_RDBES_PWD=mypass
    export DB_RDBES_DSN=dbhost:1521/XEPDB1
    python oracle_to_flask_service.py

Dependencies
------------
``pip install flask sqlalchemy oracledb python-dotenv``
"""
from __future__ import annotations

import os
from datetime import datetime, time, date
from flask import Flask, abort, jsonify, request
from sqlalchemy import select, and_, or_

from server.common.session import get_session_local
from server.common.helper import to_dict
from server.services.quota.null import null_quota
from server.services.quota.models import Quota

# ---------------------------------------------------------------------------
# Create Session
# ---------------------------------------------------------------------------
SessionLocal = get_session_local()



def fetch_one(model, filters: dict):
    conditions = []

    for key, value in filters.items():
        if key == "between":
            col_start, col_end, target = value

            # Adjust target to start and end of the day
            if isinstance(col_start, date) and isinstance(col_end, date):
                start_of_day = datetime.combine(col_start, time.min)
                end_of_day = datetime.combine(col_end, time.max)
            else:
                raise ValueError("Target for 'between' must be a datetime object")

            conditions.append(and_(start_of_day <= target, end_of_day >= target))
        else:
            conditions.append(key == value)

    stmt = select(model).where(and_(*conditions))

    with SessionLocal() as session:
        rec = session.scalars(stmt).first()
        return to_dict(rec) if rec else None


def fetch_many_dict(model, filters: dict):
    conditions = []

    for key, value in filters.items():
        if key == "between":
            col, start_d, end_d = value  # value is (column, start_date, end_date)
            start = datetime.combine(start_d, time.min)
            end   = datetime.combine(end_d, time.max)
            conditions.append(col.between(start, end))

        elif key == "any_between":
            # value is list of (column, start_date, end_date)
            ors = []
            for col, start_d, end_d in value:
                start = datetime.combine(start_d, time.min)
                end   = datetime.combine(end_d, time.max)
                ors.append(col.between(start, end))
            conditions.append(or_(*ors))

        else:
            # assume key is a ColumnElement, e.g. model.ftegund
            conditions.append(key == value)

    stmt = select(model).where(and_(*conditions))
    with SessionLocal() as session:
        return [to_dict(r) for r in session.scalars(stmt).all()]


# --- TargetAssemblage --------------------------------------------------------------
def get_quota(filter: dict):
    data = fetch_many_dict(Quota, filter)

    if data is []:
        return [null_quota]

    for rec in data:
        rec['i_gildi'] = rec['i_gildi'].strftime('%Y-%m-%d %H:%M')
        rec['ur_gildi'] = rec['ur_gildi'].strftime('%Y-%m-%d %H:%M')

    return data


# ---------------------------------------------------------------------------
# Flask app & routing
# ---------------------------------------------------------------------------

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

# --- Health --------------------------------------------------------------
@app.get("/health")
def health():
    """Liveness/readiness probe."""
    current_timestamp = datetime.now().isoformat()
    response = {
        "Landing-service Status": "200 OK",
        "timestamp": current_timestamp
    }
    return jsonify(response), 200


# --- Target assemblage ------
# --------------------------------------------------------
# TODO fleiri parametrar


@app.get("/quota")
def quota_endpoint():
    species_no = request.args.get("species", type=int)
    year = request.args.get("year", type=int)

    if not species_no or not year:
        abort(400, "Missing species and/or year")

    filter = {
        Quota.ftegund: species_no,
        "any_between": [
            (Quota.i_gildi, date(year,1,1), date(year,12,31)),
            (Quota.ur_gildi, date(year, 1, 1), date(year, 12, 31))
        ]
    }

    data = get_quota(filter)
    return jsonify(data) if data else abort(404, "No Landings found")


# ---------------------------------------------------------------------------

if __name__ == "__main__":

    host = "0.0.0.0"
    port = int(os.getenv("PORT", 5047))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug)
