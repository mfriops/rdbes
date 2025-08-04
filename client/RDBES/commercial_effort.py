
import pandas as pd

class CommercialEffort:
    CErecordType = 'CE'

    def __init__(self, eff: dict):
        self.CEcommercialEffort = None
        self.CEdataBasisOfScientificEffort = None
        self.CEdataSourceOfScientificEffort = None
        self.CEsamplingScheme = None
        self.CEvesselFlagCountry = None
        self.CEyear = None
        self.CEquarter = None
        self.CEmonth = None
        self.CEArea = None
        self.CEStatisticalRectangle = None
        self.CEdataBasisOfStatisticalRectangle = None
        self.CEdataSourceOfStatisticalRectangle = None
        self.CEfisheriesManagementUnit = None
        self.CEgsaSubarea = None
        self.CEjurisdictionArea = None
        self.CEfishingAreaCategory = None
        self.CEfreshWaterName = None
        self.CEexclusiveEconomicZone = None
        self.CEexclusiveEconomicZoneIndicator = None
        self.CEnationalFishingActivity = None
        self.CEmetier6 = None
        self.CEincidentalByCatchMitigationDevice = None
        self.CElandingLocation = None
        self.CEvesselLengthCategory = None
        self.CEfishingTechnique = None
        self.CEmeshSizeRange = None
        self.CEsupraRegion = None
        self.CEgeoIndicator = None
        self.CEspecificConditionsTechnical = None
        self.CEdeepSeaRegulation = None
        self.CEofficialVesselHoursAtSea = None
        self.CEnumberOfFractionTrips = None
        self.CEnumberOfDominantTrips = None
        self.CEofficialDaysAtSea = None
        self.CEScientificDaysAtSea = None
        self.CEofficialFishingDays = None
        self.CEscientificFishingDays = None
        self.CEofficialNumberOfHaulsOrSets = None
        self.CEScientificNumberOfHaulsOrSets = None
        self.CEofficialVesselFishingHour = None
        self.CEscientificVesselFishingHour = None
        self.CEofficialSoakingMeterHour = None
        self.CEscientificSoakingMeterHour = None
        self.CEofficialkWDaysAtSea = None
        self.CEscientifickWDaysAtSea = None
        self.CEofficialkWFishingDays = None
        self.CEscientifickWFishingDays = None
        self.CEOfficialkWFishingHours = None
        self.CEscientifickWFishingHours = None
        self.CEgTDaysAtSea = None
        self.CEgTFishingDays = None
        self.CEgTFishingHours = None
        self.CEnumberOfUniqueVessels = None
        self.CEgearDimensions = None
        self.CEnumberOfFAD = None
        self.CEnumberofSupVes = None
        self.CEfishingDaysErrorMeasureValueType = None
        self.CEfishingDaystErrorMeasureValueFirst = None
        self.CEfishingDaystErrorMeasureValueSecond = None
        self.CEscientificFishingDaysQualitativeBias = None
        self.CEconfidentialityFlag = None
        self.CEencryptedVesselIds = None

        self.CElabel = None



    def dict(self) -> list:
        ce = {}
        ce['CEcommercialEffort'] = self.CEcommercialEffort
        ce['CErecordType'] = self.CErecordType
        ce['CEdataBasisOfScientificEffort'] = self.CEdataBasisOfScientificEffort
        ce['CEdataSourceOfScientificEffort'] = self.CEdataSourceOfScientificEffort
        ce['CEsamplingScheme'] = self.CEsamplingScheme
        ce['CEvesselFlagCountry'] = self.CEvesselFlagCountry
        ce['CEyear'] = self.CEyear
        ce['CEquarter'] = self.CEquarter
        ce['CEmonth'] = self.CEmonth
        ce['CEArea'] = self.CEArea
        ce['CEStatisticalRectangle'] = self.CEStatisticalRectangle
        ce['CEdataBasisOfStatisticalRectangle'] = self.CEdataBasisOfStatisticalRectangle
        ce['CEdataSourceOfStatisticalRectangle'] = self.CEdataSourceOfStatisticalRectangle
        ce['CEfisheriesManagementUnit'] = self.CEfisheriesManagementUnit
        ce['CEgsaSubarea'] = self.CEgsaSubarea
        ce['CEjurisdictionArea'] = self.CEjurisdictionArea
        ce['CEfishingAreaCategory'] = self.CEfishingAreaCategory
        ce['CEfreshWaterName'] = self.CEfreshWaterName
        ce['CEexclusiveEconomicZone'] = self.CEexclusiveEconomicZone
        ce['CEexclusiveEconomicZoneIndicator'] = self.CEexclusiveEconomicZoneIndicator
        ce['CEnationalFishingActivity'] = self.CEnationalFishingActivity
        ce['CEmetier6'] = self.CEmetier6
        ce['CEincidentalByCatchMitigationDevice'] = self.CEincidentalByCatchMitigationDevice
        ce['CElandingLocation'] = self.CElandingLocation
        ce['CEvesselLengthCategory'] = self.CEvesselLengthCategory
        ce['CEfishingTechnique'] = self.CEfishingTechnique
        ce['CEmeshSizeRange'] = self.CEmeshSizeRange
        ce['CEsupraRegion'] = self.CEsupraRegion
        ce['CEgeoIndicator'] = self.CEgeoIndicator
        ce['CEspecificConditionsTechnical'] = self.CEspecificConditionsTechnical
        ce['CEdeepSeaRegulation'] = self.CEdeepSeaRegulation
        ce['CEofficialVesselHoursAtSea'] = self.CEofficialVesselHoursAtSea
        ce['CEnumberOfFractionTrips'] = self.CEnumberOfFractionTrips
        ce['CEnumberOfDominantTrips'] = self.CEnumberOfDominantTrips
        ce['CEofficialDaysAtSea'] = self.CEofficialDaysAtSea
        ce['CEScientificDaysAtSea'] = self.CEScientificDaysAtSea
        ce['CEofficialFishingDays'] = self.CEofficialFishingDays
        ce['CEscientificFishingDays'] = self.CEscientificFishingDays
        ce['CEofficialNumberOfHaulsOrSets'] = self.CEofficialNumberOfHaulsOrSets
        ce['CEScientificNumberOfHaulsOrSets'] = self.CEScientificNumberOfHaulsOrSets
        ce['CEofficialVesselFishingHour'] = self.CEofficialVesselFishingHour
        ce['CEscientificVesselFishingHour'] = self.CEscientificVesselFishingHour
        ce['CEofficialSoakingMeterHour'] = self.CEofficialSoakingMeterHour
        ce['CEscientificSoakingMeterHour'] = self.CEscientificSoakingMeterHour
        ce['CEofficialkWDaysAtSea'] = self.CEofficialkWDaysAtSea
        ce['CEscientifickWDaysAtSea'] = self.CEscientifickWDaysAtSea
        ce['CEofficialkWFishingDays'] = self.CEofficialkWFishingDays
        ce['CEscientifickWFishingDays'] = self.CEscientifickWFishingDays
        ce['CEOfficialkWFishingHours'] = self.CEOfficialkWFishingHours
        ce['CEscientifickWFishingHours'] = self.CEscientifickWFishingHours
        ce['CEgTDaysAtSea'] = self.CEgTDaysAtSea
        ce['CEgTFishingDays'] = self.CEgTFishingDays
        ce['CEgTFishingHours'] = self.CEgTFishingHours
        ce['CEnumberOfUniqueVessels'] = self.CEnumberOfUniqueVessels
        ce['CEgearDimensions'] = self.CEgearDimensions
        ce['CEnumberOfFAD'] = self.CEnumberOfFAD
        ce['CEnumberofSupVes'] = self.CEnumberofSupVes
        ce['CEfishingDaysErrorMeasureValueType'] = self.CEfishingDaysErrorMeasureValueType
        ce['CEfishingDaystErrorMeasureValueFirst'] = self.CEfishingDaystErrorMeasureValueFirst
        ce['CEfishingDaystErrorMeasureValueSecond'] = self.CEfishingDaystErrorMeasureValueSecond
        ce['CEscientificFishingDaysQualitativeBias'] = self.CEscientificFishingDaysQualitativeBias
        ce['CEconfidentialityFlag'] = self.CEconfidentialityFlag
        ce['CEencryptedVesselIds'] = self.CEencryptedVesselIds
        ce['CElabel'] = self.CElabel
        return ce


    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])


    def validate(self):
        return [
            {"name": 'CEcommercialEffort',                         "dtype": "int", "not_null": False},
            {"name": 'CErecordType',                               "dtype": "str", "not_null": True, "allowed_values": ["CE"]},
            {"name": 'CEdataBasisOfScientificEffort',              "dtype": "str", "not_null": True, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'CEdataSourceOfScientificEffort',             "dtype": "str", "not_null": True, "allowed_values": ["CombOD","Crew","Exprt","HarbLoc","Logb","NotApplicable","Observer","OthDF","PosDat","SalN","SampDC","SampDS","Unknown","VMS"]},
            {"name": 'CEsamplingScheme',                           "dtype": "str", "not_null": False, "allowed_values": ["CE"]},
            {"name": 'CEvesselFlagCountry',                        "dtype": "str", "not_null": True, "allowed_values": ["IS"]},
            {"name": 'CEyear',                                     "dtype": "int", "not_null": True, "range": (1965, 2025)},
            {"name": 'CEquarter',                                  "dtype": "int", "not_null": True, "range": (1, 4)},
            {"name": 'CEmonth',                                    "dtype": "int", "not_null": False, "range": (1, 12)},
            {"name": 'CEArea',                                     "dtype": "str", "not_null": True, "allowed_values": ["CE"]},
            {"name": 'CEStatisticalRectangle',                     "dtype": "str", "not_null": True, "allowed_values": ["CE"]},
            {"name": 'CEdataBasisOfStatisticalRectangle',          "dtype": "str", "not_null": True, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'CEdataSourceOfStatisticalRectangle',         "dtype": "str", "not_null": True, "allowed_values": ["CombOD","Crew","Exprt","HarbLoc","Logb","NotApplicable","Observer","OthDF","PosDat","SalN","SampDC","SampDS","Unknown","VMS"]},
            {"name": 'CEfisheriesManagementUnit',                  "dtype": "str", "not_null": False},
            {"name": 'CEgsaSubarea',                               "dtype": "str", "not_null": True, "allowed_values": ["CE"]},
            {"name": 'CEjurisdictionArea',                         "dtype": "str", "not_null": False, "allowed_values": ["Angola","Canaries","Congo","Gambia","Guineav","Guinea-Bissau","Madeira","Mauritania","Morocco","Senegal","Sierra Leona"]},
            {"name": 'CEfishingAreaCategory',                      "dtype": "str", "not_null": True, "allowed_values": ["BP","BR","BU","C","CE","CF","CR","FW","L","LK","MC","MO","NA","T","TT"]},
            {"name": 'CEfreshWaterName',                           "dtype": "str", "not_null": True, "allowed_values": ["CE"]},
            {"name": 'CEexclusiveEconomicZone',                    "dtype": "str", "not_null": False, "allowed_values": ["CE"]},
            {"name": 'CEexclusiveEconomicZoneIndicator',           "dtype": "str", "not_null": False, "allowed_values": ["COAST","EU","RFMO","UK"]},
            {"name": 'CEnationalFishingActivity',                  "dtype": "str", "not_null": False, "allowed_values": ["CE"]},
            {"name": 'CEmetier6',                                  "dtype": "str", "not_null": True}, # RDBES.Metier
            {"name": 'CEincidentalByCatchMitigationDevice',        "dtype": "str", "not_null": True, "allowed_values": ["CE"]},
            {"name": 'CElandingLocation',                          "dtype": "str", "not_null": True}, # RDBES.Harbour
            {"name": 'CEvesselLengthCategory',                     "dtype": "str", "not_null": True, "allowed_values": ["CE"]},
            {"name": 'CEfishingTechnique',                         "dtype": "str", "not_null": False, "allowed_values": ["CE"]},
            {"name": 'CEmeshSizeRange',                            "dtype": "str", "not_null": False},
            {"name": 'CEsupraRegion',                              "dtype": "str", "not_null": False},
            {"name": 'CEgeoIndicator',                             "dtype": "str", "not_null": False},
            {"name": 'CEspecificConditionsTechnical',              "dtype": "str", "not_null": False},
            {"name": 'CEdeepSeaRegulation',                        "dtype": "str", "not_null": False, "allowed_values": ["CE"]},
            {"name": 'CEofficialVesselHoursAtSea',                 "dtype": "str", "not_null": False, "range": (0.01, 50000)},
            {"name": 'CEnumberOfFractionTrips',                    "dtype": "float", "not_null": True, "range": (0.001, 50000)},
            {"name": 'CEnumberOfDominantTrips',                    "dtype": "int", "not_null": True, "range": (0, 50000)},
            {"name": 'CEofficialDaysAtSea',                        "dtype": "float", "not_null": True, "range": (0.01, 25000)},
            {"name": 'CEScientificDaysAtSea',                      "dtype": "float", "not_null": True, "range": (0.01, 25000)},
            {"name": 'CEofficialFishingDays',                      "dtype": "float", "not_null": True, "range": (0.01, 25000)},
            {"name": 'CEscientificFishingDays',                    "dtype": "float", "not_null": True, "range": (0.01, 25000)},
            {"name": 'CEofficialNumberOfHaulsOrSets',              "dtype": "int", "not_null": False, "range": (1, 250000)},
            {"name": 'CEScientificNumberOfHaulsOrSets',            "dtype": "int", "not_null": False, "range": (1, 250000)},
            {"name": 'CEofficialVesselFishingHour',                "dtype": "float", "not_null": False, "range": (0.01, 1200000)},
            {"name": 'CEscientificVesselFishingHour',              "dtype": "float", "not_null": False, "range": (0.01, 1200000)},
            {"name": 'CEofficialSoakingMeterHour',                 "dtype": "float", "not_null": False, "range": (0.01, 10000000)},
            {"name": 'CEscientificSoakingMeterHour',               "dtype": "float", "not_null": False, "range": (0.01, 10000000)},
            {"name": 'CEofficialkWDaysAtSea',                      "dtype": "int", "not_null": True, "range": (0, 2500000)},
            {"name": 'CEscientifickWDaysAtSea',                    "dtype": "int", "not_null": True, "range": (0, 2500000)},
            {"name": 'CEofficialkWFishingDays',                    "dtype": "int", "not_null": True, "range": (0, 2500000)},
            {"name": 'CEscientifickWFishingDays',                  "dtype": "int", "not_null": True, "range": (0, 2500000)},
            {"name": 'CEOfficialkWFishingHours',                   "dtype": "int", "not_null": False, "range": (0, 25000000)},
            {"name": 'CEscientifickWFishingHours',                 "dtype": "int", "not_null": False, "range": (0, 25000000)},
            {"name": 'CEgTDaysAtSea',                              "dtype": "int", "not_null": True, "range": (0, 25000000)},
            {"name": 'CEgTFishingDays',                            "dtype": "int", "not_null": True, "range": (0, 25000000)},
            {"name": 'CEgTFishingHours',                           "dtype": "int", "not_null": False, "range": (0, 100000000000)},
            {"name": 'CEnumberOfUniqueVessels',                    "dtype": "int", "not_null": True, "range": (0, 100000000)},
            {"name": 'CEgearDimensions',                           "dtype": "int", "not_null": False, "range": (0, 1000000)},
            {"name": 'CEnumberOfFAD',                              "dtype": "int", "not_null": False, "range": (0, 999)},
            {"name": 'CEnumberofSupVes',                           "dtype": "int", "not_null": False, "range": (0, 999)},
            {"name": 'CEfishingDaysErrorMeasureValueType',         "dtype": "str", "not_null": False, "allowed_values": ["CE"]},
            {"name": 'CEfishingDaystErrorMeasureValueFirst',       "dtype": "float", "not_null": False, "range": (0.000001, 999)},
            {"name": 'CEfishingDaystErrorMeasureValueSecond',      "dtype": "float", "not_null": False, "range": (0.000001, 999)},
            {"name": 'CEscientificFishingDaysQualitativeBias',     "dtype": "str", "not_null": False, "allowed_values": ["CE"]},
            {"name": 'CEconfidentialityFlag',                      "dtype": "str", "not_null": True, "allowed_values": ["CE"]},
            {"name": 'CEencryptedVesselIds',                       "dtype": "str", "not_null": True},

            {"name": 'CElabel',                                    "dtype": "str", "not_null": False},
        ]
