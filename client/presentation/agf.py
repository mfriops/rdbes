#!/usr/local/bin/python3
# coding: utf-8

import os
from typing import Any, Dict, Optional

from flask import json
from client.business.agf import AgfBusiness

class AgfPresentation:
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

    agf_business = AgfBusiness()

    def health(self):
        return self.agf_business.health()
