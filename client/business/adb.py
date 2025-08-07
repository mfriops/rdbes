#!/usr/local/bin/python3
# coding: utf-8

import os
import json

from flask import jsonify
from client.api.adb import AdbService

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

    # gear_url = os.environ.get("ADB_API_URL", "http://localhost:5046")
    adb_api_url = os.environ.get("API_GATEWAY_URL", "http://localhost:8001").rstrip("/")
    adb_api_url = adb_api_url + '/' + os.environ.get("ADB_API_GATEWAY", "adb").rstrip("/")
    print(adb_api_url)
    adb_service = AdbService(adb_api_url)

    def health(self):
        return jsonify(self.adb_service.health())

    def get_fishing_trip(self, registration_no: int, station_date: str):
        return json.loads(jsonify(self.adb_service.get_fishing_trip( registration_no, station_date)).data)

    def get_fishing_trips(self, landing_from: str, landing_to: str):
        return json.loads(jsonify(self.adb_service.get_fishing_trips( landing_from, landing_to)).data)

    def get_fishing_station(self, fishing_trip_ids: list):
        return json.loads(jsonify(self.adb_service.get_fishing_station(fishing_trip_ids)).data)

    def get_trawl_and_seine_net(self, fishing_station_ids: list):
        return json.loads(jsonify(self.adb_service.get_trawl_and_seine_net(fishing_station_ids)).data)

    def get_target_assemblage(self, species_no: str, landing_year: int):
        return json.loads(jsonify(self.adb_service.get(species_no, landing_year)).data)
