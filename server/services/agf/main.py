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
from sqlalchemy import select, and_

from server.common.session import get_session_local
from server.common.helper import to_dict
from server.services.agf.null import null_landings
from server.services.agf.models import Landings

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
    """
    Generic helper to fetch multiple records where all column==value in filters.

    :param model: SQLAlchemy model class
    :param filters: dict of {column: value}, where column is model.<column_name>
    :return: list of dicts representing the records, or empty list
    """
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
        recs = session.scalars(stmt).all()
        return [to_dict(rec) for rec in recs]


# --- TargetAssemblage --------------------------------------------------------------
def get_landings(filter: dict):
    data = fetch_many_dict(Landings, filter)

    if data is []:
        return [null_landings]

    for rec in data:
        rec['londun_hefst'] = rec['londun_hefst'].strftime('%Y-%m-%d %H:%M')

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


@app.get("/landings")
def landings_endpoint():
    date_from = request.args.get("date_from", type=str)
    date_to = request.args.get("date_to", type=str)
    if not date_from or not date_to:
        abort(400, "Missing date from and to")

    filter = {
        "between": (datetime.strptime(date_from,'%Y-%m-%d').date(), datetime.strptime(date_to,'%Y-%m-%d').date(), Landings.londun_hefst)
    }
    data = get_landings(filter)
    return jsonify(data) if data else abort(404, "No Landings found")


# ---------------------------------------------------------------------------

if __name__ == "__main__":

    host = "0.0.0.0"
    port = int(os.getenv("PORT", 5045))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug)
