
import pandas as pd

class SpeciesList:
    SLrecordType = 'SL'

    def __init__(self, species: dict):
        self.SLid = None
        self.SLcountry = 'IS'
        self.SLinstitute = '4766'
        self.SLspeciesListName = species['name']
        self.SLyear = species['year']
        self.SLcatchFraction = 'Catch'


    def dict(self) -> dict:
        sl = {}
        sl['SLid'] = self.SLid
        sl['SLrecordType'] = self.SLrecordType
        sl['SLcountry'] = self.SLcountry
        sl['SLinstitute'] = self.SLinstitute
        sl['SLspeciesListName'] = self.SLspeciesListName
        sl['SLyear'] = self.SLyear
        sl['SLcatchFraction'] = self.SLcatchFraction
        return sl


    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])


    def validate(self):
        return [
            {"name": 'SLid',                       "dtype": "int", "not_null": False},
            {"name": 'SLrecordType',               "dtype": "str", "not_null": True, "allowed_values": ["SL"]},
            {"name": 'SLcountry',                  "dtype": "str", "not_null": True, "allowed_values": ["IS"]},
            {"name": 'SLinstitute',                "dtype": "str", "not_null": True, "allowed_values": ["4766"]},
            {"name": 'SLspeciesListName',          "dtype": "str", "not_null": True},
            {"name": 'SLyear',                     "dtype": "int", "not_null": True, "range": (1965, 2025)},
            {"name": 'SLcatchFraction',            "dtype": "str", "not_null": True, "allowed_values": ["Catch","Dis","Lan"]},
        ]
