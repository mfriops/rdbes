
import pandas as pd
import numpy as np
from client.utils.geo import geoconvert

class AdbFishingStation:

    def __init__(self, trip: dict):
        self.fishing_station_id = trip['fishing_station_id']
        self.fishing_trip_id = trip['fishing_trip_id']
        self.fishing_gear_no = trip['fishing_gear_no']
        self.fishing_start = trip['fishing_start']
        self.fishing_end = trip['fishing_end']
        self.latitude = geoconvert(trip['latitude'])
        self.longitude = np.sign(int(trip['longitude']))*geoconvert(abs(int(trip['longitude'])))
        self.latitude_end = geoconvert(trip['latitude_end'])
        self.longitude_end = np.sign(int(trip['longitude_end']))*geoconvert(abs(int(trip['longitude_end'])))

    def dict(self) -> dict:
        me = {}
        me['fishing_station_id'] = self.fishing_station_id
        me['fishing_trip_id'] = self.fishing_trip_id
        me['fishing_gear_no'] = self.fishing_gear_no
        me['fishing_start'] = self.fishing_start
        me['fishing_end'] = self.fishing_end
        me['latitude'] = self.latitude
        me['longitude'] = self.longitude
        me['latitude_end'] = self.latitude_end
        me['longitude_end'] = self.longitude_end
        return me

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
