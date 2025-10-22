#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class Sample:
    SArecordType = 'SA'

    def __init__(self, sample: dict | None = None):

        """Initialize from a sample dict, or create an empty instance."""
        if sample is None:
            # create an empty instance (all attributes None)
            for spec in self.validate():
                setattr(self, spec["name"], None)
            return

        self.SAid = sample['sample_id']
        self.SSid = sample['sample_id']
        self.SAsequenceNumber = sample['sequence']
        self.SAparentSequenceNumber = None
        self.SAstratification = 'N'
        self.SAstratumName = 'U'
        self.SAspeciesCode = sample['worms_id']
        self.SAspeciesCodeFAO = None
        self.SAstateOfProcessing = 'DEF'
        self.SApresentation = 'WHL'
        self.SAspecimensState = 'Unknown'
        self.SAcatchCategory = 'Catch'
        self.SAlandingCategory = None
        self.SAcommSizeCatScale = None
        self.SAcommSizeCat = None
        self.SAsex = 'U'   #self.get_sex(sample['sex_no'])
        self.SAexclusiveEconomicZoneIndicator = None
        self.SAarea = None
        self.SArectangle = None
        self.SAfisheriesManagementUnit = None
        self.SAgsaSubarea = 'NotApplicable'
        self.SAjurisdictionArea = None
        self.SAgeographicalDataBasis = None
        self.SAgeographicalSource = None
        self.SAnationalFishingActivity = None
        self.SAmetier5 = None
        self.SAmetier6 = None
        self.SAgear = None
        self.SAgearDataBasis = None
        self.SAgearSource = None
        self.SAmeshSize = None
        self.SAselectionDevice = None
        self.SAselectionDeviceMeshSize = None
        self.SAunitType = 'Box'
        self.SAtotalWeightLive = None
        self.SAsampleWeightLive = None
        self.SAnumberTotal = None
        self.SAnumberSampled = None
        self.SAselectionProb = None
        self.SAinclusionProb = None
        self.SAselectionMethod = 'NPJS'
        self.SAunitName = sample['sample_id']
        self.SAlowerHierarchy = 'C'
        self.SAsampler = 'SelfSampling'
        self.SAsampled = 'Y'
        self.SAreasonNotSampled = None
        self.SAnonResponseCollected = None
        self.SAreasonNotSampledFM = None
        self.SAreasonNotSampledBV = None
        self.SAtotalWeightMeasured = None
        self.SAtotalWeightMeasuredDataBasis = None
        self.SAsampleWeightMeasured = None
        self.SAconversionFactorMeasLive = None
        self.SAauxiliaryVariableTotal = None
        self.SAauxiliaryVariableValue = None
        self.SAauxiliaryVariableName = None
        self.SAauxiliaryVariableUnit = None

    def dict(self) -> dict:
        sa = {}
        sa['SAid']= self.SAid
        sa['SSid']= self.SSid
        sa['SArecordType']= self.SArecordType
        sa['SAsequenceNumber']= self.SAsequenceNumber
        sa['SAparentSequenceNumber']= self.SAparentSequenceNumber
        sa['SAstratification']= self.SAstratification
        sa['SAstratumName']= self.SAstratumName
        sa['SAspeciesCode']= self.SAspeciesCode
        sa['SAspeciesCodeFAO']= self.SAspeciesCodeFAO
        sa['SAstateOfProcessing']= self.SAstateOfProcessing
        sa['SApresentation']= self.SApresentation
        sa['SAspecimensState']= self.SAspecimensState
        sa['SAcatchCategory']= self.SAcatchCategory
        sa['SAlandingCategory']= self.SAlandingCategory
        sa['SAcommSizeCatScale']= self.SAcommSizeCatScale
        sa['SAcommSizeCat']= self.SAcommSizeCat
        sa['SAsex']= self.SAsex
        sa['SAexclusiveEconomicZoneIndicator']= self.SAexclusiveEconomicZoneIndicator
        sa['SAarea']= self.SAarea
        sa['SArectangle']= self.SArectangle
        sa['SAfisheriesManagementUnit']= self.SAfisheriesManagementUnit
        sa['SAgsaSubarea']= self.SAgsaSubarea
        sa['SAjurisdictionArea']= self.SAjurisdictionArea
        sa['SAgeographicalDataBasis']= self.SAgeographicalDataBasis
        sa['SAgeographicalSource']= self.SAgeographicalSource
        sa['SAnationalFishingActivity']= self.SAnationalFishingActivity
        sa['SAmetier5']= self.SAmetier5
        sa['SAmetier6']= self.SAmetier6
        sa['SAgear']= self.SAgear
        sa['SAgearDataBasis']= self.SAgearDataBasis
        sa['SAgearSource']= self.SAgearSource
        sa['SAmeshSize']= self.SAmeshSize
        sa['SAselectionDevice']= self.SAselectionDevice
        sa['SAselectionDeviceMeshSize']= self.SAselectionDeviceMeshSize
        sa['SAunitType']= self.SAunitType
        sa['SAtotalWeightLive']= self.SAtotalWeightLive
        sa['SAsampleWeightLive']= self.SAsampleWeightLive
        sa['SAnumberTotal']= self.SAnumberTotal
        sa['SAnumberSampled']= self.SAnumberSampled
        sa['SAselectionProb']= self.SAselectionProb
        sa['SAinclusionProb']= self.SAinclusionProb
        sa['SAselectionMethod']= self.SAselectionMethod
        sa['SAunitName']= self.SAunitName
        sa['SAlowerHierarchy']= self.SAlowerHierarchy
        sa['SAsampler']= self.SAsampler
        sa['SAsampled']= self.SAsampled
        sa['SAreasonNotSampled']= self.SAreasonNotSampled
        sa['SAnonResponseCollected']= self.SAnonResponseCollected
        sa['SAreasonNotSampledFM']= self.SAreasonNotSampledFM
        sa['SAreasonNotSampledBV']= self.SAreasonNotSampledBV
        sa['SAtotalWeightMeasured']= self.SAtotalWeightMeasured
        sa['SAtotalWeightMeasuredDataBasis']= self.SAtotalWeightMeasuredDataBasis
        sa['SAsampleWeightMeasured']= self.SAsampleWeightMeasured
        sa['SAconversionFactorMeasLive']= self.SAconversionFactorMeasLive
        sa['SAauxiliaryVariableTotal']= self.SAauxiliaryVariableTotal
        sa['SAauxiliaryVariableValue']= self.SAauxiliaryVariableValue
        sa['SAauxiliaryVariableName']= self.SAauxiliaryVariableName
        sa['SAauxiliaryVariableUnit']= self.SAauxiliaryVariableUnit
        return sa

    def columns(self) -> list[str]:
        """Return all column names in the same order as dict()."""
        return list(map(str.lower, self.dict().keys()))

    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])

    def get_sex(self, sex_no):
        if sex_no == None:
            return 'Undetermined'
        elif sex_no == 1:
            return 'Male'
        elif sex_no == 2:
            return 'Female'

    def validate(self):
        return [
            {"name": 'SAid',                               "dtype": "int", "not_null": False},
            {"name": 'SSid',                               "dtype": "int", "not_null": False},
            {"name": 'SArecordType',                       "dtype": "str", "not_null": True, "allowed_values": ["SA"]},
            {"name": 'SAsequenceNumber',                   "dtype": "int", "not_null": True},
            {"name": 'SAparentSequenceNumber',             "dtype": "int", "not_null": False},
            {"name": 'SAstratification',                   "dtype": "str", "not_null": True, "allowed_values": ["N","Y"]},
            {"name": 'SAstratumName',                      "dtype": "str", "not_null": True},
            {"name": 'SAspeciesCode',                      "dtype": "str", "not_null": True}, # Worms
            {"name": 'SAspeciesCodeFAO',                   "dtype": "str", "not_null": False},
            {"name": 'SAstateOfProcessing',                "dtype": "str", "not_null": True, "allowed_values": ["BAF", "BOI", "DEF", "DRI", "FRE", "FRO", "SAD", "SAL", "SMO", "UNK"]},
            {"name": 'SApresentation',                     "dtype": "str", "not_null": True, "allowed_values": ["CBF", "CBF", "CLA", "DWT", "FBS", "FIL", "FIS", "FSP", "GHT", "GUG", "GUH", "GUL", "GUN", "GUS", "GUT", "HEA", "JAP", "JAT", "LAT", "LAP", "LVR", "OTH", "ROE", "SKI", "SUR", "TAL", "TLD", "TNG", "TUB", "Unknown", "WHL", "WNG"]},
            {"name": 'SAspecimensState',                   "dtype": "str", "not_null": True, "allowed_values": ["AliveHighProbSurvival","AliveLowProbSurvival","DeadOrZeroProbSurvival","Decomposed","Mixed","NotDetermined","Predated","Unknown"]},
            {"name": 'SAcatchCategory',                    "dtype": "str", "not_null": True, "allowed_values": ["BMS","Catch","Dis","Lan","RegDis"]},
            {"name": 'SAlandingCategory',                  "dtype": "str", "not_null": False, "allowed_values": ["HuC","HuCInd","Ind","None"]},
            {"name": 'SAcommSizeCatScale',                 "dtype": "str", "not_null": False, "allowed_values": ["BEL cod","BEL lemon sole","BEL plaice","BEL sole","English","ES-AZTI","ES-IEO","EU","NLD","PT-IPMA","SCT fish sorting","SCT Nephrops sorting","Unsorted"]},
            {"name": 'SAcommSizeCat',                      "dtype": "str", "not_null": False, "allowed_values": ["?"]},
            {"name": 'SAsex',                              "dtype": "str", "not_null": True, "allowed_values": ["F","H","I","M","T","U","X"]},
            {"name": 'SAexclusiveEconomicZoneIndicator',   "dtype": "str", "not_null": False, "allowed_values": ["?"]}, #HINT/ath
            {"name": 'SAarea',                             "dtype": "str", "not_null": False, "allowed_values": ["?"]},
            {"name": 'SArectangle',                        "dtype": "str", "not_null": False, "allowed_values": ["?"]},
            {"name": 'SAfisheriesManagementUnit',          "dtype": "str", "not_null": False},
            {"name": 'SAgsaSubarea',                       "dtype": "str", "not_null": True, "allowed_values": ["1","10","11.1", "11.2", "12", "13", "14", "15", "16", "17", "18", "19", "2", "20", "21", "22", "23", "24","25", "26", "27", "28", "29", "3", "30", "4", "5", "6", "7", "8", "9", "NotApplicable"]},
            {"name": 'SAjurisdictionArea',                 "dtype": "str", "not_null": False, "allowed_values": ["Angola","Canaries","Congo","Gambia","Guineav","Guinea-Bissau","Madeira","Mauritania","Morocco","Senegal","Sierra Leona"]},
            {"name": 'SAgeographicalDataBasis',            "dtype": "str", "not_null": False, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'SAgeographicalSource',               "dtype": "str", "not_null": False, "allowed_values": ["CombOD","Crew","Exprt","HarbLoc","Logb","NotApplicable","Observer","OthDF","PosDat","SalN","SampDC","SampDS","Unknown","VMS"]},
            {"name": 'SAnationalFishingActivity',          "dtype": "str", "not_null": False, "allowed_values": ["?"]},
            {"name": 'SAmetier5',                          "dtype": "str", "not_null": False, "allowed_values": ["?"]},
            {"name": 'SAmetier6',                          "dtype": "str", "not_null": False}, # RDBES.Metier
            {"name": 'SAgear',                             "dtype": "str", "not_null": False, "allowed_values": ["FPN","FPO","FWR","FYK","GEL","GN","GNC","GND","GNS","GTN","GTR","HMD","LA","LH","LHM","LHP","LLD","LLS","LTL","LX","MIS","OTB","OTM","OTT","PS	","PTB","PTM","SB","SBV","SDN","SPR","SSC","TBB"]},
            {"name": 'SAgearDataBasis',                    "dtype": "str", "not_null": False, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'SAgearSource',                       "dtype": "str", "not_null": False, "allowed_values": ["CombOD","Crew","Exprt","HarbLoc","Logb","NotApplicable","Observer","OthDF","PosDat","SalN","SampDC","SampDS","Unknown","VMS"]},
            {"name": 'SAmeshSize',                         "dtype": "int", "not_null": False},
            {"name": 'SAselectionDevice',                  "dtype": "int", "not_null": False, "allowed_values": ["0","1","2","3","4"]},
            {"name": 'SAselectionDeviceMeshSize',          "dtype": "int", "not_null": False},
            {"name": 'SAunitType',                         "dtype": "str", "not_null": True, "allowed_values": ["Basket",'Box','Container','Haul','Individuals','Minutes','Number','Tray','Weight']},
            {"name": 'SAtotalWeightLive',                  "dtype": "int", "not_null": False},
            {"name": 'SAsampleWeightLive',                 "dtype": "int", "not_null": False},
            {"name": 'SAnumberTotal',                      "dtype": "float", "not_null": False, "range": (0.1, 999999999)},
            {"name": 'SAnumberSampled',                    "dtype": "float", "not_null": False, "range": (0.1, 999999999)},
            {"name": 'SAselectionProb',                    "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": 'SAinclusionProb',                    "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": 'SAselectionMethod',                  "dtype": "str", "not_null": True, "allowed_values": ["CENSUS", "D", "FIXED", "NotApplicable", "NPCLQS-O", "NPCLQS-T", "NPCS", "NPJS", "NPQSRSWOR", "NPQSRSWR", "NPQSYSS", "R", "SRSWOR", "SRSWR", "SYSS", "Unknown", "UPSWOR", "UPSWR"]},
            {"name": 'SAunitName',                         "dtype": "str", "not_null": True},
            {"name": 'SAlowerHierarchy',                   "dtype": "str", "not_null": False, "allowed_values": ["A", "B", "C", "D"]},
            {"name": 'SAsampler',                          "dtype": "str", "not_null": False, "allowed_values": ["Control", "Imagery", "Observer", "SelfSampling"]},
            {"name": 'SAsampled',                          "dtype": "str", "not_null": True, "allowed_values": ["N", "Y"]},
            {"name": 'SAreasonNotSampled',                 "dtype": "str", "not_null": False, "allowed_values": ["CameraNotWorking", "CameraViewObstructed", "IndustryDeclined", "NoAnswer", "NoContactDetails", "NotAvailable", "ObserverDeclined", "Other", "OutOfFrame", "PoorImageQuality", "QuotaReached", "Unknown"]},
            {"name": 'SAnonResponseCollected',             "dtype": "str", "not_null": False, "allowed_values": ["N","Y"]},
            {"name": 'SAreasonNotSampledFM',               "dtype": "str", "not_null": False},
            {"name": 'SAreasonNotSampledBV',               "dtype": "str", "not_null": False},
            {"name": 'SAtotalWeightMeasured',              "dtype": "int", "not_null": False},
            {"name": 'SAtotalWeightMeasuredDataBasis',     "dtype": "str", "not_null": False, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'SAsampleWeightMeasured',             "dtype": "int", "not_null": False},
            {"name": 'SAconversionFactorMeasLive',         "dtype": "float", "not_null": False, "range": (0.900, 10)},
            {"name": 'SAauxiliaryVariableTotal',           "dtype": "float", "not_null": False},
            {"name": 'SAauxiliaryVariableValue',           "dtype": "float", "not_null": False},
            {"name": 'SAauxiliaryVariableName',            "dtype": "str", "not_null": False},
            {"name": 'SAauxiliaryVariableUnit',            "dtype": "str", "not_null": False},
        ]
