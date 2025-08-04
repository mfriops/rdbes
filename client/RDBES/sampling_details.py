
import pandas as pd

class SamplingDetails:
    SDrecordType = 'SD'

    def __init__(self):
        self.SDid = None
        self.DEid = None
        self.SDcountry = 'IS'
        self.SDinstitution = '4766'

    def dict(self) -> dict:
        sd = {}
        sd['SDid'] = self.SDid
        sd['DEid'] = self.DEid
        sd['SDrecordType'] = self.SDrecordType
        sd['SDcountry'] = self.SDcountry
        sd['SDinstitution'] = self.SDinstitution
        return sd

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
