#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class IndividualSpecies:
    ISrecordType = 'IS'

    def __init__(self, species: dict):
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
