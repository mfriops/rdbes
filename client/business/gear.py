#!/usr/local/bin/python3
# coding: utf-8

import os
import json

from flask import jsonify
from client.api.gear import GearService

class GearBusiness:
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

    # gear_url = os.environ.get("GEAR_API_URL", "http://localhost:5043")
    gear_api_url = os.environ.get("API_GATEWAY_URL", "http://localhost:8001").rstrip("/")
    gear_api_url = gear_api_url + '/' + os.environ.get("GEAR_API_GATEWAY", "gear").rstrip("/")
    print(gear_api_url)
    gear_service = GearService(gear_api_url)

    def health(self):
        return jsonify(self.gear_service.health())

    def get_fishing_gear(self, fishing_gear_nos: list):
        return json.loads(jsonify(self.gear_service.get_fishing_gear(fishing_gear_nos)).data)

    def get_isscfg(self, isscfg_nos: list):
        return json.loads(jsonify(self.gear_service.get_isscfg(isscfg_nos)).data)
