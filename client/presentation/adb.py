#!/usr/local/bin/python3
# coding: utf-8

import os
from typing import Any, Dict, Optional

from flask import json
from client.business.adb import AdbBusiness

class AdbPresentation:
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

    adb_business = AdbBusiness()

    def health(self):
        return self.adb_business.health()
