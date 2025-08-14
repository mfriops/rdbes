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
from datetime import datetime
from flask import Flask, abort, jsonify, request

from server.common.session import get_session_local
from server.common.fetch import fetch_many
from server.common.helper import parse_int_list
from server.services.vessel.models import Vessel

# ---------------------------------------------------------------------------
# Create Session
# ---------------------------------------------------------------------------
SessionLocal = get_session_local()

# ---------------------------------------------------------------------------
# Declarative models (minimal column subsets)
# ---------------------------------------------------------------------------


# --- vessel --------------------------------------------------------------
# def get_vessel(registration_no: int):
#     return fetch_one(vessel, vessel.registration_no, registration_no)

def get_vessel(registration_nos: list[int] | int):
    return fetch_many(SessionLocal, Vessel, Vessel.registration_no, registration_nos)

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
        "vessel-service Status": "200 OK",
        "timestamp": current_timestamp
    }
    return jsonify(response), 200


# --- vessel --------------------------------------------------------------
@app.get("/vessel")
def vessel_endpoint():
    registration_nos = parse_int_list(request.args.get("registration_no"), param_name="registration_no")
    data = get_vessel(registration_nos)
    return jsonify(data) if data else abort(404, "No Vessels found")


# ---------------------------------------------------------------------------

if __name__ == "__main__":

    host = "0.0.0.0"
    port = int(os.getenv("PORT", 5044))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug)
