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
from server.common.fetch import fetch_one, fetch_many
from server.common.helper import to_dict, parse_int_list

from models import FishingGear, Isscfg

# ---------------------------------------------------------------------------
# Create Session
# ---------------------------------------------------------------------------
SessionLocal = get_session_local()


# --- Fishing gear ----------------------------------------------------------------
def get_fishing_gear(fishing_gear_no: list[str] | str):
    return fetch_many(SessionLocal, FishingGear, FishingGear.fishing_gear_no, fishing_gear_no)


# --- Isscfg ----------------------------------------------------------------
def get_isscfg(isscfg_no: list[str] | str):
    return fetch_many(SessionLocal, Isscfg, Isscfg.isscfg_no, isscfg_no)

# ---------------------------------------------------------------------------
# Flask app & routing
# ---------------------------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------------------------
# Many entry point
# ---------------------------------------------------------------------------

# --- Health ----------------------------------------------------------------
@app.get("/health")
def health():
    """Liveness/readiness probe."""
    current_timestamp = datetime.now().isoformat()
    response = {
        "gear-service Status": "200 OK",
        "timestamp": current_timestamp
    }
    return jsonify(response), 200


# --- Fishing gear ----------------------------------------------------------------
@app.get("/fishing_gear")
def fishing_gear_endpoint():
    fishing_gear_nos = parse_int_list(request.args.get("fishing_gear_no"), param_name="fishing_gear_no")
    data = get_fishing_gear(fishing_gear_nos)
    return jsonify(data) if data else abort(404, "Fishing gear not found")


# --- Isscfg ----------------------------------------------------------------
@app.get("/isscfg")
def isscfg_endpoint():
    isscfg_nos = parse_int_list(request.args.get("isscfg_no"), param_name="isscfg_no")
    data = get_isscfg(isscfg_nos)
    return jsonify(data) if data else abort(404, "Isscfg not found")



# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5043)))
