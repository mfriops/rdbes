#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class FrequencyMeasure:
    FMrecordType = 'FM'

    def __init__(self, freq: dict | None = None):

        """Initialize from a sample dict, or create an empty instance."""
        if freq is None:
            # create an empty instance (all attributes None)
            for spec in self.validate():
                setattr(self, spec["name"], None)
            return

        self.FMid = None
        self.SAid = freq['sample_id']
        self.FMstateOfProcessing = 'DEF'
        self.FMpresentation = 'WHL'
        self.FMclassMeasured = freq['length']
        self.FMnumberAtUnit = freq['frequency']
        self.FMtypeMeasured = 'LengthTotal'
        self.FMmethod = None
        self.FMmeasurementEquipment = None
        self.FMaccuracy = None
        self.FMconversionFactorAssessment = 1
        self.FMtypeAssessment = 'LengthTotal'
        self.FMsampler = None
        self.FMaddGrpMeasurement = None
        self.FMaddGrpMeasurementType = None

    def dict(self) -> dict:
        fm = {}
        fm['FMid'] = self.FMid
        fm['SAid'] = self.SAid
        fm['FMrecordType'] = self.FMrecordType
        fm['FMstateOfProcessing'] = self.FMstateOfProcessing
        fm['FMpresentation'] = self.FMpresentation
        fm['FMclassMeasured'] = self.FMclassMeasured
        fm['FMnumberAtUnit'] = self.FMnumberAtUnit
        fm['FMtypeMeasured'] = self.FMtypeMeasured
        fm['FMmethod'] = self.FMmethod
        fm['FMmeasurementEquipment'] = self.FMmeasurementEquipment
        fm['FMaccuracy'] = self.FMaccuracy
        fm['FMconversionFactorAssessment'] = self.FMconversionFactorAssessment
        fm['FMtypeAssessment'] = self.FMtypeAssessment
        fm['FMsampler'] = self.FMsampler
        fm['FMaddGrpMeasurement'] = self.FMaddGrpMeasurement
        fm['FMaddGrpMeasurementType'] = self.FMaddGrpMeasurementType
        return fm

    def columns(self) -> list[str]:
        """Return all column names in the same order as dict()."""
        return list(map(str.lower, self.dict().keys()))

    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])

    def validate(self):
        return [
            {"name": 'FMid',                           "dtype": "int", "not_null": False},
            {"name": 'SAid',                           "dtype": "int", "not_null": False},
            {"name": 'FMrecordType',                   "dtype": "str", "not_null": True, "allowed_values": ["FM"]},
            {"name": 'FMstateOfProcessing',            "dtype": "str", "not_null": True, "allowed_values": ["BAF", "BOI", "DEF", "DRI", "FRE", "FRO", "SAD", "SAL", "SMO", "UNK"]},
            {"name": 'FMpresentation',                 "dtype": "str", "not_null": True, "allowed_values": ["CBF", "CBF", "CLA", "DWT", "FBS", "FIL", "FIS", "FSP", "GHT", "GUG", "GUH", "GUL", "GUN", "GUS", "GUT", "HEA", "JAP", "JAT", "LAT", "LAP", "LVR", "OTH", "ROE", "SKI", "SUR", "TAL", "TLD", "TNG", "TUB", "Unknown", "WHL", "WNG"]},
            {"name": 'FMclassMeasured',                "dtype": "int", "not_null": True},
            {"name": 'FMnumberAtUnit',                 "dtype": "int", "not_null": True},
            {"name": 'FMtypeMeasured',                 "dtype": "str", "not_null": False, "allowed_values": ["Age", "Berried", "ForkLength", "GeneticPopulation", "HatchSeason", "IlliciumCollected", "InfoConversionFactor", "InfoGenetic", "InfoGonad", "InfoLiver", "InfoOtolithMorphometrics", "InfoParasite", "InfoStomach", "InfoTagging", "LengthCarapace", "LengthLowerJawFork", "LengthMantle", "LengthMaximumShell", "LengthPinchedTail", "LengthPreAnal", "LengthPreCaudal", "LengthStandard", "LengthTail", "LengthTotal", "LengthWingSpan", "Maturity", "OtolithCollected", "ScaleCollected", "Sex", "SpecimenState", "Stock", "VertebraCount", "WeightGutted", "WeightLive", "WeightMeasured", "WidthCarapace", "WidthMaximumShell"]},
            {"name": 'FMmethod',                       "dtype": "str", "not_null": False, "allowed_values": ["-9", "a-spine", "caudal-thorn", "cf-spine", "cleithral-bone", "d-denticle", "df-ray", "df-spine", "egg", "gonad", "illicium", "larvae", "opercular-bone", "otolith", "scale", "shell", "spine", "statolith", "tooth", "vertebra", "wing-bone"]},
            {"name": 'FMmeasurementEquipment',         "dtype": "str", "not_null": False, "allowed_values": ["?"]},
            {"name": 'FMaccuracy',                     "dtype": "str", "not_null": False, "allowed_values": ["100g", "10g", "25mm", "500g", "5cm", "cm", "g", "kg", "mm", "NotApplicable", "scm", "smm", "year"]},
            {"name": 'FMconversionFactorAssessment',   "dtype": "float", "not_null": True},
            {"name": 'FMtypeAssessment',               "dtype": "str", "not_null": True, "allowed_values": ["Age","","Berried","ForkLength","GeneticPopulation","HatchSeason","IlliciumCollected","InfoConversionFactor","InfoGenetic","InfoGonad","InfoLiver","InfoOtolithMorphometrics","InfoParasite","InfoStomach","InfoTagging","LengthCarapace","LengthLowerJawFork","LengthMantle","LengthMaximumShell","LengthPinchedTail","LengthPreAnal","LengthPreCaudal","LengthStandard","LengthTail","LengthTotal","LengthWingSpan","Maturity","OtolithCollected","ScaleCollected","Sex","SpecimenState","Stock","VertebraCount","WeightGutted","WeightLive","WeightMeasured","WidthCarapace","WidthMaximumShell"]},
            {"name": 'FMsampler',                      "dtype": "str", "not_null": False, "allowed_values": ["Control", "Imagery", "Observer", "SelfSampling"]},
            {"name": 'FMaddGrpMeasurement',            "dtype": "float", "not_null": False},
            {"name": 'FMaddGrpMeasurementType',        "dtype": "str", "not_null": False, "allowed_values": ["Age", "Berried", "ForkLength", "GeneticPopulation", "HatchSeason", "IlliciumCollected", "InfoConversionFactor", "InfoGenetic", "InfoGonad", "InfoLiver", "InfoOtolithMorphometrics", "InfoParasite", "InfoStomach", "InfoTagging", "LengthCarapace", "LengthLowerJawFork", "LengthMantle", "LengthMaximumShell", "LengthPinchedTail", "LengthPreAnal", "LengthPreCaudal", "LengthStandard", "LengthTail", "LengthTotal", "LengthWingSpan", "Maturity", "OtolithCollected", "ScaleCollected", "Sex", "SpecimenState", "Stock", "VertebraCount", "WeightGutted", "WeightLive", "WeightMeasured", "WidthCarapace", "WidthMaximumShell"]},
        ]
