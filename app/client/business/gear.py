#!/usr/local/bin/python3
# coding: utf-8

import os, json
from flask import jsonify
from app.client.api.gear import GearService

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
    gear_api_url = os.environ.get("API_GEAR_GATEWAY_URL")
    if not gear_api_url:
        gear_api_url = "http://127.0.0.1:8001/gear"

    print(gear_api_url)
    gear_service = GearService(gear_api_url.rstrip("/"))

    def health(self):
        return jsonify(self.gear_service.health())

    def get_fishing_gear(self, fishing_gear_nos: list):
        return json.loads(jsonify(self.gear_service.get_fishing_gear(fishing_gear_nos)).data)

    def get_isscfg(self, isscfg_nos: list):
        return json.loads(jsonify(self.gear_service.get_isscfg(isscfg_nos)).data)
