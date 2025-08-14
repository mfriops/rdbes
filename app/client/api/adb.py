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
from typing import Any, Dict, Optional, List, Sequence, Union

class NotFound(Exception):
    """Raised when the micro-service returns HTTP 404."""


class AdbService:
    """
    Simple synchronous client for the Oracle-backed RDBES Flask service.

    Parameters
    ----------
    base_url :
        Root URL of the micro-service, *without* a trailing slash.
        Can also be supplied via env-var ``ADB_API_URL``.
    timeout :
        Per-request timeout in seconds (default **10**).
    """

    def __init__(self, base_url: Optional[str] = None, timeout: int = 10) -> None:
        # self.base_url = (base_url or os.getenv("ADB_API_URL") or "").rstrip("/")
        print(base_url)
        self.base_url = base_url
        if not self.base_url:
            raise ValueError("base_url not provided and ADB_API_URL not set")
        self.timeout = timeout
        self._session = Session()  # connection pooling

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #
    def health(self) -> Dict[str, Any]:
        return self._get_json("/health")

    def get_fishing_trip(self, registration_no: int, station_date: str) -> Dict[str, Any]:

        if registration_no is None or station_date is None:
            raise ValueError("registration_no and station_date may not be empty")

        query = 'registration_no=' + str(registration_no) + '&fishing_date=' + station_date
        endpoint = f"/fishing_trip?{query}"
        return self._get_json(endpoint)


    def get_fishing_trips(self, landing_from: str, landing_to: str) -> Dict[str, Any]:

        if landing_from is None or landing_to is None:
            raise ValueError("landing_from and landing_to may not be empty")

        query = 'landing_from=' + str(landing_from) + '&landing_to=' + landing_to
        endpoint = f"/fishing_trip?{query}"
        return self._get_json(endpoint)


    def get_fishing_station(self, fishing_trip_ids: Union[int, Sequence[int]]) -> Dict[str, Any]:
        # normalise to list[int] so we can join below
        if isinstance(fishing_trip_ids, str):
            ids: List[str] = [fishing_trip_ids]
        else:
            ids = list(fishing_trip_ids)

        if fishing_trip_ids is None:
            raise ValueError("fishing_trip_ids may not be empty")

        # build “…?species_no=1,2,3”
        query = ",".join(str(i) for i in ids)
        endpoint = f"/fishing_station?fishing_trip_id={query}"
        return self._get_json(endpoint)


    def get_trawl_and_seine_net(self, fishing_station_ids: Union[int, Sequence[int]]) -> Dict[str, Any]:
        # normalise to list[int] so we can join below
        if isinstance(fishing_station_ids, str):
            ids: List[str] = [fishing_station_ids]
        else:
            ids = list(fishing_station_ids)

        if fishing_station_ids is None:
            raise ValueError("fishing_station_ids may not be empty")

        # build “…?species_no=1,2,3”
        query = ",".join(str(i) for i in ids)
        endpoint = f"/trawl_and_seine_net?fishing_station_id={query}"
        return self._get_json(endpoint)


    def get_target_assemblage(self, species_no: int, year: int) -> Dict[str, Any]:

        if species_no is None or year is None:
            raise ValueError("species_no and year may not be empty")

        query = 'species_no=' + str(species_no) + '&year=' + str(year)
        endpoint = f"/target_assemblage?{query}"
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
