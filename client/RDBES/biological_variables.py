
import pandas as pd

class BiologicalVariables:
    BVrecordType = 'BV'

    def __init__(self, meas: dict, meas_type: str):
        self.BVid = None
        self.SAid = meas['sample_id']
        self.FMid = None
        self.BVnationalUniqueFishId = meas['measure_id']
        self.BVstateOfProcessing = 'DEF'
        self.BVpresentation = 'WHL'
        self.BVstratification = 'N'
        self.BVstratumName = 'U'
        self.BVtypeMeasured = meas_type
        self.BVvalueMeasured = meas['measure']
        self.BVvalueUnitOrScale = meas['measure_unit']
        self.BVspecimenType = meas['specimen_type']
        self.BVanalysisType = None
        self.BVaccuracy = None
        self.BVcertaintyQualitative = 'Unknown'
        self.BVcertaintyQuantitative = None
        self.BVconversionFactorAssessment = 1
        self.BVtypeAssessment = meas_type
        self.BVnumberTotal = meas['tot_count']
        self.BVnumberSampled = meas['grp_count'] if meas_type in ('WeightMeasured', 'Age') else None
        self.BVselectionProb = None
        self.BVinclusionProb = None
        self.BVselectionMethod = 'Unknown'
        self.BVunitName = None
        self.BVsampler = None


    def dict(self) -> dict:
        bv = {}
        bv['BVid'] = self.BVid
        bv['SAid'] = self.SAid
        bv['FMid'] = self.FMid
        bv['BVrecordType'] = self.BVrecordType
        bv['BVnationalUniqueFishId'] = self.BVnationalUniqueFishId
        bv['BVstateOfProcessing'] = self.BVstateOfProcessing
        bv['BVpresentation'] = self.BVpresentation
        bv['BVstratification'] = self.BVstratification
        bv['BVstratumName'] = self.BVstratumName
        bv['BVtypeMeasured'] = self.BVtypeMeasured
        bv['BVvalueMeasured'] = self.BVvalueMeasured
        bv['BVvalueUnitOrScale'] = self.BVvalueUnitOrScale
        bv['BVspecimenType'] = self.BVspecimenType
        bv['BVanalysisType'] = self.BVanalysisType
        bv['BVaccuracy'] = self.BVaccuracy
        bv['BVcertaintyQualitative'] = self.BVcertaintyQualitative
        bv['BVcertaintyQuantitative'] = self.BVcertaintyQuantitative
        bv['BVconversionFactorAssessment'] = self.BVconversionFactorAssessment
        bv['BVtypeAssessment'] = self.BVtypeAssessment
        bv['BVnumberTotal'] = self.BVnumberTotal
        bv['BVnumberSampled'] = self.BVnumberSampled
        bv['BVselectionProb'] = self.BVselectionProb
        bv['BVinclusionProb'] = self.BVinclusionProb
        bv['BVselectionMethod'] = self.BVselectionMethod
        bv['BVunitName'] = self.BVunitName
        bv['BVsampler'] = self.BVsampler
        return bv

    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])


    def validate(self):
        return [
            {"name": 'BVid',                           "dtype": "int",    "not_null": False},
            {"name": 'SAid',                           "dtype": "int",    "not_null": False},
            {"name": 'FMid',                           "dtype": "int",    "not_null": False},
            {"name": 'BVrecordType',                   "dtype": "str",    "not_null": True, "allowed_values": ["BV"]},
            {"name": 'BVnationalUniqueFishId',         "dtype": "str",    "not_null": True},
            {"name": 'BVstateOfProcessing',            "dtype": "str",    "not_null": True, "allowed_values": ["BAF","BOI","DEF","DRI","FRE","FRO","SAD","SAL","SMO","UNK"]},
            {"name": 'BVpresentation',                 "dtype": "str",    "not_null": True, "allowed_values": ["CBF","CLA","DWT","FBS","FIL","FIS","FSP","GHT","GUG","GUH","GUL","GUN","GUS","GUT","HEA","JAP","JAT","LAP","LVR","OTH","ROE","SKI","SUR","TAL","TLD","TNG","TUB","Unknown","WHL","WNG"]},
            {"name": 'BVstratification',               "dtype": "str",    "not_null": True, "allowed_values": ["N","Y"]},
            {"name": 'BVstratumName',                  "dtype": "str",    "not_null": True},
            {"name": 'BVtypeMeasured',                 "dtype": "str",    "not_null": True, "allowed_values": ["Age", "Berried", "ForkLength", "GeneticPopulation", "HatchSeason", "IlliciumCollected", "InfoConversionFactor", "InfoGenetic", "InfoGonad", "InfoLiver", "InfoOtolithMorphometrics", "InfoParasite", "InfoStomach", "InfoTagging", "LengthCarapace", "LengthLowerJawFork", "LengthMantle", "LengthMaximumShell", "LengthPinchedTail", "LengthPreAnal", "LengthPreCaudal", "LengthStandard", "LengthTail", "LengthTotal", "LengthWingSpan", "Maturity", "OtolithCollected", "ScaleCollected", "Sex", "SpecimenState", "Stock", "VertebraCount", "WeightGutted", "WeightLive", "WeightMeasured", "WidthCarapace", "WidthMaximumShell"]},
            {"name": 'BVvalueMeasured',                "dtype": "str",    "not_null": True},
            {"name": 'BVvalueUnitOrScale',             "dtype": "str",    "not_null": True, "allowed_values": ["Agewr","Ageyear","Lengthmm","NotApplicable","Sex","SMSF","Weightg"]},
            {"name": 'BVspecimenType',                 "dtype": "str",    "not_null": False, "allowed_values": ["otolith", "scale"]},
            {"name": 'BVanalysisType',                 "dtype": "str",    "not_null": False, "allowed_values": ["?"]},
            {"name": 'BVaccuracy',                     "dtype": "str",    "not_null": False, "allowed_values": ["100g", "10g", "25mm", "500g", "5cm", "cm", "g", "kg", "mm", "NotApplicable", "scm", "smm", "year"]},
            {"name": 'BVcertaintyQualitative',         "dtype": "str",    "not_null": True, "allowed_values": ["AQ1","AQ2","AQ3","AQ3_QA","NotApplicable","QS1","QS2","QS3","QS3_QA","Unknown"]},
            {"name": 'BVcertaintyQuantitative',        "dtype": "float",  "not_null": False, "range": (0.001, 1)},
            {"name": 'BVconversionFactorAssessment',   "dtype": "float", "not_null": True, "range": (0.1001, 10)},
            {"name": 'BVtypeAssessment',               "dtype": "str",    "not_null": True, "allowed_values": ["Age", "Berried", "ForkLength", "GeneticPopulation", "HatchSeason", "IlliciumCollected", "InfoConversionFactor", "InfoGenetic", "InfoGonad", "InfoLiver", "InfoOtolithMorphometrics", "InfoParasite", "InfoStomach", "InfoTagging", "LengthCarapace", "LengthLowerJawFork", "LengthMantle", "LengthMaximumShell", "LengthPinchedTail", "LengthPreAnal", "LengthPreCaudal", "LengthStandard", "LengthTail", "LengthTotal", "LengthWingSpan", "Maturity", "OtolithCollected", "ScaleCollected", "Sex", "SpecimenState", "Stock", "VertebraCount", "WeightGutted", "WeightLive", "WeightMeasured", "WidthCarapace", "WidthMaximumShell"]},
            {"name": 'BVnumberTotal',                  "dtype": "int",    "not_null": False},
            {"name": 'BVnumberSampled',                "dtype": "int",    "not_null": False},
            {"name": 'BVselectionProb',                "dtype": "float",  "not_null": False, "range": (0, 1)},
            {"name": 'BVinclusionProb',                "dtype": "float",  "not_null": False, "range": (0, 1)},
            {"name": 'BVselectionMethod',              "dtype": "str",    "not_null": True, "allowed_values": ["CENSUS", "D", "FIXED", "NotApplicable", "NPCLQS-O", "NPCLQS-T", "NPCS", "NPJS", "NPQSRSWOR", "NPQSRSWR", "NPQSYSS", "R", "SRSWOR", "SRSWR", "SYSS", "Unknown", "UPSWOR", "UPSWR"]},
            {"name": 'BVunitName',                     "dtype": "str",    "not_null": True},
            {"name": 'BVsampler',                      "dtype": "str",    "not_null": False, "allowed_values": ["Control", "Imagery", "Observer", "SelfSampling"]},
        ]

