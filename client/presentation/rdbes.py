#!/usr/local/bin/python3
# coding: utf-8

import os

from typing import Any, Dict, Optional
from flask import jsonify

from client.business.rdbes import RdbesBusiness


class RdbesPresentation:
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

    rdbes_business = RdbesBusiness()

    def health(self) -> Dict[str, Any]:
        return self.rdbes_business.health()

    def insert(self, table: str, payload: Dict[str, Any]) -> Any:
        return self.rdbes_business.insert(table, payload)

    def select(self, table: str) -> Any:
        return self.rdbes_business.select(table)

    def get_harbour(self, port_no: int):
        return self.rdbes_business.get_harbour(port_no)

    def get_area(self, code: str):
        return self.rdbes_business.get_area(code)

    def get_metier(self, metier: str):
        return self.rdbes_business.get_rdbes_business(metier)

    def set_sample(self, cruiseDict):
        return self.rdbes_business.write_sample(cruiseDict)

    # def set_sample(self, cruiseDict):
    #     res = self.rdbes_business.del_sample(cruiseDict)
    #     return res

    def set_landing(self, cruiseDict):
        res = self.rdbes_business.write_landing(cruiseDict)
        return res

    def set_effort(self, cruiseDict):
        res = self.rdbes_business.write_effort(cruiseDict)
        return res

    def set_file(self, locaid, fileType):
        res = self.rdbes_business.write_file(locaid, fileType)
        return res
