
import pandas as pd

class ChannelCruise:

    def __init__(self, cruise: dict):
        self.cruise_id = cruise['cruise_id']
        self.cruise = cruise['cruise']
        self.departure = cruise['departure']
        self.arrival = cruise['arrival']

    def dict(self) -> dict:
        cr = {}
        cr['cruise_id'] = self.cruise_id
        cr['cruise'] = self.cruise
        cr['departure'] = self.departure
        cr['arrival'] = self.arrival
        return cr

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])

