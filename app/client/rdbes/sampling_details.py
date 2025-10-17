#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd
from app.client.api.misc import get_country, get_organisation

class SamplingDetails:
    SDrecordType = 'SD'

    def __init__(self, empty: bool = False):
        """
        Initialize SamplingDetails.
        If empty=True, create an empty instance without calling external functions.
        """
        self.SDid = None
        self.DEid = None

        if empty:
            self.SDcountry = None
            self.SDinstitution = None
        else:
            self.SDcountry = get_country()
            self.SDinstitution = get_organisation()

    def dict(self) -> dict:
        sd = {}
        sd['SDid'] = self.SDid
        sd['DEid'] = self.DEid
        sd['SDrecordType'] = self.SDrecordType
        sd['SDcountry'] = self.SDcountry
        sd['SDinstitution'] = self.SDinstitution
        return sd

    def columns(self) -> list[str]:
        """Return all column names in the same order as dict()."""
        return list(map(str.lower, self.dict().keys()))

    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])

    def validate(self):
        return [
            {"name": 'SDid',            "dtype": "int", "not_null": False },
            {"name": 'DEid',            "dtype": "int", "not_null": False },
            {"name": 'SDrecordType',    "dtype": "str", "not_null": True, "allowed_values": ["SD"] },
            {"name": 'SDcountry',       "dtype": "str", "not_null": True, "allowed_values": ["IS"] },
            {"name": 'SDinstitution',   "dtype": "str", "not_null": True, "allowed_values": ["4766"] },
        ]
