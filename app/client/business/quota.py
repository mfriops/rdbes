#!/usr/local/bin/python3
# coding: utf-8

import os, json
from flask import jsonify
from app.client.api.quota import QuotaService

class QuotaBusiness:
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
    quota_api_url = os.environ.get("API_QUOTA_GATEWAY_URL")
    if not quota_api_url:
        quota_api_url = "http://127.0.0.1:8001/quota"

    print(quota_api_url)
    quota_service = QuotaService(quota_api_url.rstrip("/"))

    def health(self):
        return jsonify(self.quota_service.health())

    def get_quota(self, species_no: int, year: int):
        return json.loads(jsonify(self.quota_service.get_quota(species_no, year)).data)
