#!/usr/local/bin/python3
# coding: utf-8

import os, json
from flask import jsonify
from app.client.api.adb import AdbService

class AdbBusiness:
    """
    Simple synchronous client for the Oracle-backed RDBES Flask service.

    Parameters
    ----------
    base_url :
        Root URL of the micro-service, *without* a trailing slash.
        Can also be supplied via env-var ``RDBES_API_URL``.
    timeout :
        Per-request timeout in seconds (default **10**).
    """

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #
    adb_api_url = os.environ.get("API_ADB_GATEWAY_URL")
    if not adb_api_url:
        gear_api_url = "http://127.0.0.1:8001/adb"

    print(adb_api_url)
    adb_service = AdbService(adb_api_url.rstrip("/"))

    def health(self):
        return jsonify(self.adb_service.health())

    def get_fishing_trip(self, registration_no: int, station_date: str):
        return json.loads(jsonify(self.adb_service.get_fishing_trip( registration_no, station_date)).data)

    def get_fishing_trips(self, landing_from: str, landing_to: str):
        return json.loads(jsonify(self.adb_service.get_fishing_trips( landing_from, landing_to)).data)

    def get_fishing_station(self, fishing_trip_ids: list):
        return json.loads(jsonify(self.adb_service.get_fishing_station(fishing_trip_ids)).data)

    def get_fishing_station_for_target(self, fishing_trip_ids: list, target_species_no: int):
        return json.loads(jsonify(self.adb_service.get_fishing_station_for_target(fishing_trip_ids, target_species_no)).data)

    def get_trawl_and_seine_net(self, fishing_station_ids: list):
        return json.loads(jsonify(self.adb_service.get_trawl_and_seine_net(fishing_station_ids)).data)

    def get_target_assemblage(self, species_no: str, landing_year: int):
        return json.loads(jsonify(self.adb_service.get_target_assemblage(species_no, landing_year)).data)
