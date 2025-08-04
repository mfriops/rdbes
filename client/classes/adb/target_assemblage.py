
import pandas as pd

class AdbTargetAssemblage:

    def __init__(self, trip: dict):
        self.fishing_trip_id = trip['fishing_trip_id']
        self.registration_no = trip['registration_no']
        self.species_no = trip['species_no']
        self.departure_date = trip['departure_date']
        self.landing_date = trip['landing_date']
        self.landing_year = trip['landing_year']
        self.quantity = trip['quantity']
        self.catch_type = trip['catch_type']

    def dict(self) -> dict:
        me = {}
        me['fishing_trip_id'] = self.fishing_trip_id
        me['registration_no'] = self.registration_no
        me['species_no'] = self.species_no
        me['departure_date'] = self.departure_date
        me['landing_date'] = self.landing_date
        me['landing_year'] = self.landing_year
        me['quantity'] = self.quantity
        me['catch_type'] = self.catch_type
        return me

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
