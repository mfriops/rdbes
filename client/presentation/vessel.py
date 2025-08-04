#!/usr/local/bin/python3
# coding: utf-8

import os
from typing import Any, Dict, Optional

from flask import json
from client.business.vessel import VesselBusiness

class VesselPresentation:
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

    vessel_business = VesselBusiness()

    def health(self):
        return self.vessel_business.health()

    def get_vessel(self, registration_no: int):
        return self.vessel_business.get_vessel(registration_no)
