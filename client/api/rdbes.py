#!/usr/local/bin/python3
# coding: utf-8

import os
from requests import request
from urllib.parse import urlencode
from typing import Any, Dict, List, Sequence, Union

# ---------------------------------------------------------------------------
# Data‑access layer
# ---------------------------------------------------------------------------

DEFAULT_TIMEOUT: int = 5  # seconds

class RdbesService:
    """Light wrapper around the *Flask Oracle Insert API* JSON endpoints."""

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        # self.base_url = (base_url or os.getenv("RDBES_API_URL") or "").rstrip("/")
        print(base_url)
        self.base_url = base_url
        self.timeout = timeout

    # Internal HTTP helper --------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, *, json: Dict[str, Any] | None = None) -> Any:
        resp = request(method, self._url(path), json=json, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    def _get_json(self, path: str) -> Dict[str, Any]:
        return self._request("GET", path)

    # Public API ------------------------------------------------------------

    def health(self) -> Any:
        return self._request("GET", "health")

    def insert(self, table: str, payload: Dict[str, Any]) -> Any:
        return self._request("POST", table, json=payload)

    def select(self, table: str) -> Any:
        return self._request("GET", table)

    def get_harbour(self, port_nos: Union[int, Sequence[int]]) -> Dict[str, Any]:
        # normalise to list[int] so we can join below
        if isinstance(port_nos, int):
            ids: List[int] = [port_nos]
        else:
            ids = list(port_nos)

        if not ids:
            raise ValueError("port_nos may not be empty")

        # build “…?registration_no=1,2,3”
        query = ",".join(str(i) for i in ids)
        endpoint = f"/harbour?port_no={query}"
        return self._get_json(endpoint)

    def get_area(self, lat: float, lon: float) -> Dict[str, Any]:
        params = '?' + urlencode({"lat": lat, "lon": lon})
        return self._request("GET", f"/area{params}")

    def get_metier(self, area_code: str, gear_type: str, target_assemblage: str, mesh_size: int) -> Dict[str, Any]:
        params = '?' + urlencode({
            "area_code": area_code,
            "gear_type": gear_type,
            "target_assemblage": target_assemblage,
            "mesh_size": mesh_size
        })
        return self._request("GET", f"/metier{params}")

