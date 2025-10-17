#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class IndividualSpecies:
    ISrecordType = 'IS'

    def __init__(self, species: dict | None = None):

        """Initialize from a sample dict, or create an empty instance."""
        if species is None:
            # create an empty instance (all attributes None)
            for spec in self.validate():
                setattr(self, spec["name"], None)
            return

        self.ISid = None
        self.SLid = None
        self.IScommercialTaxon = species['worms_id']
        self.ISspeciesCode = species['worms_id']

    def dict(self) -> dict:
        isp = {}
        isp['ISid'] = self.ISid
        isp['SLid'] = self.SLid
        isp['ISrecordType'] = self.ISrecordType
        isp['IScommercialTaxon'] = self.IScommercialTaxon
        isp['ISspeciesCode'] = self.ISspeciesCode
        return isp

    def columns(self) -> list[str]:
        """Return all column names in the same order as dict()."""
        return list(map(str.lower, self.dict().keys()))

    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])

    def validate(self):
        return [
            {"name": 'ISid',                       "dtype": "int", "not_null": False},
            {"name": 'SLid',                       "dtype": "int", "not_null": False},
            {"name": 'ISrecordType',               "dtype": "str", "not_null": True, "allowed_values": ["IS"]},
            {"name": 'IScommercialTaxon',          "dtype": "int", "not_null": True}, # Wormscode
            {"name": 'ISspeciesCode',              "dtype": "int", "not_null": True}, # Wormscode
        ]
