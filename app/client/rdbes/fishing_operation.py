#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd
from app.client.utils.geo import ices_statistical_rectangle

class FishingOperation:
    FOrecordType = 'FO'

    def __init__(self, sample: dict):
        self.FOid = sample['fishing_station_id']
        self.FTid = sample['fishing_trip_id']
        self.SDid = None
        self.FOstratification = 'N'
        self.FOsequenceNumber = sample['fishing_station_id'] if sample['fishing_station_id'] != None else None
        self.FOstratumName = 'U'
        self.FOclustering = 'N'
        self.FOclusterName = 'U'
        self.FOsampler = 'SelfSampling'
        self.FOaggregationLevel = 'H'
        self.FOvalidity = 'V'
        self.FOcatchReg = 'Lan'
        self.FOstartDate = sample['fishing_start'].strftime('%Y-%m-%d') if sample['fishing_start'] != None else None
        self.FOstartTime = sample['fishing_start'].strftime('%H:%M') if sample['fishing_start'] != None else None
        self.FOendDate = sample['fishing_end'].strftime('%Y-%m-%d') if sample['fishing_end'] != None else None
        self.FOendTime = sample['fishing_end'].strftime('%H:%M') if sample['fishing_end'] != None else None
        self.FOduration = int((sample['fishing_end'] - sample['fishing_start']).total_seconds()/60) if sample['fishing_end'] != None and sample['fishing_start'] != None else None
        self.FOfishingDurationDataBasis = 'Measured'
        self.FOdurationSource = 'Crew'
        self.FOhandlingTime = None
        self.FOstartLat = sample['tow_latitude'] if sample['tow_latitude'] != None else None
        self.FOstartLon = sample['tow_longitude'] if sample['tow_longitude'] != None else None
        self.FOstopLat = sample['tow_latitude_end'] if sample['tow_latitude_end'] != None else None
        self.FOstopLon = sample['tow_longitude_end'] if sample['tow_longitude_end'] != None else None
        self.FOexclusiveEconomicZoneIndicator = None
        self.FOarea = sample['area']
        self.FOrectangle =  ices_statistical_rectangle(self.FOstartLat,self.FOstartLon) if self.FOstartLat != None and self.FOstartLon != None else None
        self.FOfisheriesManagementUnit = None
        self.FOgsaSubarea = 'NotApplicable'
        self.FOjurisdictionArea = None
        self.FOgeographicalDataBasis = 'Measured'
        self.FOgeographicalSource = 'PosDat'
        self.FOfishingDepth = None
        self.FOwaterDepth = None
        self.FOnationalFishingActivity = None
        self.FOmetier5 = sample['metier6'][:7] if sample['metier6'] != None else None
        self.FOmetier6 = sample['metier6']
        self.FOgear = sample['fao_gear_code']
        self.FOgearDataBasis = None
        self.FOgearSource = None
        self.FOmeshSize = sample['mesh_size'] if sample['mesh_size'] != None else None
        self.FOselectionDevice = None
        self.FOselectionDeviceMeshSize = None
        self.FOtargetSpecies = None
        self.FOincidentalByCatchMitigationDeviceFirst = 'Unknown'
        self.FOincidentalByCatchMitigationDeviceTargetFirst = 'NotApplicable'
        self.FOincidentalByCatchMitigationDeviceSecond = 'None'
        self.FOincidentalByCatchMitigationDeviceTargetSecond = 'NotApplicable'
        self.FOgearDimensions = None
        self.FOobservationCode = 'Unknown'
        self.FOnumberTotal = None
        self.FOnumberFOsampled = None
        self.FOselectionProb = None
        self.FOinclusionProb = None
        self.FOselectionMethod = 'NPJS'
        self.FOunitName = sample['fishing_station_id']
        self.FOselectionMethodCluster = None
        self.FOnumberTotalClusters = None
        self.FOnumberFOsampledClusters = None
        self.FOselectionProbCluster = None
        self.FOinclusionProbCluster = None
        self.FOsampled = 'Y'
        self.FOreasonNotSampled = 'Unknown'
        self.FOnonResponseCollected = None
        self.FOauxiliaryVariableTotal = None
        self.FOauxiliaryVariableValue = None
        self.FOauxiliaryVariableName = None
        self.FOauxiliaryVariableUnit = None


    def dict(self) -> list:
        fo = {}
        fo['FOid'] = self.FOid
        fo['FTid'] = self.FTid
        fo['SDid'] = self.SDid
        fo['FOrecordType'] = self.FOrecordType
        fo['FOstratification'] = self.FOstratification
        fo['FOsequenceNumber'] = self.FOsequenceNumber
        fo['FOstratumName'] = self.FOstratumName
        fo['FOclustering'] = self.FOclustering
        fo['FOclusterName'] = self.FOclusterName
        fo['FOsampler'] = self.FOsampler
        fo['FOaggregationLevel'] = self.FOaggregationLevel
        fo['FOvalidity'] = self.FOvalidity
        fo['FOcatchReg'] = self.FOcatchReg
        fo['FOstartDate'] = self.FOstartDate
        fo['FOstartTime'] = self.FOstartTime
        fo['FOendDate'] = self.FOendDate
        fo['FOendTime'] = self.FOendTime
        fo['FOduration'] = self.FOduration
        fo['FOfishingDurationDataBasis'] = self.FOfishingDurationDataBasis
        fo['FOdurationSource'] = self.FOdurationSource
        fo['FOhandlingTime'] = self.FOhandlingTime
        fo['FOstartLat'] = self.FOstartLat
        fo['FOstartLon'] = self.FOstartLon
        fo['FOstopLat'] = self.FOstopLat
        fo['FOstopLon'] = self.FOstopLon
        fo['FOexclusiveEconomicZoneIndicator'] = self.FOexclusiveEconomicZoneIndicator
        fo['FOarea'] = self.FOarea
        fo['FOrectangle'] = self.FOrectangle
        fo['FOfisheriesManagementUnit'] = self.FOfisheriesManagementUnit
        fo['FOgsaSubarea'] = self.FOgsaSubarea
        fo['FOjurisdictionArea'] = self.FOjurisdictionArea
        fo['FOgeographicalDataBasis'] = self.FOgeographicalDataBasis
        fo['FOgeographicalSource'] = self.FOgeographicalSource
        fo['FOfishingDepth'] = self.FOfishingDepth
        fo['FOwaterDepth'] = self.FOwaterDepth
        fo['FOnationalFishingActivity'] = self.FOnationalFishingActivity
        fo['FOmetier5'] = self.FOmetier5
        fo['FOmetier6'] = self.FOmetier6
        fo['FOgear'] = self.FOgear
        fo['FOgearDataBasis'] = self.FOgearDataBasis
        fo['FOgearSource'] = self.FOgearSource
        fo['FOmeshSize'] = self.FOmeshSize
        fo['FOselectionDevice'] = self.FOselectionDevice
        fo['FOselectionDeviceMeshSize'] = self.FOselectionDeviceMeshSize
        fo['FOtargetSpecies'] = self.FOtargetSpecies
        fo['FOincidentalByCatchMitigationDeviceFirst'] = self.FOincidentalByCatchMitigationDeviceFirst
        fo['FOincidentalByCatchMitigationDeviceTargetFirst'] = self.FOincidentalByCatchMitigationDeviceTargetFirst
        fo['FOincidentalByCatchMitigationDeviceSecond'] = self.FOincidentalByCatchMitigationDeviceSecond
        fo['FOincidentalByCatchMitigationDeviceTargetSecond'] = self.FOincidentalByCatchMitigationDeviceTargetSecond
        fo['FOgearDimensions'] = self.FOgearDimensions
        fo['FOobservationCode'] = self.FOobservationCode
        fo['FOnumberTotal'] = self.FOnumberTotal
        fo['FOnumberFOsampled'] = self.FOnumberFOsampled
        fo['FOselectionProb'] = self.FOselectionProb
        fo['FOinclusionProb'] = self.FOinclusionProb
        fo['FOselectionMethod'] = self.FOselectionMethod
        fo['FOunitName'] = self.FOunitName
        fo['FOselectionMethodCluster'] = self.FOselectionMethodCluster
        fo['FOnumberTotalClusters'] = self.FOnumberTotalClusters
        fo['FOnumberFOsampledClusters'] = self.FOnumberFOsampledClusters
        fo['FOselectionProbCluster'] = self.FOselectionProbCluster
        fo['FOinclusionProbCluster'] = self.FOinclusionProbCluster
        fo['FOsampled'] = self.FOsampled
        fo['FOreasonNotSampled'] = self.FOreasonNotSampled
        fo['FOnonResponseCollected'] = self.FOnonResponseCollected
        fo['FOauxiliaryVariableTotal'] = self.FOauxiliaryVariableTotal
        fo['FOauxiliaryVariableValue'] = self.FOauxiliaryVariableValue
        fo['FOauxiliaryVariableName'] = self.FOauxiliaryVariableName
        fo['FOauxiliaryVariableUnit'] = self.FOauxiliaryVariableUnit
        return fo

    def pand(self: list) -> pd.DataFrame:
        # return self.dict()
        return pd.DataFrame([self.dict()])


    def validate(self):
        return [
            {"name": 'FOid',                                              "dtype": "int", "not_null": False},
            {"name": 'FTid',                                              "dtype": "str", "not_null": False},
            {"name": 'SDid',                                              "dtype": "int", "not_null": False},
            {"name": 'FOrecordType',                                      "dtype": "str", "not_null": True, "allowed_values": ["FO"]},
            {"name": 'FOstratification',                                  "dtype": "str", "not_null": True, "allowed_values": ["N","Y"]},
            {"name": 'FOsequenceNumber',                                  "dtype": "int", "not_null": True},
            {"name": 'FOstratumName',                                     "dtype": "str", "not_null": True},
            {"name": 'FOclustering',                                      "dtype": "str", "not_null": True, "allowed_values": ["1C", "1CS", "2C", "2CS", "N", "S1C", "S2C"]},
            {"name": 'FOclusterName',                                     "dtype": "str", "not_null": True},
            {"name": 'FOsampler',                                         "dtype": "str", "not_null": False, "allowed_values": ["Control", "Imagery", "Observer", "SelfSampling"]},
            {"name": 'FOaggregationLevel',                                "dtype": "str", "not_null": True, "allowed_values": ["H","I"]},
            {"name": 'FOvalidity',                                        "dtype": "str", "not_null": True, "allowed_values": ["I","V"]},
            {"name": 'FOcatchReg',                                        "dtype": "str", "not_null": True, "allowed_values": ["All","Dis","Lan","None"]},
            {"name": 'FOstartDate',                                       "dtype": "str", "not_null": False},
            {"name": 'FOstartTime',                                       "dtype": "str", "not_null": False},
            {"name": 'FOendDate',                                         "dtype": "str", "not_null": True},
            {"name": 'FOendTime',                                         "dtype": "str", "not_null": False},
            {"name": 'FOduration',                                        "dtype": "int", "not_null": False},
            {"name": 'FOfishingDurationDataBasis',                        "dtype": "str", "not_null": True, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'FOdurationSource',                                  "dtype": "str", "not_null": True, "allowed_values": ["CombOD","Crew","Exprt","HarbLoc","Logb","NotApplicable","Observer","OthDF","PosDat","SalN","SampDC","SampDS","Unknown","VMS"]},
            {"name": 'FOhandlingTime',                                    "dtype": "int", "not_null": False},
            {"name": 'FOstartLat',                                        "dtype": "float", "not_null": False, "range": (-90000000, 90000000)},
            {"name": 'FOstartLon',                                        "dtype": "float", "not_null": False, "range": (-180000000, 180000000)},
            {"name": 'FOstopLat',                                         "dtype": "float", "not_null": False, "range": (-90000000, 90000000)},
            {"name": 'FOstopLon',                                         "dtype": "float", "not_null": False, "range": (-180000000, 180000000)},
            {"name": 'FOexclusiveEconomicZoneIndicator',                  "dtype": "str", "not_null": False, "allowed_values": ["IS"]}, #HINT/ath
            {"name": 'FOarea',                                            "dtype": "str", "not_null": True} ,
            {"name": 'FOrectangle',                                       "dtype": "str", "not_null": False},
            {"name": 'FOfisheriesManagementUnit',                         "dtype": "str", "not_null": False},
            {"name": 'FOgsaSubarea',                                      "dtype": "str", "not_null": True, "allowed_values": ["NotApplicable"]},
            # {"name": 'FOgsaSubarea',                                      "dtype": "str", "not_null": True, "allowed_values": ["NotApplicable","1","10","11.1","11.2","12","13","14","15","16","17","18","19","2","20","21","22","23","24","25","26","27","28","29","3","30","4","5","6","7","8","9"]},
            {"name": 'FOjurisdictionArea',                                "dtype": "str", "not_null": False, "allowed_values": ["Angola","Canaries","Congo","Gambia","Guineav","Guinea-Bissau","Madeira","Mauritania","Morocco","Senegal","Sierra Leona"]},
            {"name": 'FOgeographicalDataBasis',                           "dtype": "str", "not_null": False, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'FOgeographicalSource',                              "dtype": "str", "not_null": False, "allowed_values": ["CombOD","Crew","Exprt","HarbLoc","Logb","NotApplicable","Observer","OthDF","PosDat","SalN","SampDC","SampDS","Unknown","VMS"]},
            {"name": 'FOfishingDepth',                                    "dtype": "int", "not_null": False},
            {"name": 'FOwaterDepth',                                      "dtype": "int", "not_null": False},
            {"name": 'FOnationalFishingActivity',                         "dtype": "str", "not_null": False, "allowed_values": ["?"]},
            {"name": 'FOmetier5',                                         "dtype": "str", "not_null": False},
            {"name": 'FOmetier6',                                         "dtype": "str", "not_null": True}, # RDBES.Metier
            {"name": 'FOgear',                                            "dtype": "str", "not_null": True, "allowed_values": ["FPN","FPO","FWR","FYK","GEL","GN","GNC","GND","GNS","GTN","GTR","HMD","LA","LH","LHM","LHP","LLD","LLS","LTL","LX","MIS","OTB","OTM","OTT","PS","PTB","PTM","SB","SBV","SDN","SPR","SSC","TBB"]},
            {"name": 'FOgearDataBasis',                                   "dtype": "str", "not_null": False, "allowed_values": ["Estimated","Measured","NotApplicable","Official","Unknown"]},
            {"name": 'FOgearSource',                                      "dtype": "str", "not_null": False, "allowed_values": ["CombOD","Crew","Exprt","HarbLoc","Logb","NotApplicable","Observer","OthDF","PosDat","SalN","SampDC","SampDS","Unknown","VMS"]},
            {"name": 'FOmeshSize',                                        "dtype": "int", "not_null": False},
            {"name": 'FOselectionDevice',                                 "dtype": "int", "not_null": False, "allowed_values": ["0","1","2","3","4"]},
            {"name": 'FOselectionDeviceMeshSize',                         "dtype": "int", "not_null": False},
            {"name": 'FOtargetSpecies',                                   "dtype": "str", "not_null": False, "allowed_values": ["FO"]},
            {"name": 'FOincidentalByCatchMitigationDeviceFirst',          "dtype": "str", "not_null": True, "allowed_values": ["AttAcoustic","AttAltProf","AttExclDev","AttLight","AttOther","AttPasRef","AttVis","ModAcoustic","ModEscPan","ModHook","ModOther","ModRopeless","ModStren","ModVis","ModWeight","None","NotRecorded","Unknown","VesAppHaulPro","VesAppMan","VesAppOther","VesAppScaLin"]},
            {"name": 'FOincidentalByCatchMitigationDeviceTargetFirst',    "dtype": "str", "not_null": True, "allowed_values": ["Birds","LargeCetaceans","NotApplicable","OtherOrCombination","ProtectedElasmobranchs","ProtectedFish","Seals","SmallCetaceans","Turtles"]},
            {"name": 'FOincidentalByCatchMitigationDeviceSecond',         "dtype": "str", "not_null": True, "allowed_values": ["None"]},
            {"name": 'FOincidentalByCatchMitigationDeviceTargetSecond',   "dtype": "str", "not_null": True, "allowed_values": ["NotApplicable"]},
            {"name": 'FOgearDimensions',                                  "dtype": "int", "not_null": False},
            {"name": 'FOobservationCode',                                 "dtype": "str", "not_null": True, "allowed_values": ["Dr","DrOt","DrSl","DrSlOt","Ot","Pr","PrDr","PrDrOt","PrDrSl","PrDrSlOt","PrOt","PrSl","PrSlOt","Sl","SlOt","So","SoDr","SoDrOt","SoDrSl","SoDrSlOt","SoOt","SoPr","SoPrDr","SoPrDrOt","SoPrDrSl","SoPrDrSlOt","SoPrOt","SoPrSl","SoPsSlOt","SoSl","SoSlOt","Unknown"]},
            {"name": 'FOnumberTotal',                                     "dtype": "int", "not_null": False},
            {"name": 'FOnumberFOsampled',                                 "dtype": "int", "not_null": False},
            {"name": 'FOselectionProb',                                   "dtype": "float", "not_null": False},
            {"name": 'FOinclusionProb',                                   "dtype": "float", "not_null": False},
            {"name": 'FOselectionMethod',                                 "dtype": "str", "not_null": True, "allowed_values": ["CENSUS", "D", "FIXED", "NotApplicable", "NPCLQS-O", "NPCLQS-T", "NPCS", "NPJS", "NPQSRSWOR", "NPQSRSWR", "NPQSYSS", "R", "SRSWOR", "SRSWR", "SYSS", "Unknown", "UPSWOR", "UPSWR"]},
            {"name": 'FOunitName',                                        "dtype": "str", "not_null": True},
            {"name": 'FOselectionMethodCluster',                          "dtype": "str", "not_null": False, "allowed_values": ["CENSUS", "D", "FIXED", "NotApplicable", "NPCLQS-O", "NPCLQS-T", "NPCS", "NPJS", "NPQSRSWOR", "NPQSRSWR", "NPQSYSS", "R", "SRSWOR", "SRSWR", "SYSS", "Unknown", "UPSWOR", "UPSWR"]},
            {"name": 'FOnumberTotalClusters',                             "dtype": "int", "not_null": False},
            {"name": 'FOnumberFOsampledClusters',                         "dtype": "int", "not_null": False},
            {"name": 'FOselectionProbCluster',                            "dtype": "float", "not_null": False},
            {"name": 'FOinclusionProbCluster',                            "dtype": "float", "not_null": False},
            {"name": 'FOsampled',                                         "dtype": "str", "not_null": True, "allowed_values": ["N","Y"]},
            {"name": 'FOreasonNotSampled',                                "dtype": "str", "not_null": False, "allowed_values": ["CameraNotWorking", "CameraViewObstructed", "IndustryDeclined", "NoAnswer", "NoContactDetails", "NotAvailable", "ObserverDeclined", "Other", "OutOfFrame", "PoorImageQuality", "QuotaReached", "Unknown"]},
            {"name": 'FOnonResponseCollected',                            "dtype": "str", "not_null": False, "allowed_values": ["N","Y"]},
            {"name": 'FOauxiliaryVariableTotal',                          "dtype": "float", "not_null": False},
            {"name": 'FOauxiliaryVariableValue',                          "dtype": "float", "not_null": False},
            {"name": 'FOauxiliaryVariableName',                           "dtype": "str", "not_null": False},
            {"name": 'FOauxiliaryVariableUnit',                           "dtype": "str", "not_null": False},
        ]
