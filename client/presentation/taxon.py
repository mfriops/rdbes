#!/usr/local/bin/python3
# coding: utf-8

import os
from typing import Any, Dict, Optional

from flask import json
from client.business.taxon import TaxonBusiness

class TaxonPresentation:
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

    taxon_business = TaxonBusiness()

    def health(self):
        return self.taxon_business.health()

    def get_species(self, species_no: int):
        return self.taxon_business.get_species(species_no)
