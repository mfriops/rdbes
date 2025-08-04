
import pandas as pd

class FishingTrip:
    FTrecordType = 'FT'

    def __init__(self, sample):
        self.FTid = sample['fishing_trip_id']
        self.OSid = None
        self.VSid = None
        self.VDid = None
        self.SDid = None
        self.FOid = None
        self.TEid = None
        self.FTencryptedVesselCode = sample['vessel_id']
        self.FTsequenceNumber = None
        self.FTstratification = 'N'
        self.FTstratumName = 'U'
        self.FTclustering = 'N'
        self.FTclusterName = 'U'
        self.FTsampler = 'SelfSampling'
        self.FTsamplingType = 'AtSea'
        self.FTnumberOfHaulsOrSets = None
        self.FTdepartureLocation = sample['departure_harbour']
        self.FTdepartureDate = sample['departure'][:10] if sample['departure'] != None else None
        self.FTdepartureTime = sample['departure'][:11:16] if sample['departure'] != None else None
        self.FTarrivalLocation = sample['landing_harbour']
        self.FTarrivalDate = sample['arrival'][:10] if sample['arrival'] != None else None
        self.FTarrivalTime = sample['arrival'][11:16] if sample['arrival'] != None else None
        self.FTdominantLandingDate = None
        self.FTnumberTotal = None
        self.FTnumberSampled = None
        self.FTselectionProb = None
        self.FTinclusionProb = None
        self.FTselectionMethod = 'NotApplicable'
        self.FTunitName = sample['fishing_trip_id']
        self.FTselectionMethodCluster = None
        self.FTnumberTotalClusters = None
        self.FTnumberSampledClusters = None
        self.FTselectionProbCluster = None
        self.FTinclusionProbCluster = None
        self.FTsampled = 'Y'
        self.FTreasonNotSampled = None
        self.FTnonResponseCollected = None
        self.FTauxiliaryVariableTotal = None
        self.FTauxiliaryVariableValue = None
        self.FTauxiliaryVariableName = None
        self.FTauxiliaryVariableUnit = None


    def dict(self) -> dict:
        ft = {}
        ft['FTid'] = self.FTid
        ft['OSid'] = self.OSid
        ft['VSid'] = self.VSid
        ft['VDid'] = self.VDid
        ft['SDid'] = self.SDid
        ft['FOid'] = self.FOid
        ft['TEid'] = self.TEid
        ft['FTrecordType'] = self.FTrecordType
        ft['FTencryptedVesselCode'] = self.FTencryptedVesselCode
        ft['FTsequenceNumber'] = self.FTsequenceNumber
        ft['FTstratification'] = self.FTstratification
        ft['FTstratumName'] = self.FTstratumName
        ft['FTclustering'] = self.FTclustering
        ft['FTclusterName'] = self.FTclusterName
        ft['FTsampler'] = self.FTsampler
        ft['FTsamplingType'] = self.FTsamplingType
        ft['FTnumberOfHaulsOrSets'] = self.FTnumberOfHaulsOrSets
        ft['FTdepartureLocation'] = self.FTdepartureLocation
        ft['FTdepartureDate'] = self.FTdepartureDate
        ft['FTdepartureTime'] = self.FTdepartureTime
        ft['FTarrivalLocation'] = self.FTarrivalLocation
        ft['FTarrivalDate'] = self.FTarrivalDate
        ft['FTarrivalTime'] = self.FTarrivalTime
        ft['FTdominantLandingDate'] = self.FTdominantLandingDate
        ft['FTnumberTotal'] = self.FTnumberTotal
        ft['FTnumberSampled'] = self.FTnumberSampled
        ft['FTselectionProb'] = self.FTselectionProb
        ft['FTinclusionProb'] = self.FTinclusionProb
        ft['FTselectionMethod'] = self.FTselectionMethod
        ft['FTunitName'] = self.FTunitName
        ft['FTselectionMethodCluster'] = self.FTselectionMethodCluster
        ft['FTnumberTotalClusters'] = self.FTnumberTotalClusters
        ft['FTnumberSampledClusters'] = self.FTnumberSampledClusters
        ft['FTselectionProbCluster'] = self.FTselectionProbCluster
        ft['FTinclusionProbCluster'] = self.FTinclusionProbCluster
        ft['FTsampled'] = self.FTsampled
        ft['FTreasonNotSampled'] = self.FTreasonNotSampled
        ft['FTnonResponseCollected'] = self.FTnonResponseCollected
        ft['FTauxiliaryVariableTotal'] = self.FTauxiliaryVariableTotal
        ft['FTauxiliaryVariableValue'] = self.FTauxiliaryVariableValue
        ft['FTauxiliaryVariableName'] = self.FTauxiliaryVariableName
        ft['FTauxiliaryVariableUnit'] = self.FTauxiliaryVariableUnit
        return ft

    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])


    def validate(self):
        return [
            {"name": "FTid",                        "dtype": "str", "not_null": False},
            {"name": "OSid",                        "dtype": "int", "not_null": False},
            {"name": "VSid",                        "dtype": "int", "not_null": False},
            {"name": "VDid",                        "dtype": "int", "not_null": False},
            {"name": "SDid",                        "dtype": "int", "not_null": False},
            {"name": "FOid",                        "dtype": "int", "not_null": False},
            {"name": "TEid",                        "dtype": "int", "not_null": False},
            {"name": "FTrecordType",                "dtype": "str", "not_null": True, "allowed_values": ["FT"]},
            {"name": "FTencryptedVesselCode",       "dtype": "str", "not_null": True},
            {"name": "FTsequenceNumber",            "dtype": "int", "not_null": True},
            {"name": "FTstratification",            "dtype": "str", "not_null": True, "allowed_values": ["N", "Y"]},
            {"name": "FTstratumName",               "dtype": "str", "not_null": True},
            {"name": "FTclustering",                "dtype": "str", "not_null": True, "allowed_values": ["1C", "1CS", "2C", "2CS", "N", "S1C", "S2C"]},
            {"name": "FTclusterName",               "dtype": "str", "not_null": True},
            {"name": "FTsampler",                   "dtype": "str", "not_null": False, "allowed_values": ["Control", "Imagery", "Observer", "SelfSampling"]},
            {"name": "FTsamplingType",              "dtype": "str", "not_null": True, "allowed_values": ["AtSea","OnShore"]},
            {"name": "FTnumberOfHaulsOrSets",       "dtype": "int", "not_null": False, "range": (1, 300)},
            {"name": "FTdepartureLocation",         "dtype": "str", "not_null": False, }, # RDBES.Harbour
            {"name": "FTdepartureDate",             "dtype": "str", "not_null": False},
            {"name": "FTdepartureTime",             "dtype": "str", "not_null": False},
            {"name": "FTarrivalLocation",           "dtype": "str", "not_null": True}, # RDBES.Harbour
            {"name": "FTarrivalDate",               "dtype": "str", "not_null": True},
            {"name": "FTarrivalTime",               "dtype": "str", "not_null": False},
            {"name": "FTdominantLandingDate",       "dtype": "str", "not_null": False},
            {"name": "FTnumberTotal",               "dtype": "int", "not_null": False},
            {"name": "FTnumberSampled",             "dtype": "int", "not_null": False},
            {"name": "FTselectionProb",             "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": "FTinclusionProb",             "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": "FTselectionMethod",           "dtype": "str", "not_null": True, "allowed_values": ["CENSUS", "D", "FIXED", "NotApplicable", "NPCLQS-O", "NPCLQS-T", "NPCS", "NPJS", "NPQSRSWOR", "NPQSRSWR", "NPQSYSS", "R", "SRSWOR", "SRSWR", "SYSS", "Unknown", "UPSWOR", "UPSWR"]},
            {"name": "FTunitName",                  "dtype": "str", "not_null": True},
            {"name": "FTselectionMethodCluster",    "dtype": "str", "not_null": False, "allowed_values": ["CENSUS", "D", "FIXED", "NotApplicable", "NPCLQS-O", "NPCLQS-T", "NPCS", "NPJS", "NPQSRSWOR", "NPQSRSWR", "NPQSYSS", "R", "SRSWOR", "SRSWR", "SYSS", "Unknown", "UPSWOR", "UPSWR"]},
            {"name": "FTnumberTotalClusters",       "dtype": "int", "not_null": False},
            {"name": "FTnumberSampledClusters",     "dtype": "int", "not_null": False},
            {"name": "FTselectionProbCluster",      "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": "FTinclusionProbCluster",      "dtype": "float", "not_null": False, "range": (0, 1)},
            {"name": "FTsampled",                   "dtype": "str", "not_null": True, "allowed_values": ["N","Y"]},
            {"name": "FTreasonNotSampled",          "dtype": "str", "not_null": False, "allowed_values": ["CameraNotWorking", "CameraViewObstructed", "IndustryDeclined", "NoAnswer", "NoContactDetails", "NotAvailable", "ObserverDeclined", "Other", "OutOfFrame", "PoorImageQuality", "QuotaReached", "Unknown"]},
            {"name": "FTnonResponseCollected",      "dtype": "str", "not_null": False, "allowed_values": ["N","Y"]},
            {"name": "FTauxiliaryVariableTotal",    "dtype": "float", "not_null": False},
            {"name": "FTauxiliaryVariableValue",    "dtype": "float", "not_null": False},
            {"name": "FTauxiliaryVariableName",     "dtype": "str", "not_null": False},
            {"name": "FTauxiliaryVariableUnit",     "dtype": "str", "not_null": False},
        ]

