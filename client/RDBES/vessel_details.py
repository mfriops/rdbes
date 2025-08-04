
import pandas as pd
from ..utils.rdbes import vessel_length_category

class VesselDetails:
    VDrecordType = 'VD'

    def __init__(self, vessel: dict):
        self.VDid = None
        self.VDencryptedVesselCode = vessel['vessel_id']
        self.VDyear = vessel['year']
        self.VDcountry = 'IS'
        self.VDhomePort = vessel['home_harbour']
        self.VDflagCountry = 'IS'
        self.VDlength = round(float(vessel['length']))
        self.VDlengthCategory = vessel_length_category(float(vessel['length']))
        self.VDpower = round(float(vessel['power_kw']))
        self.VDtonnage = round(float(vessel['brutto_weight_tons']))
        self.VDtonUnit = 'GRT'

    def dict(self) -> dict:
        vd = {}
        vd['VDid'] = self.VDid
        vd['VDrecordType'] = self.VDrecordType
        vd['VDencryptedVesselCode'] = self.VDencryptedVesselCode
        vd['VDyear'] = self.VDyear
        vd['VDcountry'] = self.VDcountry             #country()
        vd['VDhomePort'] = self.VDhomePort
        vd['VDflagCountry'] = self.VDflagCountry     #country()
        vd['VDlength'] = self.VDlength
        vd['VDlengthCategory'] = self.VDlengthCategory
        vd['VDpower'] = self.VDpower
        vd['VDtonnage'] = self.VDtonnage
        vd['VDtonUnit'] = self.VDtonUnit
        return vd

    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])


    def validate(self):
        return [
            {"name": 'VDid',                    "dtype": "int", "not_null": False},
            {"name": 'VDrecordType',            "dtype": "str", "not_null": True, "allowed_values": ["VD"]},
            {"name": 'VDencryptedVesselCode',   "dtype": "str", "not_null": True},
            {"name": 'VDyear',                  "dtype": "int", "not_null": True, "range": (1965, 2025)},
            {"name": 'VDcountry',               "dtype": "str", "not_null": True, "allowed_values": ["IS"]},
            {"name": 'VDhomePort',              "dtype": "str", "not_null": False},
            {"name": 'VDflagCountry',           "dtype": "str", "not_null": True, "allowed_values": ["IS"]},
            {"name": 'VDlength',                "dtype": "float", "not_null": False, "range": (3.00, 160)},
            {"name": 'VDlengthCategory',        "dtype": "str", "not_null": True, "allowed_values": ["NK","VL0006","VL0008","VL0010","VL0015","VL0608","VL0612","VL0810","VL0815","VL1012","VL1215","VL1218","VL1518","VL15XX","VL1824","VL2440","VL40XX"]},
            {"name": 'VDpower',                 "dtype": "int", "not_null": False, "range": (4, 9000)},
            {"name": 'VDtonnage',               "dtype": "int", "not_null": False, "range": (1, 10000)},
            {"name": 'VDtonUnit',               "dtype": "str", "not_null": False, "allowed_values": ["GRT","GT"]},
        ]
