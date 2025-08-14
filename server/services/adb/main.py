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
from server.common.helper import to_dict, parse_int_list, parse_str_list
from server.common.fetch import fetch_many
from server.services.adb.null import null_fishing_trip, null_fishing_station, null_trawl_and_seine_net
from server.services.adb.models import FishingTrip, FishingStation, TrawlAndSeineNet, TargetAssemblage

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
            if isinstance(target, date):
                start_of_day = datetime.combine(target, time.min)
                end_of_day = datetime.combine(target, time.max)
            else:
                raise ValueError("Target for 'between' must be a datetime object")

            conditions.append(and_(col_start <= end_of_day, col_end >= start_of_day))
        else:
            conditions.append(key == value)

    stmt = select(model).where(and_(*conditions))

    with SessionLocal() as session:
        rec = session.scalars(stmt).first()
        return to_dict(rec) if rec else None


def fetch_many_between(model, filters: dict):
    conditions = []

    for key, value in filters.items():
        if key == "between":
            col_start, col_end, target = value

            # Adjust target to start and end of the day
            if isinstance(col_start, date) and isinstance(col_end, date):
                conditions.append(and_(col_start <= target, col_end >= target))
            else:
                raise ValueError("Target for 'between' must be a datetime object")

        else:
            conditions.append(key == value)

    stmt = select(model).where(and_(*conditions))

    with SessionLocal() as session:
        recs = session.scalars(stmt).all()
        return [to_dict(rec) for rec in recs]


def fetch_many_dict(model, filters: dict):
    """
    Generic helper to fetch multiple records where all column==value in filters.

    :param model: SQLAlchemy model class
    :param filters: dict of {column: value}, where column is model.<column_name>
    :return: list of dicts representing the records, or empty list
    """
    conditions = [column == value for column, value in filters.items()]
    stmt = select(model).where(and_(*conditions))

    with SessionLocal() as session:
        recs = session.scalars(stmt).all()
        return [to_dict(rec) for rec in recs]


# --- TargetAssemblage --------------------------------------------------------------
def get_fishing_trip(filter: dict):
    data = fetch_one(FishingTrip, filter)

    if data is None:
        return null_fishing_trip

    data['departure'] = data['departure'].strftime('%Y-%m-%d %H:%M')
    data['landing'] = data['landing'].strftime('%Y-%m-%d %H:%M')
    return data

def get_fishing_trips(filter: dict):
    data = fetch_many_between(FishingTrip, filter)

    if data is []:
        return null_fishing_trip

    for d in data:
        d['departure'] = d['departure'].strftime('%Y-%m-%d %H:%M')
        d['landing'] = d['landing'].strftime('%Y-%m-%d %H:%M')
    return data


def get_fishing_station(fishing_trip_ids: list[str] | str):
    data = fetch_many(SessionLocal, FishingStation, FishingStation.fishing_trip_id, fishing_trip_ids)
    if data == []:
        return null_fishing_station

    for rec in data:
        rec['fishing_start'] = rec['fishing_start'].strftime('%Y-%m-%d %H:%M') if rec['fishing_start'] != None else rec['fishing_start']
        rec['fishing_end'] = rec['fishing_end'].strftime('%Y-%m-%d %H:%M') if rec['fishing_end'] != None else rec['fishing_end']
    return data

def get_trawl_and_seine_net(fishing_station_ids: list[int] | int):
    data = fetch_many(SessionLocal, TrawlAndSeineNet, TrawlAndSeineNet.fishing_station_id, fishing_station_ids)
    if data == []:
        return null_trawl_and_seine_net

    return data


def get_target_assemblage(filter: dict):
    data = fetch_many_dict(TargetAssemblage, filter)
    for rec in data:
        rec['departure_date'] = rec['departure_date'].strftime('%Y-%m-%d')
        rec['landing_date'] = rec['landing_date'].strftime('%Y-%m-%d')

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
        "ADB-service Status": "200 OK",
        "timestamp": current_timestamp
    }
    return jsonify(response), 200


# --- Target assemblage ------
# --------------------------------------------------------
# TODO fleiri parametrar


@app.get("/fishing_trip")
def fishing_trip_endpoint():
    registration_no = request.args.get("registration_no", type=int)
    fishing_date = request.args.get("fishing_date", type=str)
    landing_from = request.args.get("landing_from", type=str)
    landing_to = request.args.get("landing_to", type=str)

    if registration_no != None and fishing_date != None:
        filter = {
            FishingTrip.vessel_no: registration_no,
            "between": (FishingTrip.departure, FishingTrip.landing, datetime.strptime(fishing_date,'%Y-%m-%d').date())
        }

        data = get_fishing_trip(filter)
        return jsonify(data) if data else abort(404, "No Fishing Trip found")

    elif landing_from != None and landing_to != None:
        filter = {
            "between": (datetime.strptime(landing_from,'%Y-%m-%d').date(), datetime.strptime(landing_to,'%Y-%m-%d').date(), FishingTrip.landing)
        }

        data = get_fishing_trips(filter)
        return jsonify(data) if data else abort(404, "No Fishing Trip found")

    else:
        abort(400, "Missing or wrong parameters!")

    data = get_fishing_trip(filter)
    return jsonify(data) if data else abort(404, "No Fishing Trip found")


@app.get("/fishing_station")
def fishing_station_endpoint():
    fishing_trip_ids = parse_str_list(request.args.get("fishing_trip_id"), param_name="fishing_trip_id")
    data = get_fishing_station(fishing_trip_ids)
    return jsonify(data) if data else abort(404, "No Fishing Stations found")

@app.get("/trawl_and_seine_net")
def trawl_and_seine_net_endpoint():
    fishing_station_ids = parse_int_list(request.args.get("fishing_station_id"), param_name="fishing_station_id")
    data = get_trawl_and_seine_net(fishing_station_ids)
    return jsonify(data) if data else abort(404, "No Trawl or Seine Net found")


@app.get("/target_assemblage")
def target_assemblage_endpoint():
    species_no = request.args.get("species_no", type=int)
    year = request.args.get("year", type=int)
    if not species_no or not year:
        abort(400, "Missing species_no or year")

    filter = {
        TargetAssemblage.species_no: species_no,
        TargetAssemblage.landing_year: year
    }
    data = get_target_assemblage(filter)
    return jsonify(data) if data else abort(404, "No Species found")

# ---------------------------------------------------------------------------

if __name__ == "__main__":

    host = "0.0.0.0"
    port = int(os.getenv("PORT", 5046))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug)
