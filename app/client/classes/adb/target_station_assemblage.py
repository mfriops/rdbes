#!/usr/local/bin/python3
# coding: utf-8

import numpy as np
import pandas as pd
from app.client.utils.geo import geoconvert

class AdbTargetStationAssemblage:

    def __init__(self, trip: dict):
        self.fishing_station_id = trip['fishing_station_id']
        self.fishing_trip_id = trip['fishing_trip_id']
        self.registration_no = trip['registration_no']
        self.fishing_gear_no = trip['fishing_gear_no']
        self.fishing_start = trip['fishing_start']
        self.fishing_end = trip['fishing_end']
        self.latitude = geoconvert(trip['latitude'])
        self.longitude = (-1)*np.sign(trip['longitude'])*geoconvert(abs(trip['longitude']))
        self.latitude_end = geoconvert(trip['latitude_end'])
        self.longitude_end = (-1)*np.sign(trip['longitude_end'])*geoconvert(abs(trip['longitude_end']))
        self.species_no = trip['species_no']
        self.quantity = trip['quantity']


    def dict(self) -> dict:
        me = {}
        me['fishing_station_id'] = self.fishing_station_id
        me['fishing_trip_id'] = self.fishing_trip_id
        me['registration_no'] = self.registration_no
        me['fishing_gear_no'] = self.fishing_gear_no
        me['fishing_start'] = self.fishing_start
        me['fishing_end'] = self.fishing_end
        me['latitude'] = self.latitude
        me['longitude'] = self.longitude
        me['latitude_end'] = self.latitude_end
        me['longitude_end'] = self.longitude_end
        me['species_no'] = self.species_no
        me['quantity'] = self.quantity
        return me

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
