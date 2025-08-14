#!/usr/local/bin/python3
# coding: utf-8

import os, json
from flask import jsonify
from app.client.api.channel import ChannelService


class ChannelBusiness:
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
    channel_api_url = os.environ.get("API_CHANNEL_GATEWAY_URL")
    if not channel_api_url:
        channel_api_url = "http://127.0.0.1:8001/channel"

    print(channel_api_url)
    channel_service = ChannelService(channel_api_url.rstrip("/"))

    def health(self):
        return jsonify(self.channel_service.health())

    def get_cruise(self, cruise: str):
        return json.loads(jsonify(self.channel_service.get_cruise(cruise)).data)

    def get_station(self, cruise_id: int):
        return json.loads(jsonify(self.channel_service.get_station(cruise_id)).data)

    def get_sample(self, station_ids: list):
        return json.loads(jsonify(self.channel_service.get_sample(station_ids)).data)

    def get_measure(self, sample_ids: list):
        return json.loads(jsonify(self.channel_service.get_measure(sample_ids)).data)

    def get_otolith(self, measure_ids: list):
        return json.loads(jsonify(self.channel_service.get_otolith(measure_ids)).data)

    def get_species(self, species_nos: list):
        return json.loads(jsonify(self.channel_service.get_species(species_nos)).data)

    def get_sexual_maturity(self, sexual_maturity_id: int):
        return jsonify(self.channel_service.get_sexual_maturity(sexual_maturity_id))
