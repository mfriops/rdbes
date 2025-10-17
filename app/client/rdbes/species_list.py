#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd
from app.client.api.misc import get_country, get_organisation


class SpeciesList:
    SLrecordType = 'SL'

    def __init__(self, species: dict | None = None):

        """Initialize from a sample dict, or create an empty instance."""
        if species is None:
            # create an empty instance (all attributes None)
            for spec in self.validate():
                setattr(self, spec["name"], None)
            return

        self.SLid = None
        self.SLcountry = get_country()
        self.SLinstitute = get_organisation()
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

    def columns(self) -> list[str]:
        """Return all column names in the same order as dict()."""
        return list(map(str.lower, self.dict().keys()))

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
