#!/usr/local/bin/python3
# coding: utf-8

import os, json
from flask import jsonify
from app.client.api.agf import AgfService

class AgfBusiness:
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
    landing_api_url = os.environ.get("API_AGF_GATEWAY_URL")
    if not landing_api_url:
        landing_api_url = "http://127.0.0.1:8001/agf"

    print(landing_api_url)
    agf_service = AgfService(landing_api_url.rstrip("/"))

    def health(self):
        return jsonify(self.agf_service.health())

    def get_landings(self, date_from: str, date_to: str):
        return json.loads(jsonify(self.agf_service.get_landings( date_from, date_to)).data)
