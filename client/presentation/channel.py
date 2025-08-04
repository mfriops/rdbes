#!/usr/local/bin/python3
# coding: utf-8

import os
from typing import Any, Dict, Optional

from flask import json
from client.business.channel import ChannelBusiness

class ChannelPresentation:
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

    channel_business = ChannelBusiness()

    def health(self):
        return self.channel_business.health()

    def get_cruise(self, cruise: str):
        return self.channel_business.get_cruise(cruise)

    def get_station(self, cruise_id: int):
        return self.channel_business.get_station(cruise_id)

    def get_sample(self, station_id: list):
        return self.channel_business.get_sample(station_id)

    def get_measure(self, sample_id: list):
        return self.channel_business.get_measure(sample_id)

    def get_otolith(self, measure_id: list):
        return self.channel_business.get_otolith(measure_id)

    def get_species(self, species_no: int):
        return self.channel_business.get_species(species_no)

    def get_sexual_maturity(self, sexual_maturity_id: int):
        return self.channel_business.get_sexual_maturity(sexual_maturity_id)
