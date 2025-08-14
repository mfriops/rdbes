#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class AdbFishingTrip:

    def __init__(self, trip: dict):
        self.fishing_trip_id = trip['id']
        self.registration_no = trip['vessel_no']
        self.departure = trip['departure']
        self.departure_port_no = trip['departure_port_no']
        self.landing = trip['landing']
        self.landing_port_no = trip['landing_port_no']

    def dict(self) -> dict:
        me = {}
        me['fishing_trip_id'] = self.fishing_trip_id
        me['registration_no'] = self.registration_no
        me['departure'] = self.departure
        me['departure_port_no'] = self.departure_port_no
        me['landing'] = self.landing
        me['landing_port_no'] = self.landing_port_no
        return me

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
