#!/usr/local/bin/python3
# coding: utf-8

import os, json
from flask import jsonify
from app.client.api.vessel import VesselService

class VesselBusiness:
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
    vessel_api_url = os.environ.get("API_VESSEL_GATEWAY_URL")
    if not vessel_api_url:
        vessel_api_url = "http://127.0.0.1:8001/vessel"

    print(vessel_api_url)
    vessel_service = VesselService(vessel_api_url.rstrip("/"))

    def health(self):
        return jsonify(self.vessel_service.health())

    def get_vessel(self, registration_no: list):
        return json.loads(jsonify(self.vessel_service.get_vessel(registration_no)).data)
