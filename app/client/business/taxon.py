#!/usr/local/bin/python3
# coding: utf-8

import os, json
from flask import jsonify
from app.client.api.taxon import TaxonService

class TaxonBusiness:
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
    taxon_api_url = os.environ.get("API_TAXON_GATEWAY_URL")
    if not taxon_api_url:
        taxon_api_url = "http://127.0.0.1:8001/taxon"

    print(taxon_api_url)
    taxon_service = TaxonService(taxon_api_url.rstrip("/"))

    def health(self):
        return jsonify(self.taxon_service.health())

    def get_species(self, species_no: int):
        return json.loads(jsonify(self.taxon_service.get_species(species_no)).data)

