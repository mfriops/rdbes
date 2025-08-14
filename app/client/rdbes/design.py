#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class Design:
    DErecordType = 'DE'

    def __init__(self, cruise: dict):
        self.DEid = None
        self.DEsamplingScheme = "FO_Pelagic_At-sea"
        self.DEsamplingSchemeType = 'NatRouCF'
        self.DEyear = cruise['year']
        self.DEstratumName = cruise['cruise']
        self.DEhierarchyCorrect = "Y"
        self.DEhierarchy = "2"
        self.DEsampled = "Y"
        self.DEreasonNotSampled = None
        self.DEnonResponseCollected = "N"
        self.DEauxiliaryVariableTotal = None
        self.DEauxiliaryVariableValue = None
        self.DEauxiliaryVariableName = None
        self.DEauxiliaryVariableUnit = None
        self.DElabel = None

    def dict(self) -> dict:
        de = {}
        de['DEid'] = self.DEid
        de['DErecordType'] = self.DErecordType
        de['DEsamplingScheme'] = self.DEsamplingScheme
        de['DEsamplingSchemeType'] = self.DEsamplingSchemeType
        de['DEyear'] = self.DEyear
        de['DEstratumName'] = self.DEstratumName
        de['DEhierarchyCorrect'] = self.DEhierarchyCorrect
        de['DEhierarchy'] = self.DEhierarchy
        de['DEsampled'] = self.DEsampled
        de['DEreasonNotSampled'] = self.DEreasonNotSampled
        de['DEnonResponseCollected'] = self.DEnonResponseCollected
        de['DEauxiliaryVariableTotal'] = self.DEauxiliaryVariableTotal
        de['DEauxiliaryVariableValue'] = self.DEauxiliaryVariableValue
        de['DEauxiliaryVariableName'] = self.DEauxiliaryVariableName
        de['DEauxiliaryVariableUnit'] = self.DEauxiliaryVariableUnit
        de['DElabel'] = self.DElabel
        return de

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])

    def validate(self) -> list:
        return [
            {"name": 'DEid',                        "dtype": "int", "not_null": False},
            {"name": 'DErecordType',                "dtype": "str", "not_null": True, "allowed_values": ["DE"]},
            {"name": 'DEsamplingScheme',            "dtype": "str", "not_null": True, "allowed_values": ["FO_Pelagic_At-sea", "FO_Pelagic_On-shore"]},
            {"name": 'DEsamplingSchemeType',        "dtype": "str", "not_null": True, "allowed_values": ["NatPilCF", "NatPilIB", "NatRouCF", "NatRouIB", "RegPilCF", "RegPilIB", "RegRouCF", "ResProIB"]},
            {"name": 'DEyear',                      "dtype": "int", "not_null": True, "range": (1965, 2025)},
            {"name": 'DEstratumName',               "dtype": "str", "not_null": True},
            {"name": 'DEhierarchyCorrect',          "dtype": "str", "not_null": True, "allowed_values": ["N", "Y"]},
            {"name": 'DEhierarchy',                 "dtype": "int", "not_null": True, "range": (1, 13)},
            {"name": 'DEsampled',                   "dtype": "str", "not_null": True, "allowed_values": ["N", "Y"]},
            {"name": 'DEreasonNotSampled',          "dtype": "str", "not_null": False, "allowed_values": ["CameraNotWorking", "CameraViewObstructed", "IndustryDeclined", "NoAnswer", "NoContactDetails", "NotAvailable", "ObserverDeclined", "Other", "OutOfFrame", "PoorImageQuality", "QuotaReached", "Unknown"]},
            {"name": 'DEnonResponseCollected',      "dtype": "str", "not_null": False, "allowed_values": ["N", "Y"]},
            {"name": 'DEauxiliaryVariableTotal',    "dtype": "float", "not_null": False},
            {"name": 'DEauxiliaryVariableValue',    "dtype": "float", "not_null": False},
            {"name": 'DEauxiliaryVariableName',     "dtype": "str", "not_null": False},
            {"name": 'DEauxiliaryVariableUnit',     "dtype": "str", "not_null": False},
            {"name": 'DElabel',                     "dtype": "str", "not_null": False},
        ]
