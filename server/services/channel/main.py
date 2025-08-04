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
import oracledb  # Oracle driver for SQLAlchemy "oracledb" dialect

from typing import Any, Dict
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request

from server.common.session import get_session_local
from server.common.fetch import fetch_one, fetch_many
from server.common.helper import to_dict, parse_int_list

from models import Cruise, Station, Sample, Measure, Otolith, Species, SexualMaturity

# ---------------------------------------------------------------------------
# Create Session
# ---------------------------------------------------------------------------
SessionLocal = get_session_local()



# --- Cruise --------------------------------------------------------------
def get_cruise(code: str):
    data = fetch_one(SessionLocal, Cruise, Cruise.cruise, code)
    data['departure'] = data['departure'].strftime("%Y-%m-%d")
    data['arrival'] = data['arrival'].strftime("%Y-%m-%d")
    return data


# --- Station --------------------------------------------------------------
def get_station(cruise_id: int):
    data = fetch_many(SessionLocal, Station, Station.cruise_id, cruise_id)
    for rec in data:
        rec['station_date'] = rec['station_date'].strftime("%Y-%m-%d")

    return data


# --- Sample --------------------------------------------------------------
def get_sample(station_ids: list[int] | int):
    data = fetch_many(SessionLocal, Sample, Sample.station_id, station_ids)
    for rec in data:
        rec['tow_start'] = rec['tow_start'].strftime("%Y-%m-%d %H:%M") if rec['tow_start'] != None else rec['tow_start']
        rec['tow_end'] = rec['tow_end'].strftime("%Y-%m-%d %H:%M") if rec['tow_end'] != None else rec['tow_end']

    return data


# --- Measure --------------------------------------------------------------
def get_measure(sample_ids: list[int] | int):
    return fetch_many(SessionLocal, Measure, Measure.sample_id, sample_ids)


# --- Otolith --------------------------------------------------------------
def get_otolith(measure_ids: list[int] | int):
    return fetch_many(SessionLocal, Otolith, Otolith.measure_id, measure_ids)


# --- Species --------------------------------------------------------------
def get_species(species_no: list[int] | int):
    return fetch_many(SessionLocal, Species, Species.species_no, species_no)


# --- Sexual maturity --------------------------------------------------------------
def get_sexual_maturity(sexual_maturity_id: int):
    return fetch_one(SessionLocal, SexualMaturity, SexualMaturity.sexual_maturity_id, sexual_maturity_id)


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
        "channel-service Status": "200 OK",
        "timestamp": current_timestamp
    }
    return jsonify(response), 200


# --- Cruise --------------------------------------------------------------
@app.get("/cruise/<string:cruise_code>")
def cruise_endpoint(cruise_code: str):
    data = get_cruise(cruise_code)
    return jsonify(data) if data else abort(404, "Cruise not found")


# --- Station -------------------------------------------------------------
@app.get("/station/<int:cruise_id>")
def station_endpoint(cruise_id: int):
    data = get_station(cruise_id)
    return jsonify(data) if data else abort(404, "No Stations found")


# --- Sample --------------------------------------------------------------
@app.get("/sample")
def sample_endpoint():
    station_ids = parse_int_list(request.args.get("station_id"), param_name="station_id")
    data = get_sample(station_ids)
    return jsonify(data) if data else abort(404, "No Samples found")


# --- Measure -------------------------------------------------------------
@app.get("/measure")
def measure_endpoint():
    sample_ids = parse_int_list(request.args.get("sample_id"), param_name="sample_id")
    data = get_measure(sample_ids)
    return jsonify(data) if data else abort(404, "No Measures found")


# --- Otolith -------------------------------------------------------------
@app.get("/otolith")
def otolith_endpoint():
    measure_ids = parse_int_list(request.args.get("measure_id"), param_name="measure_id")
    data = get_otolith(measure_ids)

    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "No Otoliths found"}), 200


# --- Species -------------------------------------------------------------
@app.get("/species")
def species_endpoint():
    species_nos = parse_int_list(request.args.get("species_no"), param_name="species_no")
    data = get_species(species_nos)
    return jsonify(data) if data else abort(404, "No Species found")


# --- Sexual maturity -----------------------------------------------------
@app.get("/sexual_maturity/<int:sexual_maturity_id>")
def sexual_maturity_endpoint(sexual_maturity_id: int):
    data = get_sexual_maturity(sexual_maturity_id)
    return jsonify(data) if data else abort(404, "Sexual maturity not found")

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5041)))
