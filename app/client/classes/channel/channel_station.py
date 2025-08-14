#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd
from app.client.utils.geo import geoconvert

class ChannelStation:

    def __init__(self, station: list):
        self.station_id = station['station_id']
        self.cruise_id = station['cruise_id']
        self.station_no = station['station_no']
        self.station_date = station['station_date']
        self.latitude = geoconvert(station['latitude'])
        self.longitude = station['globe_position']*geoconvert(station['longitude'])
        self.latitude_end = geoconvert(station['latitude_end'])
        self.longitude_end = station['globe_position']*geoconvert(station['longitude_end']) if station['longitude_end'] != None else None
        self.globe_position = station['globe_position']
        self.vessel_no = station['vessel_no']
        self.landing_port_no = station['port_no']

    def dict(self) -> dict:
        st = {}
        st['station_id'] = self.station_id
        st['cruise_id'] = self.cruise_id
        st['station_no'] = self.station_no
        st['station_date'] = self.station_date
        st['latitude'] = self.latitude
        st['longitude'] = self.longitude
        st['latitude_end'] = self.latitude_end
        st['longitude_end'] = self.longitude_end
        st['globe_position'] = self.globe_position
        st['vessel_no'] = self.vessel_no
        st['landing_port_no'] = self.landing_port_no
        return st

    def registration_no(self):
        return self.vessel_no

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
