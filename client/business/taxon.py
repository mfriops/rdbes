#!/usr/local/bin/python3
# coding: utf-8

import os
import json

from flask import jsonify
from client.api.taxon import TaxonService

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

    # taxon_url = os.environ.get("TAXON_API_URL", "http://localhost:5042")
    taxon_api_url = os.environ.get("API_GATEWAY_URL", "http://localhost:8001").rstrip("/")
    taxon_api_url = taxon_api_url + '/' + os.environ.get("TAXON_API_GATEWAY", "taxon").rstrip("/")
    print(taxon_api_url)
    taxon_service = TaxonService(taxon_api_url)

    def health(self):
        return jsonify(self.taxon_service.health())

    def get_species(self, species_no: int):
        return json.loads(jsonify(self.taxon_service.get_species(species_no)).data)

