#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class SpeciesSelection:
    SSrecordType = 'SS'

    def __init__(self, species: dict | None = None):

        """Initialize from a sample dict, or create an empty instance."""
        if species is None:
            # create an empty instance (all attributes None)
            for spec in self.validate():
                setattr(self, spec["name"], None)
            return

        self.SSid = species['sample_id']
        self.LEid = None
        self.FOid = species['fishing_station_id']
        self.FTid = None
        self.OSid = None
        self.TEid = None
        self.SLid = None
        self.SSsequenceNumber = None
        self.SSstratification = 'N'
        self.SSstratumName = 'U'
        self.SSclustering = 'N'
        self.SSclusterName = 'U'
        self.SSobservationActivityType = 'Unknown'
        self.SScatchFraction = 'Catch'
        self.SSobservationType = 'Visual'
        self.SSsampler = 'SelfSampling'
        self.SSspeciesListName = species['name']
        self.SSuseForCalculateZero = 'N'
        self.SStimeTotal = None
        self.SStimeTotalDataBasis = None
        self.SStimeSampled = None
        self.SSnumberTotal = None
        self.SSnumberTotalDataBasis = None
        self.SSnumberSampled = None
        self.SSselectionProb = None
        self.SSinclusionProb = None
        self.SSselectionMethod = 'FIXED'
        self.SSunitName = species['name']
        self.SSselectionMethodCluster = None
        self.SSnumberTotalClusters = None
        self.SSnumberSampledClusters = None
        self.SSselectionProbCluster = None
        self.SSinclusionProbCluster = None
        self.SSsampled = 'Y'
        self.SSreasonNotSampled = None
        self.SSnonResponseCollected = None
        self.SSauxiliaryVariableTotal = None
        self.SSauxiliaryVariableValue = None
        self.SSauxiliaryVariableName = None
        self.SSauxiliaryVariableUnit = None

    def dict(self) -> dict:
        ss = {}
        ss['SSid'] = self.SSid
        ss['LEid'] = self.LEid
        ss['FOid'] = self.FOid
        ss['FTid'] = self.FTid
        ss['OSid'] = self.OSid
        ss['TEid'] = self.TEid
        ss['SLid'] = self.SLid
        ss['SSrecordType'] = self.SSrecordType
        ss['SSsequenceNumber'] = self.SSsequenceNumber
        ss['SSstratification'] = self.SSstratification
        ss['SSstratumName'] = self.SSstratumName
        ss['SSclustering'] = self.SSclustering
        ss['SSclusterName'] = self.SSclusterName
        ss['SSobservationActivityType'] = self.SSobservationActivityType
        ss['SScatchFraction'] = self.SScatchFraction
        ss['SSobservationType'] = self.SSobservationType
        ss['SSsampler'] = self.SSsampler
        ss['SSspeciesListName'] = self.SSspeciesListName
        ss['SSuseForCalculateZero'] = self.SSuseForCalculateZero
        ss['SStimeTotal'] = self.SStimeTotal
        ss['SStimeTotalDataBasis'] = self.SStimeTotalDataBasis
        ss['SStimeSampled'] = self.SStimeSampled
        ss['SSnumberTotal'] = self.SSnumberTotal
        ss['SSnumberTotalDataBasis'] = self.SSnumberTotalDataBasis
        ss['SSnumberSampled'] = self.SSnumberSampled
        ss['SSselectionProb'] = self.SSselectionProb
        ss['SSinclusionProb'] = self.SSinclusionProb
        ss['SSselectionMethod'] = self.SSselectionMethod
        ss['SSunitName'] = self.SSunitName
        ss['SSselectionMethodCluster'] = self.SSselectionMethodCluster
        ss['SSnumberTotalClusters'] = self.SSnumberTotalClusters
        ss['SSnumberSampledClusters'] = self.SSnumberSampledClusters
        ss['SSselectionProbCluster'] = self.SSselectionProbCluster
        ss['SSinclusionProbCluster'] = self.SSinclusionProbCluster
        ss['SSsampled'] = self.SSsampled
        ss['SSreasonNotSampled'] = self.SSreasonNotSampled
        ss['SSnonResponseCollected'] = self.SSnonResponseCollected
        ss['SSauxiliaryVariableTotal'] = self.SSauxiliaryVariableTotal
        ss['SSauxiliaryVariableValue'] = self.SSauxiliaryVariableValue
        ss['SSauxiliaryVariableName'] = self.SSauxiliaryVariableName
        ss['SSauxiliaryVariableUnit'] = self.SSauxiliaryVariableUnit
        return ss

    def columns(self) -> list[str]:
        """Return all column names in the same order as dict()."""
        return list(map(str.lower, self.dict().keys()))

    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])

    def validate(self):
        return [
            {"name": 'SSid',                       "dtype": "int", "not_null": False},
            {"name": 'LEid',                       "dtype": "int", "not_null": False},
            {"name": 'FOid',                       "dtype": "int", "not_null": False},
            {"name": 'FTid',                       "dtype": "str", "not_null": False},
            {"name": 'OSid',                       "dtype": "int", "not_null": False},
            {"name": 'TEid',                       "dtype": "int", "not_null": False},
            {"name": 'SLid',                       "dtype": "int", "not_null": False},
            {"name": 'SSrecordType',               "dtype": "str", "not_null": True, "allowed_values": ["SS"]},
            {"name": 'SSsequenceNumber',           "dtype": "int", "not_null": True},
            {"name": 'SSstratification',           "dtype": "str", "not_null": True, "allowed_values": ["N", "Y"]},
            {"name": 'SSstratumName',              "dtype": "str", "not_null": True},
            {"name": 'SSclustering',               "dtype": "str", "not_null": True, "allowed_values": ["1C", "1CS", "2C", "2CS", "N", "S1C", "S2C"]},
            {"name": 'SSclusterName',              "dtype": "str", "not_null": True},
            {"name": 'SSobservationActivityType',  "dtype": "str", "not_null": True, "allowed_values": ["Drop", "Other", "Presort", "Slip", "Sort", "Unknown"]},
            {"name": 'SScatchFraction',            "dtype": "str", "not_null": True, "allowed_values": ["Catch", "Dis", "Lan"]},
            {"name": 'SSobservationType',          "dtype": "str", "not_null": True, "allowed_values": ["Imagery", "Unknown", "Visual", "Volume"]},
            {"name": 'SSsampler',                  "dtype": "str", "not_null": False, "allowed_values": ["Control", "Imagery", "Observer", "SelfSampling"]},
            {"name": 'SSspeciesListName',          "dtype": "str", "not_null": True},
            {"name": 'SSuseForCalculateZero',      "dtype": "str", "not_null": True, "allowed_values": ["N", "Y"]},
            {"name": 'SStimeTotal',                "dtype": "int", "not_null": False},
            {"name": 'SStimeTotalDataBasis',       "dtype": "str", "not_null": False, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'SStimeSampled',              "dtype": "int", "not_null": False},
            {"name": 'SSnumberTotal',              "dtype": "int", "not_null": False},
            {"name": 'SSnumberTotalDataBasis',     "dtype": "str", "not_null": False, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'SSnumberSampled',            "dtype": "int", "not_null": False},
            {"name": 'SSselectionProb',            "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": 'SSinclusionProb',            "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": 'SSselectionMethod',          "dtype": "str", "not_null": True, "allowed_values": ["CENSUS", "D", "FIXED", "NotApplicable", "NPCLQS-O", "NPCLQS-T", "NPCS", "NPJS", "NPQSRSWOR", "NPQSRSWR", "NPQSYSS", "R", "SRSWOR", "SRSWR", "SYSS", "Unknown", "UPSWOR", "UPSWR"]},
            {"name": 'SSunitName',                 "dtype": "str", "not_null": True},
            {"name": 'SSselectionMethodCluster',   "dtype": "str", "not_null": False, "allowed_values": ["CENSUS", "D", "FIXED", "NotApplicable", "NPCLQS-O", "NPCLQS-T", "NPCS", "NPJS", "NPQSRSWOR", "NPQSRSWR", "NPQSYSS", "R", "SRSWOR", "SRSWR", "SYSS", "Unknown", "UPSWOR", "UPSWR"]},
            {"name": 'SSnumberTotalClusters',      "dtype": "int", "not_null": False},
            {"name": 'SSnumberSampledClusters',    "dtype": "int", "not_null": False},
            {"name": 'SSselectionProbCluster',     "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": 'SSinclusionProbCluster',     "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": 'SSsampled',                  "dtype": "str", "not_null": False, "allowed_values": ["N", "Y"]},
            {"name": 'SSreasonNotSampled',         "dtype": "str", "not_null": False, "allowed_values": ["CameraNotWorking", "CameraViewObstructed", "IndustryDeclined", "NoAnswer", "NoContactDetails", "NotAvailable", "ObserverDeclined", "Other", "OutOfFrame", "PoorImageQuality", "QuotaReached", "Unknown"]},
            {"name": 'SSnonResponseCollected',     "dtype": "str", "not_null": False, "allowed_values": ["N", "Y"]},
            {"name": 'SSauxiliaryVariableTotal',   "dtype": "float", "not_null": False},
            {"name": 'SSauxiliaryVariableValue',   "dtype": "float", "not_null": False},
            {"name": 'SSauxiliaryVariableName',    "dtype": "str", "not_null": False, "allowed_values": [""]},
            {"name": 'SSauxiliaryVariableUnit',    "dtype": "str", "not_null": False, "allowed_values": [""]},
        ]
