#!/usr/local/bin/python3
# coding: utf-8

"""
client_rdbes_service.py
-----------------------
Typed helper for the read-only Flask micro-service that exposes:

    /health
    /cruise/<str>
    /station/<int>
    /sample/<int>
    /measure/<int>
    /species/<int>
    /sexual_maturity/<int>
    /otolith/<int>
    /harbour/<str>
    /vessel/<int>
    /gear/<int>

Usage
 from client_rdbes_service import RDBESClient, NotFound
 api = RDBESClient("http://localhost:8000")
 api.health()                     # {'channel-status': 'ok'}
 cruise = api.get_cruise("IS-SUR-2019")
 station = api.get_station(12345)
"""
from __future__ import annotations

from requests import HTTPError, Response, Session
from typing import Any, Dict, Optional

class NotFound(Exception):
    """Raised when the micro-service returns HTTP 404."""


class QuotaService:
    """
    Simple synchronous client for the Oracle-backed RDBES Flask service.

    Parameters
    ----------
    base_url :
        Root URL of the micro-service, *without* a trailing slash.
        Can also be supplied via env-var ``AGF_API_URL``.
    timeout :
        Per-request timeout in seconds (default **10**).
    """

    def __init__(self, base_url: Optional[str] = None, timeout: int = 10) -> None:
        # self.base_url = (base_url or os.getenv("AGF_API_URL") or "").rstrip("/")
        print(base_url)
        self.base_url = base_url
        if not self.base_url:
            raise ValueError("base_url not provided and AGF_API_URL not set")
        self.timeout = timeout
        self._session = Session()  # connection pooling

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #
    def health(self) -> Dict[str, Any]:
        return self._get_json("/health")


    def get_quota(self, species_no: int, year: int) -> Dict[str, Any]:

        if species_no is None or year is None:
            raise ValueError("Data species_no and year may not be empty")

        query = 'species=' + str(species_no) + '&year=' + str(year)
        endpoint = f"/quota?{query}"
        return self._get_json(endpoint)


    # ------------------------------------------------------------------ #
    # Internal helpers                                                   #
    # ------------------------------------------------------------------ #
    def _get_json(self, path: str) -> Dict[str, Any]:
        """Perform *GET* and return parsed JSON (raises ``NotFound`` on 404)."""
        url = f"{self.base_url}{path}"
        try:
            resp: Response = self._session.get(url, timeout=self.timeout)
            resp.raise_for_status()
        except HTTPError as exc:  # covers 4xx & 5xx
            if exc.response is not None and exc.response.status_code == 404:
                raise NotFound(f"Resource not found: {url}") from None
            raise
        return resp.json()
