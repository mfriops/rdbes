
import pandas as pd

class CommercialLanding:
    CLrecordType = 'CL'

    def __init__(self, land: dict):
        self.CLcommercialLanding = None
        self.CLdataBasisOfScientificWeight = None
        self.CLdataSourceOfScientificWeight = None
        self.CLsamplingScheme = None
        self.CLdataSourceLandingsValue = None
        self.CLlandingCountry = None
        self.CLvesselFlagCountry = None
        self.CLyear = land['landing_start'][:4]
        self.CLquarter = None
        self.CLmonth = None
        self.CLarea = None
        self.CLstatisticalRectangle = None
        self.CLdataBasisOfStatisticalRectangle = None
        self.CLdataSourceOfStatisticalRectangle = None
        self.CLfisheriesManagementUnit = None
        self.CLgsaSubarea = None
        self.CLjurisdictionArea = None
        self.CLfishingAreaCategory = None
        self.CLfreshWaterName = None
        self.CLexclusiveEconomicZone = None
        self.CLexclusiveEconomicZoneIndicator = None
        self.CLspeciesCode = land['species_no']
        self.CLspeciesFaoCode = None
        self.CLlandingCategory = None
        self.CLcatchCategory = None
        self.CLregDisCategory = None
        self.CLcommercialSizeCategoryScale = None
        self.CLcommercialSizeCategory = None
        self.CLnationalFishingActivity = None
        self.CLmetier6 = None
        self.CLincidentalByCatchMitigationDevice = None
        self.CLlandingLocation = None
        self.CLvesselLengthCategory = None
        self.CLfishingTechnique = None
        self.CLmeshSizeRange = None
        self.CLsupraRegion = None
        self.CLgeoIndicator = None
        self.CLspecificConditionsTechnical = None
        self.CLdeepSeaRegulation = None
        self.CLFDIconfidentialityCode = None
        self.CLofficialWeight = land['weight']
        self.CLscientificWeight = None
        self.CLexplainDifference = None
        self.CLtotalOfficialLandingsValue = None
        self.CLtotalNumberFish = None
        self.CLnumberOfUniqueVessels = None
        self.CLscientificWeightErrorMeasureValueType = None
        self.CLscientificWeightErrorMeasureValueFirst = None
        self.CLscientificWeightErrorMeasureValueSecond = None
        self.CLvalueErrorMeasureValueType = None
        self.CLvalueErrorMeasureValueFirst = None
        self.CLvalueErrorMeasureValueSecond = None
        self.CLnumberFishInCatchErrorMeasureValueType = None
        self.CLnumberFishInCatchErrorMeasureValueFirst = None
        self.CLnumberFishInCatchErrorMeasureValueSecond = None
        self.CLcomment = None
        self.CLscientificWeightQualitativeBias = None
        self.CLconfidentialityFlag = None
        self.CLencryptedVesselIds = None

        self.CLlabel = None



    def dict(self) -> dict:
        cl = {}
        cl['CLcommercialLanding'] = self.CLcommercialLanding
        cl['CLrecordType'] = self.CLrecordType
        cl['CLdataBasisOfScientificWeight'] = self.CLdataBasisOfScientificWeight
        cl['CLdataSourceOfScientificWeight'] = self.CLdataSourceOfScientificWeight
        cl['CLsamplingScheme'] = self.CLsamplingScheme
        cl['CLdataSourceLandingsValue'] = self.CLdataSourceLandingsValue
        cl['CLlandingCountry'] = self.CLlandingCountry
        cl['CLvesselFlagCountry'] = self.CLvesselFlagCountry
        cl['CLyear'] = self.CLyear
        cl['CLquarter'] = self.CLquarter
        cl['CLmonth'] = self.CLmonth
        cl['CLarea'] = self.CLarea
        cl['CLstatisticalRectangle'] = self.CLstatisticalRectangle
        cl['CLdataBasisOfStatisticalRectangle'] = self.CLdataBasisOfStatisticalRectangle
        cl['CLdataSourceOfStatisticalRectangle'] = self.CLdataSourceOfStatisticalRectangle
        cl['CLfisheriesManagementUnit'] = self.CLfisheriesManagementUnit
        cl['CLgsaSubarea'] = self.CLgsaSubarea
        cl['CLjurisdictionArea'] = self.CLjurisdictionArea
        cl['CLfishingAreaCategory'] = self.CLfishingAreaCategory
        cl['CLfreshWaterName'] = self.CLfreshWaterName
        cl['CLexclusiveEconomicZone'] = self.CLexclusiveEconomicZone
        cl['CLexclusiveEconomicZoneIndicator'] = self.CLexclusiveEconomicZoneIndicator
        cl['CLspeciesCode'] = self.CLspeciesCode
        cl['CLspeciesFaoCode'] = self.CLspeciesFaoCode
        cl['CLlandingCategory'] = self.CLlandingCategory
        cl['CLcatchCategory'] = self.CLcatchCategory
        cl['CLregDisCategory'] = self.CLregDisCategory
        cl['CLcommercialSizeCategoryScale'] = self.CLcommercialSizeCategoryScale
        cl['CLcommercialSizeCategory'] = self.CLcommercialSizeCategory
        cl['CLnationalFishingActivity'] = self.CLnationalFishingActivity
        cl['CLmetier6'] = self.CLmetier6
        cl['CLincidentalByCatchMitigationDevice'] = self.CLincidentalByCatchMitigationDevice
        cl['CLlandingLocation'] = self.CLlandingLocation
        cl['CLvesselLengthCategory'] = self.CLvesselLengthCategory
        cl['CLfishingTechnique'] = self.CLfishingTechnique
        cl['CLmeshSizeRange'] = self.CLmeshSizeRange
        cl['CLsupraRegion'] = self.CLsupraRegion
        cl['CLgeoIndicator'] = self.CLgeoIndicator
        cl['CLspecificConditionsTechnical'] = self.CLspecificConditionsTechnical
        cl['CLdeepSeaRegulation'] = self.CLdeepSeaRegulation
        cl['CLFDIconfidentialityCode'] = self.CLFDIconfidentialityCode
        cl['CLofficialWeight'] = self.CLofficialWeight
        cl['CLscientificWeight'] = self.CLscientificWeight
        cl['CLexplainDifference'] = self.CLexplainDifference
        cl['CLtotalOfficialLandingsValue'] = self.CLtotalOfficialLandingsValue
        cl['CLtotalNumberFish'] = self.CLtotalNumberFish
        cl['CLnumberOfUniqueVessels'] = self.CLnumberOfUniqueVessels
        cl['CLscientificWeightErrorMeasureValueType'] = self.CLscientificWeightErrorMeasureValueType
        cl['CLscientificWeightErrorMeasureValueFirst'] = self.CLscientificWeightErrorMeasureValueFirst
        cl['CLscientificWeightErrorMeasureValueSecond'] = self.CLscientificWeightErrorMeasureValueSecond
        cl['CLvalueErrorMeasureValueType'] = self.CLvalueErrorMeasureValueType
        cl['CLvalueErrorMeasureValueFirst'] = self.CLvalueErrorMeasureValueFirst
        cl['CLvalueErrorMeasureValueSecond'] = self.CLvalueErrorMeasureValueSecond
        cl['CLnumberFishInCatchErrorMeasureValueType'] = self.CLnumberFishInCatchErrorMeasureValueType
        cl['CLnumberFishInCatchErrorMeasureValueFirst'] = self.CLnumberFishInCatchErrorMeasureValueFirst
        cl['CLnumberFishInCatchErrorMeasureValueSecond'] = self.CLnumberFishInCatchErrorMeasureValueSecond
        cl['CLcomment'] = self.CLcomment
        cl['CLscientificWeightQualitativeBias'] = self.CLscientificWeightQualitativeBias
        cl['CLconfidentialityFlag'] = self.CLconfidentialityFlag
        cl['CLencryptedVesselIds'] = self.CLencryptedVesselIds

        cl['CLlabel'] = self.CLlabel
        return cl


    def pand(self) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])

    def validate(self):
        return [

            {"name": 'CLcommercialLanding',                        "dtype": "int", "not_null": False},
            {"name": 'CLrecordType',                               "dtype": "str", "not_null": True, "allowed_values": ["CL"]},
            {"name": 'CLdataBasisOfScientificWeight',               "dtype": "str", "not_null": True, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'CLdataSourceOfScientificWeight',             "dtype": "str", "not_null": True, "allowed_values": ["CombOD","Crew","Exprt","HarbLoc","Logb","NotApplicable","Observer","OthDF","PosDat","SalN","SampDC","SampDS","Unknown","VMS"]},
            {"name": 'CLsamplingScheme',                           "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLdataSourceLandingsValue',                  "dtype": "str", "not_null": True, "allowed_values": ["Avgp","Combsnap","Other","Saln"]},
            {"name": 'CLlandingCountry',                           "dtype": "str", "not_null": True, "allowed_values": ["IS"]},
            {"name": 'CLvesselFlagCountry',                        "dtype": "str", "not_null": True, "allowed_values": ["IS"]},
            {"name": 'CLyear',                                     "dtype": "int", "not_null": True, "range": (1965, 2025)},
            {"name": 'CLquarter',                                  "dtype": "int", "not_null": True, "range": (1, 4)},
            {"name": 'CLmonth',                                    "dtype": "int", "not_null": False, "range": (1, 12)},
            {"name": 'CLarea',                                     "dtype": "str", "not_null": True, "allowed_values": ["CL"]},
            {"name": 'CLstatisticalRectangle',                     "dtype": "str", "not_null": True, "allowed_values": ["CL"]},
            {"name": 'CLdataBasisOfStatisticalRectangle',          "dtype": "str", "not_null": True, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'CLdataSourceOfStatisticalRectangle',         "dtype": "str", "not_null": True, "allowed_values": ["CombOD","Crew","Exprt","HarbLoc","Logb","NotApplicable","Observer","OthDF","PosDat","SalN","SampDC","SampDS","Unknown","VMS"]},
            {"name": 'CLfisheriesManagementUnit',                  "dtype": "str", "not_null": False},
            {"name": 'CLgsaSubarea',                               "dtype": "str", "not_null": True, "allowed_values": ["CL"]},
            {"name": 'CLjurisdictionArea',                         "dtype": "str", "not_null": False, "allowed_values": ["Angola","Canaries","Congo","Gambia","Guineav","Guinea-Bissau","Madeira","Mauritania","Morocco","Senegal","Sierra Leona"]},
            {"name": 'CLfishingAreaCategory',                      "dtype": "str", "not_null": True, "allowed_values": ["BP","BR","BU","C","CE","CF","CR","FW","L","LK","MC","MO","NA","T","TT"]},
            {"name": 'CLfreshWaterName',                           "dtype": "str", "not_null": True, "allowed_values": ["CL"]},
            {"name": 'CLexclusiveEconomicZone',                    "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLexclusiveEconomicZoneIndicator',           "dtype": "str", "not_null": False, "allowed_values": ["COAST","EU","RFMO","UK"]},
            {"name": 'CLspeciesCode',                              "dtype": "int", "not_null": True, "allowed_values": ["CL"]},
            {"name": 'CLspeciesFaoCode',                           "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLlandingCategory',                          "dtype": "str", "not_null": True, "allowed_values": ["HuC","HuCInd","Ind","None"]},
            {"name": 'CLcatchCategory',                            "dtype": "str", "not_null": True, "allowed_values": ["BMS","Catch","Dis","Lan","RegDis"]},
            {"name": 'CLregDisCategory',                           "dtype": "str", "not_null": False, "allowed_values": ["DamagedFish","DeMinimis","HighSurvivability","NotApplicable","NotKnown"]},
            {"name": 'CLcommercialSizeCategoryScale',              "dtype": "str", "not_null": False, "allowed_values": ["BEL cod","BEL lemon sole","BEL plaice","BEL sole","English","ES-AZTI","ES-IEO","EU","NLD","PT-IPMA","SCT fish sorting","SCT Nephrops sorting","Unsorted"]},
            {"name": 'CLcommercialSizeCategory',                   "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLnationalFishingActivity',                  "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLmetier6',                                  "dtype": "str", "not_null": True}, # RDBES.Metier
            {"name": 'CLincidentalByCatchMitigationDevice',        "dtype": "str", "not_null": True, "allowed_values": ["AttAcoustic","AttAltProf","AttExclDev","AttLight","AttOther","AttPasRef","AttVis","ModAcoustic","ModEscPan","ModHook","ModOther","ModRopeless","ModStren","ModVis","ModWeight","None","NotRecorded","Unknown","VesAppHaulPro","VesAppMan","VesAppOther","VesAppScaLin"]},
            {"name": 'CLlandingLocation',                          "dtype": "str", "not_null": True}, # RDBES.Harbour
            {"name": 'CLvesselLengthCategory',                     "dtype": "str", "not_null": True, "allowed_values": ["CL"]},
            {"name": 'CLfishingTechnique',                         "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLmeshSizeRange',                            "dtype": "str", "not_null": False},
            {"name": 'CLsupraRegion',                              "dtype": "str", "not_null": False},
            {"name": 'CLgeoIndicator',                             "dtype": "str", "not_null": False},
            {"name": 'CLspecificConditionsTechnical',              "dtype": "str", "not_null": False},
            {"name": 'CLdeepSeaRegulation',                        "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLFDIconfidentialityCode',                   "dtype": "str", "not_null": False},
            {"name": 'CLofficialWeight',                           "dtype": "float", "not_null": True, "range": (0, 2000000000)},
            {"name": 'CLscientificWeight',                         "dtype": "float", "not_null": True, "range": (0, 2000000000)},
            {"name": 'CLexplainDifference',                        "dtype": "str", "not_null": True, "allowed_values": ["CL"]},
            {"name": 'CLtotalOfficialLandingsValue',               "dtype": "float", "not_null": True, "range": (1, 100000000)},
            {"name": 'CLtotalNumberFish',                          "dtype": "int", "not_null": False, "range": (1, 100000)},
            {"name": 'CLnumberOfUniqueVessels',                    "dtype": "int", "not_null": True, "range": (1, 100000)},
            {"name": 'CLscientificWeightErrorMeasureValueType',    "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLscientificWeightErrorMeasureValueFirst',   "dtype": "float", "not_null": False, "range": (0.000001, 999)},
            {"name": 'CLscientificWeightErrorMeasureValueSecond',  "dtype": "float", "not_null": False, "range": (0.000001, 999)},
            {"name": 'CLvalueErrorMeasureValueType',               "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLvalueErrorMeasureValueFirst',              "dtype": "float", "not_null": False, "range": (0.000001, 999)},
            {"name": 'CLvalueErrorMeasureValueSecond',             "dtype": "float", "not_null": False, "range": (0.000001, 999)},
            {"name": 'CLnumberFishInCatchErrorMeasureValueType',   "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLnumberFishInCatchErrorMeasureValueFirst',  "dtype": "float", "not_null": False, "range": (0.000001, 999)},
            {"name": 'CLnumberFishInCatchErrorMeasureValueSecond', "dtype": "float", "not_null": False, "range": (0.000001, 999)},
            {"name": 'CLcomment',                                  "dtype": "str", "not_null": False},
            {"name": 'CLscientificWeightQualitativeBias',          "dtype": "str", "not_null": False, "allowed_values": ["CL"]},
            {"name": 'CLconfidentialityFlag',                      "dtype": "str", "not_null": True, "allowed_values": ["N","Y"]},
            {"name": 'CLencryptedVesselIds',                       "dtype": "str", "not_null": True},

            {"name": 'CLlabel',                                    "dtype": "str",  "not_null": False},
        ]
