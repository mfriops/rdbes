#!/usr/local/bin/python3
# coding: utf-8

import os, json
import pandas as pd
import io, csv
from typing import Any, Dict
from flask import jsonify
from requests import HTTPError, Response

from app.client.utils.pandas import match_closest_station
from app.client.api.rdbes import RdbesService
from app.client.business.channel import ChannelBusiness
from app.client.business.vessel import VesselBusiness
from app.client.business.gear import GearBusiness
from app.client.business.adb import AdbBusiness
from app.client.business.agf import AgfBusiness
from app.client.business.quota import QuotaBusiness
from app.client.rdbes.design import Design
from app.client.rdbes.fishing_trip import FishingTrip
from app.client.rdbes.fishing_operation import FishingOperation
from app.client.rdbes.species_selection import SpeciesSelection
from app.client.rdbes.sample import Sample
from app.client.rdbes.sampling_details import SamplingDetails
from app.client.rdbes.vessel_details import VesselDetails
from app.client.rdbes.individual_species import IndividualSpecies
from app.client.rdbes.species_list import SpeciesList
from app.client.rdbes.frequency_measure import FrequencyMeasure
from app.client.rdbes.biological_variable import BiologicalVariable
from app.client.rdbes.commercial_landing import CommercialLanding
from app.client.rdbes.commercial_effort import CommercialEffort
from app.client.rdbes.harbour import Harbour
from app.client.classes.channel.channel_station import ChannelStation
from app.client.classes.channel.channel_sample import ChannelSample
from app.client.classes.biota.biota_measure import BiotaMeasure
from app.client.classes.taxon.species import TaxonSpecies
from app.client.classes.vessel.vessel import VesselVessel
from app.client.classes.gear.fishing_gear import GearFishingGear
from app.client.classes.gear.isscfg import GearIsscfg
from app.client.classes.adb.fishing_trip import AdbFishingTrip
from app.client.classes.adb.fishing_station import AdbFishingStation
from app.client.classes.adb.trawl_and_seine_net import AdbTrawlAndSeineNet
from app.client.classes.adb.target_assemblage import AdbTargetAssemblage
from app.client.classes.adb.target_station_assemblage import AdbTargetStationAssemblage
from app.client.classes.agf.landings import AgfLandings
from app.client.classes.quota.quota import QuotaQuota

from app.client.utils.ora import nvl
from app.client.utils.misc import chunked
from server.services.adb.models import TargetAssemblage


class RdbesBusiness:
    """
    Simple synchronous client for the Oracle-backed rdbes Flask service.

    Parameters
    ----------
    base_url :
        Root URL of the micro-service, *without* a trailing slash.
        Can also be supplied via env-var ``RDBES_API_URL``.
    timeout :
        Per-request timeout in seconds (default **10**).
    """

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #
    rdbes_api_url = os.environ.get("API_RDBES_GATEWAY_URL")
    if not rdbes_api_url:
        rdbes_api_url = "http://127.0.0.1:8001/rdbes"

    print(rdbes_api_url)
    rdbes_service = RdbesService(rdbes_api_url.rstrip("/"))

    channel_business = ChannelBusiness()
    vessel_business = VesselBusiness()
    gear_business = GearBusiness()
    adb_business = AdbBusiness()
    agf_business = AgfBusiness()
    quota_business = QuotaBusiness()

    def health(self) -> Dict[str, Any]:
        return jsonify(self.rdbes_service.health())

    def insert(self, table: str, payload: Dict[str, Any]) -> Any:
        ret_json =  jsonify(self.rdbes_service.insert(table, payload))
        return json.loads(ret_json.data)

    def select(self, table: str):
        ret_json =  jsonify(self.rdbes_service.select(table))
        return json.loads(ret_json.data)

    def get_harbour(self, port_nos: list):
        return json.loads(jsonify(self.rdbes_service.get_harbour(port_nos)).data)

    def get_area(self, lat: float, lon: float):
        ret = json.loads(jsonify(self.rdbes_service.get_area(lat, lon)).data)
        return ret['code']

    def get_metier(self, area_code: str, gear_type: str, target_assemblage: str, mesh_size: int):
        if area_code is None or gear_type is None or target_assemblage is None or mesh_size is None:
            return None
        else:
            ret = json.loads(jsonify(self.rdbes_service.get_metier(area_code, gear_type, target_assemblage, mesh_size)).data)
            return ret['metier']

    # ------------------------------------------------------------------ #
    # Internal helpers                                                   #
    # ------------------------------------------------------------------ #
    def _get_json(self, path: str) -> Dict[str, Any]:
        """Perform *GET* and return parsed JSON (raises ``NotFound`` on 404)."""
        url = f"{self.base_url}{path}"
        try:
            resp: Response = self._session.get(url, timeout=self.timeout)
            resp.raise_for_status()
        except HTTPError as exc:  # covers 4xx & 5xx
            if exc.response is not None and exc.response.status_code == 404:
                raise NotFound(f"Resource not found: {url}") from None
            raise
        return resp.json()

    def update_trip_info(self, channelStationDf):

        def safe_call(row):
            if pd.isna(row['vessel_no']) or pd.isna(row['station_date']):
                return {}  # skip update if key values are missing
            try:
                return self.adb_business.get_fishing_trip(row['vessel_no'], row['station_date']) or {}
            except Exception:
                return {}

        # Apply the external function once per row
        updates = channelStationDf.apply(safe_call, axis=1)

        # Now map the result dict fields to DataFrame columns
        channelStationDf['fishing_trip_id'] = [d.get('id') for d in updates]
        channelStationDf['departure'] = [d.get('departure') for d in updates]
        channelStationDf['arrival'] = [d.get('landing') for d in updates]
        channelStationDf['departure_port_no'] = pd.Series([d.get('departure_port_no') for d in updates], dtype='Int64')
        channelStationDf['landing_port_no'] = pd.Series([d.get('landing_port_no') for d in updates], dtype='Int64')

        return channelStationDf


    def write_sample(self, cruiseDict, year, target_species_no):

        errors = False
        errorsHtml = {}

        ##
        ## The population
        # ## Fyrst all the ships with quota -----------------------------------------------------------------------------------
        # quotaCol = ['registration_no','species_no','quota_type','quota','valid_from','valid_to']
        # quotaDf = pd.DataFrame([QuotaQuota(quota).dict() for quota in self.quota_business.get_quota(target_species_no, year)], columns=quotaCol)
        #
        # ## Sum quota/weight over all quota types / ensure weight is numeric (optional but common) ----------------------
        # quotaDf['quota'] = pd.to_numeric(quotaDf['quota'], errors='coerce')
        #
        # quotaTotDf = (
        #     quotaDf
        #     .groupby(['registration_no', 'species_no'], dropna=False)
        #     .agg(total_quota=('quota', 'sum'))
        #     .reset_index()
        #     .query('total_quota > 100000') # Only vessel with quota > 100 tonn
        #     .sort_values('registration_no', ignore_index=True)
        # )

        ##
        ## The population / those ships that fishes the quota ----------------------------------------------------------------------
        populationCol = ['fishing_trip_id','registration_no','species_no','departure_date','landing_date','departure_port_no','landing_port_no','landing_year','quantity','catch_type','stations_cnt']
        populationDf = pd.DataFrame([AdbTargetAssemblage(mack).dict() for mack in self.adb_business.get_target_assemblage(target_species_no, year)], columns=populationCol)

        populationDf["quantity"] = pd.to_numeric(populationDf["quantity"], errors='coerce')
        # populationDf = populationDf[populationDf["quantity"] > 10000]

        # ## Finally the population to sample from -----------------------------------------------------------------------
        # populationDf = quotaTotDf.merge(
        #                                fishDf,
        #                                on="registration_no",
        #                                how="inner" # only vessels on with quota and that fished the quota
        #                                # suffixes=("_quota", "_mackerel")
        #                     )


        # channel-Stations
        ## Get all the sample (stations), there can be more than one cruise, get station for all of them
        channelStationCol = ['cruise_id','station_id','station_date','latitude','longitude','vessel_no']
        channelStaionList = []
        for cru in cruiseDict:
            for stat in self.channel_business.get_station(cru['cruise_id']):
                channelStaionList.append(ChannelStation(stat).dict())

        channelStationDf = pd.DataFrame(channelStaionList, columns=channelStationCol)

        # Find the ADB-Fishing Trip for all the channel-Stations
        # TODO DB-call, slow ??
        # TODO change station_date to noon from midnight
        self.update_trip_info(channelStationDf)

        # vessels, first get registration_nos for all population and sample-vessels / Remove duplicate and None
        registration_nos = pd.unique(
            pd.concat([
                populationDf['registration_no'],
                channelStationDf['vessel_no'],
            ]).dropna()
        )
        vesselDf = pd.DataFrame([VesselVessel(ves).dict() for ves in self.vessel_business.get_vessel(registration_nos)])
        # TODO for now, delete non-icelandic vessels, include it maby later
        # vesselDf.drop(vesselDf[vesselDf['status'] != 'Á aðalskipaskrá'].index, inplace=True)

        # Merge with vessel on registration_no from sampleDf
        # TODO þarf líkleaa ekki þetta join nema kannski fyrir vessel_id, 7.10.2025 - ath. betur
        populationDf = populationDf.merge(vesselDf[['registration_no', 'vessel_id']], on='registration_no', how='inner')

        # TODO breyta þannig að ég uppfæri hafnir i populationDf í stað channelStationDf
        # To get all ICES-port-codes
        port_nos = pd.unique(
            pd.concat([
                populationDf['departure_port_no'],
                populationDf['landing_port_no'],
                vesselDf['home_port_no'],
            ]).dropna()
        )
        harbourDf = pd.DataFrame([Harbour(port).dict() for port in self.get_harbour(port_nos)])

        # Merge on key departure_port_no for ICES-port-code
        populationDf = populationDf.merge(harbourDf.rename(columns={'harbour':'departure_harbour'}), left_on='departure_port_no', right_on='port_no', how='left')
        populationDf.drop(columns=['departure_port_no','port_no'], inplace=True)

        # Merge on key landing_port_no for ICES-port-code
        populationDf = populationDf.merge(harbourDf.rename(columns={'harbour':'landing_harbour'}), left_on='landing_port_no', right_on='port_no', how='left')
        populationDf.drop(columns=['landing_port_no','port_no'], inplace=True)

        # Merge on key home_port_no for ICES-port-code
        vesselDf = vesselDf.merge(harbourDf.rename(columns={'harbour':'home_harbour'}), left_on='home_port_no', right_on='port_no', how='left')
        vesselDf.drop(columns=['home_port_no','port_no'], inplace=True)
        vesselDf['year'] = year

        # TODO remove, spurning um að færa aftar og reikna á adb-lag/long, 7.10.2025 ath. betur með þetta
        channelStationDf['area'] = channelStationDf.apply(
            lambda row: self.get_area(row['latitude'],row['longitude'] or {}), axis=1
        )

        # Sample
        station_ids = channelStationDf['station_id'].unique()
        channelSampleCol = ['station_id', 'sample_id', 'target_assemblage']
        channelSampleDf = pd.DataFrame([ChannelSample(samp).dict() for samp in self.channel_business.get_sample(station_ids)], columns=channelSampleCol)

        # Before the update of the fields in station/sample the correct fishing-station needs to be found
        # It is done with "match_closest_station"

        # Merge station and sample on station_id
        channelStationSampleDf = channelStationDf.merge(channelSampleDf, on='station_id', how='inner')

        # Get the ADB-Fishing Trips for all the Sample taken
        fishing_trip_ids = channelStationDf['fishing_trip_id'].dropna().unique()

        # Find ALL the ADB-Fishing Stations for all the SAMPLE-Fishing Trips
        # adbFishingStationDf = pd.DataFrame([AdbFishingStation(stat).dict() for stat in self.adb_business.get_fishing_station(fishing_trip_ids)])
        adbFishingStationDf = pd.DataFrame([AdbTargetStationAssemblage(stat).dict() for stat in self.adb_business.get_fishing_station_for_target(fishing_trip_ids, target_species_no)])

        # Gear, first get isscfg_no / Remove duplicate and None
        fishing_gear_nos = adbFishingStationDf['fishing_gear_no'].dropna().unique()
        fishingGearDf = pd.DataFrame([GearFishingGear(fg).dict() for fg in self.gear_business.get_fishing_gear(fishing_gear_nos)])
        isscfg_nos = fishingGearDf['isscfg_no'].dropna().unique()
        isscfgDf = pd.DataFrame([GearIsscfg(iss).dict() for iss in self.gear_business.get_isscfg(isscfg_nos)])
        fishingGearDf = fishingGearDf.merge(isscfgDf.rename(columns={'stand_no':'fao_gear_code'}), on='isscfg_no', how='inner')

        # Merge with Fishing gear information
        fishing_station_ids = adbFishingStationDf['fishing_station_id'].dropna().unique()
        adbTrawlAndSeineNetDf = pd.DataFrame([AdbTrawlAndSeineNet(stat).dict() for stat in self.adb_business.get_trawl_and_seine_net(fishing_station_ids)])
        adbFishingStationDf = adbFishingStationDf.merge(adbTrawlAndSeineNetDf[['fishing_station_id','mesh_size']], on='fishing_station_id', how='inner')


        # Merge with station/sample
        # channelStationSampleDf.drop(columns=['mesh_size'],inplace=True)
        channelStationSampleDf = channelStationSampleDf.merge(adbFishingStationDf[
            ['fishing_trip_id', 'fishing_station_id', 'fishing_gear_no', 'fishing_start', 'fishing_end', 'latitude', 'longitude', 'latitude_end', 'longitude_end', 'mesh_size']
            ].rename(columns={'latitude':'tow_latitude','latitude_end':'tow_latitude_end','longitude':'tow_longitude','longitude_end':'tow_longitude_end'})
            , on='fishing_trip_id', how='inner')
        channelStationSampleDf = channelStationSampleDf.astype({
            'mesh_size': 'Int64',
            'fishing_gear_no': 'Int64'
            })

        # Find the nearest station to sample time and location
        channelStationSampleDf = match_closest_station(channelStationSampleDf, time_weight=0.5)

        # Final SAMPLE
        # TODO líka að taka þau sample senm eiga ekki fishing station (MAKR-2024 þá tapast eitt sýni vegna þessa, líklegast í næstu setn.)
        # TODO sko það þarf að taka eitt tripDf fyrir allar ferðirnar því það geta verið fleri en eitt sample per trip, en það er það ekki í MAKR-2024
        sampleDf = channelStationSampleDf[(channelStationSampleDf['scaled_score'] == 1.0) | (channelStationSampleDf['scaled_score'].isna())]


        # Merge with gear on isscfg_no from sampleDf
        sampleDf = sampleDf.merge(fishingGearDf[['fishing_gear_no','fao_gear_code']], on='fishing_gear_no', how='left')
        sampleDf['sequence'] = sampleDf.groupby('fishing_trip_id')['station_id'].rank(method='first').astype(int)
        # sampleDf['sequence'] = sampleDf.sort_values('fishing_trip_id')['station_id'].rank(method='first').astype(int)

        # One get for each combination of area, stand_no, target species and mesh size
        metierDf = sampleDf[['area','fao_gear_code','target_assemblage','mesh_size']]
        metierDf = metierDf[['area','fao_gear_code','target_assemblage','mesh_size']].dropna(subset=['area','fao_gear_code','target_assemblage','mesh_size']).drop_duplicates()

        if not metierDf.empty:
            metierDf['metier6']  = metierDf.apply( lambda row: self.get_metier(
                                                        row['area'], row['fao_gear_code'], row['target_assemblage'], row['mesh_size']
                                                    ) if pd.notna(row['area']) and pd.notna(row['fao_gear_code'])
                                                         and pd.notna(row['target_assemblage']) and pd.notna(row['mesh_size'])
                                                    else None,
                                                    axis=1
                                                )
        # sampleDf.drop(columns=['metier6'],inplace=True)
        sampleDf = sampleDf.merge(metierDf, on=['area','fao_gear_code','target_assemblage','mesh_size'], how='left')

        # Measure
        sample_ids = sampleDf['sample_id'].unique()
        biotaMeasureDf = pd.DataFrame([BiotaMeasure(meas).dict() for meas in self.channel_business.get_measure(sample_ids)])
        biotaMeasureDf['species_no'] = biotaMeasureDf['species_no'].astype('Int64')

        # Species, first get species_no / remove duplicate and None
        species_nos = biotaMeasureDf['species_no'].dropna().unique()
        taxonSpeciesDf = pd.DataFrame([TaxonSpecies(spec).dict() for spec in self.channel_business.get_species(species_nos)])
        taxonSpeciesDf['year'] = year

        biotaMeasureDf = biotaMeasureDf.merge(taxonSpeciesDf,on='species_no', how='left')

        # Otolith
        measure_ids = biotaMeasureDf['measure_id'].unique()
        otolithList = []
        for ids_chunk in chunked(measure_ids, size=400):
            otol = self.channel_business.get_otolith(ids_chunk)
            if type(otol) == list:
                otolithList.extend(otol)
        otolithDf = pd.DataFrame(otolithList)
        otolithDf.drop(columns=['sample_id'], inplace=True)

        # Final MEASURE
        # TODO add count columnfr
        measureDf = biotaMeasureDf.merge(otolithDf,on='measure_id', how='left')

        # All missing values across numeric, datetime, and extension types are replaced with actual Python None.
        sampleDf = sampleDf.astype(object).where(pd.notna(sampleDf), None)
        populationDf = populationDf.astype(object).where(pd.notna(populationDf), None)

        # Use populationDf, this is CENSUS, all Mackerel fishing trips
        populationSampleDf = populationDf.merge(sampleDf, on='fishing_trip_id', how='left')
        populationSampleDf = populationSampleDf.astype(object).where(pd.notna(populationSampleDf), None)

        # Add sequence No to the Df
        populationSampleDf['sequence'] = populationSampleDf.sort_values('departure_date').reset_index().index + 1
        populationSampleDf['total_numer'] = len(populationSampleDf)
        populationSampleDf['sampled_numer'] = populationSampleDf['sample_id'].notna().sum()

        # Convert all timestamp columns to string / skip None
        # for col in sampleDf.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
        #     sampleDf[col] = sampleDf[col].apply(
        #         lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else None
        #     )

        # measureDf = measureDf.astype(object).where(measureDf.notna(measureDf), None)
        measureDf = measureDf.astype(object).where(pd.notna(measureDf), None)

        #
        # Design Tables ---------------------------------------------------------------------------------

        # Design / One Sample Design Record
        designDE = Design(year).pand()
        designReport = validate_dataframe(designDE, Design(year).validate())
        if dict_error(designReport):
            errors = True
            errorsHtml['design_errors'] = generate_html_from_dict(designReport, 'Design Validation')

        # Sampling Details / One Sampling Details Record
        samplingDetailsSD = SamplingDetails().pand()
        samplingDetailsReport = validate_dataframe(samplingDetailsSD, SamplingDetails().validate())
        if dict_error(samplingDetailsReport):
            errors = True
            errorsHtml['sampling_details_errors'] = generate_html_from_dict(samplingDetailsReport, 'Sampling Details Validation')

        #
        # Primary Sampling Units ------------------------------------------------------------------------

        # vessel Details record for all vessels sampled from
        vesselDetailsVD = pd.DataFrame([VesselDetails(ves).dict() for ves in vesselDf.to_dict(orient='records')])
        vesselDetailsVD['VDpower'] = vesselDetailsVD['VDpower'].astype(object).where(
            vesselDetailsVD['VDpower'].notna(),
            None
        )
        vesselDetailsReport = validate_dataframe(vesselDetailsVD, VesselDetails(vesselDf.to_dict(orient='records')[0]).validate())
        if dict_error(vesselDetailsReport):
            errors = True
            errorsHtml['vessel_details_errors'] = generate_html_from_dict(vesselDetailsReport, 'vessel Details Validation')

        # Fishing Trip / One record for each Fishing Trip - possible to get the fishing trip information from ADB
        fishingTripFT = pd.DataFrame([FishingTrip(samp).dict() for samp in populationSampleDf.to_dict(orient='records')])
        fishingTripReport = validate_dataframe(fishingTripFT, FishingTrip(populationSampleDf.to_dict(orient='records')[0]).validate())
        if dict_error(fishingTripReport):
            errors = True
            errorsHtml['fishing_trip_errors'] = generate_html_from_dict(fishingTripReport, 'Fishing Trip Validation')

        # Fishing Operation Like stations, many Fishing Operation for each Fishing Trip
        # TODO Núna er þetta ekki ein dict-lína heldur listi af dict-linum
        # TODO þarf að tengja station og sample saman í eina töflu

        fishingOperationFO = pd.DataFrame([FishingOperation(sampl).dict() for sampl in sampleDf.to_dict(orient='records')]).astype(object)
        # TODO hvað gerir þetta ?
        fishingOperationFO = fishingOperationFO.where(fishingOperationFO.notna(), None)
        fishingOperationReport = validate_dataframe(fishingOperationFO, FishingOperation(sampleDf.to_dict(orient='records')[0]).validate())
        if dict_error(fishingOperationReport):
            errors = True
            errorsHtml['fishing_operation_errors'] = generate_html_from_dict(fishingOperationReport, 'Fishing Operation Validation')

        # Individual Species / All Individual Species sampled in this Sample Design
        individualSpeciesIS = pd.DataFrame([IndividualSpecies(tax).dict() for tax in taxonSpeciesDf.to_dict(orient='records')])
        individualSpeciesReport = validate_dataframe(individualSpeciesIS, IndividualSpecies(taxonSpeciesDf.to_dict(orient='records')[0]).validate())
        if dict_error(individualSpeciesReport):
            errors = True
            errorsHtml['individual_species_errors'] = generate_html_from_dict(individualSpeciesReport, 'Individual Species Validation')

        # Species List / All Species sampled in this Sample Design
        speciesListSL = pd.DataFrame([SpeciesList(tax).dict() for tax in taxonSpeciesDf.to_dict(orient='records')])
        speciesListReport = validate_dataframe(speciesListSL, SpeciesList(taxonSpeciesDf.to_dict(orient='records')[0]).validate())
        if dict_error(speciesListReport):
            errors = True
            errorsHtml['species_list_errors'] = generate_html_from_dict(speciesListReport, 'Species List Validation')

        # Species Selection / All Species sampled in this Sample Design
        # TODO Sýnist hér þurfa færslu fyrir þær tegundir sem sýni er tekið af
        # TODO Sýnist ekki þurfa að gruppa á fishing_station_id hér, nægilegt að hafa sampla_id
        sampleMeasureUqDf = pd.DataFrame(pd.merge(sampleDf, measureDf.loc[measureDf['species_no']
                                                  .notnull()], on='sample_id')
                                         .drop_duplicates(subset=['fishing_station_id', 'sample_id', 'species_no'])[['fishing_station_id', 'sample_id', 'species_no']]
                                         .to_dict('records'))
        sampleMeasureUqDf = sampleMeasureUqDf.merge(taxonSpeciesDf, on='species_no', how='left')
        sampleMeasureUqDf['sequence'] = sampleMeasureUqDf.groupby(['fishing_station_id', 'sample_id'])['species_no'].rank(method='first').astype(int)

        speciesSelectionSS = pd.DataFrame([SpeciesSelection(tax).dict() for tax in sampleMeasureUqDf.to_dict(orient='records')])
        # Nan to None
        speciesSelectionSS = speciesSelectionSS.astype(object).where(pd.notna(speciesSelectionSS), None)
        speciesSelectionReport = validate_dataframe(speciesSelectionSS, SpeciesSelection(sampleMeasureUqDf.to_dict(orient='records')[0]).validate())
        if dict_error(speciesSelectionReport):
            errors = True
            errorsHtml['species_selection_errors'] = generate_html_from_dict(speciesSelectionReport, 'Species Selection Validation')

        # Sample
        # Like channel sample, but for each species and sex
        # TODO Færsla fyrir hvert sýni sem er tekið

        # sampleMeasureSexUq = pd.merge(sampleDf, measureDf.loc[measureDf['species_no'].notnull()], on='sample_id').drop_duplicates(subset=['sample_id', 'species_no','sex_no'])[['sample_id', 'species_no','sex_no']].to_dict('records')
        sampleMeasureSexUqDf = pd.merge(sampleDf, measureDf.loc[measureDf['species_no'].notnull()], on='sample_id').drop_duplicates(subset=['sample_id', 'species_no'])[['sample_id', 'species_no', 'worms_id']]
        # sampleMeasureSexUqDf['sequence'] = sampleMeasureSexUqDf.groupby('sample_id')['species_no'].rank(method='first').astype(int)
        sampleMeasureSexUqDf['sequence'] = (
                sampleMeasureSexUqDf.sort_values(['sample_id', 'species_no'])
                .reset_index(drop=True)
                .index + 1
        )
        sampleSA = pd.DataFrame([Sample(sam).dict() for sam in sampleMeasureSexUqDf.to_dict('records')])
        # Nan to None
        sampleSA = sampleSA.astype(object).where(pd.notna(sampleSA), None)

        sampleReport = validate_dataframe(sampleSA, Sample(sampleMeasureSexUqDf.to_dict(orient='records')[0]).validate())
        if dict_error(sampleReport):
            errors = True
            errorsHtml['sample_errors'] = generate_html_from_dict(sampleReport, 'Sample Validation')

        # Convert to numeric, set invalid parsing to NaN
        measureDf['length'] = pd.to_numeric(measureDf['length'], errors='coerce')
        # Convert to mm, numeric multiplication
        measureDf['length'] = 10*measureDf['length']

        # Frequency Measure / Length distributions
        # sampleMeasureLengthUq = pd.merge(channelSampleDf, biotaMeasureDf.loc[biotaMeasureDf['species_no'].notnull()], on='sample_id').drop_duplicates(subset=['sample_id', 'species_no','length'])[['sample_id', 'species_no','length']].to_dict('records')

        # TODO not do any frequency measures, only individual biological variable
        # # Group by sample_id, species_no, and length
        # frequencyDf = (
        #     measureDf
        #     .groupby(['sample_id', 'species_no', 'length'])
        #     .size()
        #     .reset_index(name='frequency')
        #     .sort_values(['sample_id', 'species_no', 'length'])
        # )
        #
        # # TODO sum count column for frequency
        # # frequencyDf = (
        # #     measureDf
        # #     .groupby(['sample_id', 'species_no', 'length'], as_index=False)['count']
        # #     .sum()
        # #     .reset_index(name='frequency')
        # #     .sort_values(['sample_id', 'species_no', 'length'])
        # # )
        #
        # frequencyMeasureFM = pd.DataFrame([FrequencyMeasure(freq).dict() for freq in frequencyDf.to_dict('records')])
        # frequencyMeasureReport = validate_dataframe(frequencyMeasureFM, FrequencyMeasure(frequencyDf.to_dict(orient='records')[0]).validate())
        # if dict_error(frequencyMeasureReport):
        #     errors = True
        #     errorsHtml['frequency_measure_errors'] = generate_html_from_dict(frequencyMeasureReport, 'Frequency Measure')

        # Biological Variable
        # Each measurement
        bv = []
        measureDf['tot_count'] = measureDf.groupby('sample_id')['sample_id'].transform('size')
        measureDf['grp_count'] = measureDf.groupby(['sample_id', 'measure_type'])['sample_id'].transform('size')
        for meas in measureDf.to_dict(orient='records'):
            if meas['measure_type'] == 'LEN' and meas['length'] != None:
                meas['measure'] = meas['length']
                meas['measure_unit'] = 'Lengthmm'
                meas['specimen_type'] = None
                bv.append(BiologicalVariable(meas, 'LengthTotal').dict())
            if meas['measure_type'] == 'OTOL' and meas['length'] != None:
                meas['measure'] = meas['length']
                meas['measure_unit'] = 'Lengthmm'
                meas['specimen_type'] = None
                bv.append(BiologicalVariable(meas, 'LengthTotal').dict())
            if meas['measure_type'] == 'OTOL' and meas['weight'] != None:
                meas['measure'] = meas['weight']
                meas['measure_unit'] = 'Weightg'
                meas['specimen_type'] = None
                bv.append(BiologicalVariable(meas, 'WeightMeasured').dict())
            if meas['measure_type'] == 'OTOL' and meas['age'] != None:
                meas['measure'] = meas['age']
                meas['measure_unit'] = 'Ageyear'
                meas['specimen_type'] = 'otolith'
                bv.append(BiologicalVariable(meas, 'Age').dict())

        biologicalVariableBV = pd.DataFrame(bv)
        measureDf['measure'] = None
        measureDf['measure_unit'] = None
        measureDf['specimen_type'] = None
        biologicalVariableBV = biologicalVariableBV.astype(object).where(pd.notna(biologicalVariableBV), None)
        biologicalVariableReport = validate_dataframe(biologicalVariableBV, BiologicalVariable(measureDf.to_dict(orient='records')[0], 'LengthTotal').validate())
        if dict_error(biologicalVariableReport):
            errors = True
            errorsHtml['biological_variable_errors'] = generate_html_from_dict(biologicalVariableReport, 'Biological Variable')

        # if errors:
        #     return {'return': -1}, errorsHtml

        # Write ALL
        for rec in vesselDetailsVD.to_dict('records'):
            vesselDetailsRes = self.insert('vessel_details', rec)

        for rec in individualSpeciesIS.to_dict('records'):
            individualSpeciesRes = self.insert('individual_species', rec)

        for rec in speciesListSL.to_dict('records'):
            speciesListRes = self.insert('species_list', rec)


        for rec in designDE.to_dict('records'):
            designRes = self.insert('design', rec)

        samplingDetailsSD['DEid'] = designRes['id']
        for rec in samplingDetailsSD.to_dict('records'):
            samplingDetailsRes = self.insert('sampling_details', rec)

        fishingTripFT['SDid'] = samplingDetailsRes['id']
        for rec in fishingTripFT.to_dict('records'):
            fishingTripRes = self.insert('fishing_trip', rec)

        for rec in fishingOperationFO.to_dict('records'):
            fishingOperationRes = self.insert('fishing_operation', rec)


        for rec in speciesSelectionSS.to_dict('records'):
            speciesSelectionRes = self.insert('species_selection', rec)

        # TODO constraint sample_sequence_uc, tekinn tímabundið af
        for rec in sampleSA.to_dict('records'):
            sampleRes = self.insert('sample', rec)

        # # TODO frequency measures not submitted, only individual biological variables like in the DB
        # for rec in frequencyMeasureFM.to_dict('records'):
        #     frequencyMeasureRes = self.insert('frequency_measure', rec)

        # TODO - comment out because of time
        for rec in biologicalVariableBV.to_dict('records'):
            biologicalVariableRes = self.insert('biological_variable', rec)

        return {'return': 0}


    def write_landing(self, cruiseDict):

        errors = False
        errorsHtml = {}

        year = cruiseDict['cruise'][-4:]
        date_from = '2024-06-02'
        date_to = '2024-06-04'

        ##
        ## Get all the data ---------------------------------------------------------------------------------

        # AGF-afladagbok

        # channel-Stations
        agfLandingsCol = ['cruise_id','station_id','station_date','latitude','longitude','vessel_no']
        agfLandingsDf = pd.DataFrame([AgfLandings(land).dict() for land in self.agf_business.get_landings(date_from, date_to)])

        # Find the ADB-Fishing Trip for all the channel-Landings
        # self.update_trip_info(channelStationDf)

        # vessel, first get registration_nos / Remove duplicate and None
        # registration_nos = channelStationDf['vessel_no'].dropna().unique()
        # vesselDf = pd.DataFrame([VesselVessel(ves).dict() for ves in self.vessel_business.get_vessel(registration_nos)])

        # # Merge with vessel on registration_no from Ladings
        # # TODO þar líkleaa ekki þetta join nema kannski fyrir vessel_id
        # channelStationDf = channelStationDf.merge(vesselDf[['registration_no', 'vessel_id']], left_on='vessel_no', right_on='registration_no', how='inner')
        # channelStationDf.drop(columns=['vessel_no'], inplace=True)
        #
        # # TODO spurning um að hraða þessu með því að ná í allar hafnir/eða þær sem þarf - með einu kalli - og join svo datasettin
        # port_nos = pd.unique(
        #     pd.concat([
        #         channelStationDf['departure_port_no'],
        #         channelStationDf['landing_port_no'],
        #         vesselDf['home_port_no'],
        #     ]).dropna()
        # )
        # harbourDf = pd.DataFrame([Harbour(port).dict() for port in self.get_harbour(port_nos)])
        #
        # # Merge on key departure_port_no
        # channelStationDf = channelStationDf.merge(harbourDf.rename(columns={'harbour':'departure_harbour'}), left_on='departure_port_no', right_on='port_no', how='left')
        # channelStationDf.drop(columns=['departure_port_no','port_no'], inplace=True)
        #
        # # Update 'departure_harbour' with values from merged 'harbour' column
        # # channelStationDf['departure_harbour'] = channelStationDf['harbour'].combine_first(
        # #     channelStationDf['departure_harbour'])
        # # Optionally drop extra columns from merge (like 'harbour' and 'port_no')
        # # channelStationDf.drop(columns=['harbour', 'port_no'], inplace=True)
        #
        # # Merge on key landing_port_no
        # channelStationDf = channelStationDf.merge(harbourDf.rename(columns={'harbour':'landing_harbour'}), left_on='landing_port_no', right_on='port_no', how='left')
        # channelStationDf.drop(columns=['landing_port_no','port_no'], inplace=True)
        #
        # # Update 'landing_harbour' with values from merged 'harbour' column
        # # channelStationDf['landing_harbour'] = channelStationDf['harbour'].combine_first(
        # #     channelStationDf['landing_harbour'])
        # # Optionally drop extra columns from merge (like 'harbour' and 'port_no')
        # # channelStationDf.drop(columns=['harbour', 'port_no'], inplace=True)
        #
        # # Merge on key home_port_no
        # vesselDf = vesselDf.merge(harbourDf.rename(columns={'harbour':'home_harbour'}), left_on='home_port_no', right_on='port_no', how='left')
        # vesselDf.drop(columns=['home_port_no','port_no'], inplace=True)
        # vesselDf['year'] = year
        #
        # # TODO need to get a shapefile/geopackage/... for the areas
        # # TODO remove # lessi setning á að vera með, tekin út vegna slow
        # # TODO remove ? um að færa aftar og reikna á adb-lag/long
        # channelStationDf['area'] = channelStationDf.apply(
        #     lambda row: self.get_area(row['latitude'],row['longitude'] or {}), axis=1
        # )
        #
        # # Find the ADB-Fishing Trips for all the Landings
        # fishing_trip_ids = channelStationDf['fishing_trip_id'].dropna().unique()
        #
        # # gear, first get isscfg_no / Remove duplicate and None
        # fishing_gear_nos = adbFishingStationDf['fishing_gear_no'].dropna().unique()
        # fishingGearDf = pd.DataFrame([GearFishingGear(fg).dict() for fg in self.gear_business.get_fishing_gear(fishing_gear_nos)])
        # isscfg_nos = fishingGearDf['isscfg_no'].dropna().unique()
        # isscfgDf = pd.DataFrame([GearIsscfg(iss).dict() for iss in self.gear_business.get_isscfg(isscfg_nos)])
        # fishingGearDf = fishingGearDf.merge(isscfgDf.rename(columns={'stand_no':'fao_gear_code'}), on='isscfg_no', how='inner')
        #
        # # Merge with Fishing gear information
        # fishing_station_ids = adbFishingStationDf['fishing_station_id'].dropna().unique()
        # adbTrawlAndSeineNetDf = pd.DataFrame([AdbTrawlAndSeineNet(stat).dict() for stat in self.adb_business.get_trawl_and_seine_net(fishing_station_ids)])
        # adbFishingStationDf = adbFishingStationDf.merge(adbTrawlAndSeineNetDf[['fishing_station_id','mesh_size']], on='fishing_station_id', how='inner')
        #
        # # Merge with gear on isscfg_no from sampleDf
        # sampleDf = sampleDf.merge(fishingGearDf[['fishing_gear_no','fao_gear_code']], on='fishing_gear_no', how='left')
        #
        # # One get for each combination of area, stand_no, target species and mesh size
        # metierDf = sampleDf[['area','fao_gear_code','target_assemblage','mesh_size']]
        # metierDf = metierDf[['area','fao_gear_code','target_assemblage','mesh_size']].dropna(subset=['area','fao_gear_code','target_assemblage','mesh_size']).drop_duplicates()
        #
        # if not metierDf.empty:
        #     metierDf['metier6']  = metierDf.apply( lambda row: self.get_metier(
        #                                                 row['area'], row['fao_gear_code'], row['target_assemblage'], row['mesh_size']
        #                                             ) if pd.notna(row['area']) and pd.notna(row['fao_gear_code'])
        #                                                  and pd.notna(row['target_assemblage']) and pd.notna(row['mesh_size'])
        #                                             else None,
        #                                             axis=1
        #                                         )
        # # sampleDf.drop(columns=['metier6'],inplace=True)
        # sampleDf = sampleDf.merge(metierDf, on=['area','fao_gear_code','target_assemblage','mesh_size'], how='left')
        #
        # # Measure
        # sample_ids = sampleDf['sample_id'].unique()
        # biotaMeasureDf = pd.DataFrame([BiotaMeasure(meas).dict() for meas in self.channel_business.get_measure(sample_ids)])
        # biotaMeasureDf['species_no'] = biotaMeasureDf['species_no'].astype('Int64')
        #
        # # Species, first get species_no / remove duplicate and None
        # species_nos = biotaMeasureDf['species_no'].dropna().unique()
        # taxonSpeciesDf = pd.DataFrame([TaxonSpecies(spec).dict() for spec in self.channel_business.get_species(species_nos)])
        # taxonSpeciesDf['year'] = year
        #
        # biotaMeasureDf = biotaMeasureDf.merge(taxonSpeciesDf,on='species_no', how='left')
        #
        # # All missing values across numeric, datetime, and extension types are replaced with actual Python None.
        # sampleDf = sampleDf.astype(object).where(pd.notna(sampleDf), None)
        #
        # # Convert all timestamp columns to string / skip None
        # # for col in sampleDf.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
        # #     sampleDf[col] = sampleDf[col].apply(
        # #         lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else None
        # #     )
        #
        # # measureDf = measureDf.astype(object).where(measureDf.notna(measureDf), None)
        # measureDf = measureDf.astype(object).where(pd.notna(measureDf), None)

        #
        # Landings Table ---------------------------------------------------------------------------------

        # Landing / One record for each Fishing Trip - possible to get the fishing trip information from ADB
        landingsCL = pd.DataFrame([CommercialLanding(land).dict() for land in agfLandingsDf.to_dict(orient='records')])
        landingsReport = validate_dataframe(landingsCL, CommercialLanding(agfLandingsDf.to_dict(orient='records')[0]).validate())
        if dict_error(landingsReport):
            errors = True
            errorsHtml['commercial_landing_errors'] = generate_html_from_dict(landingsReport, 'Commercial Landing Validation')

        if errors:
            return {'return': -1}, errorsHtml

        # Write ALL
        for rec in landingsCL.to_dict('records'):
            landingRes = self.insert('commercial_landing', rec)

        return {'return': 0}


    def write_effort(self, cruiseDict):

        errors = False
        errorsHtml = {}

        year = cruiseDict['cruise'][-4:]
        landing_from = '2024-06-02'
        landing_to = '2024-06-04'

        ##
        ## Get all the data ---------------------------------------------------------------------------------

        # channel-Cruise
        # channelCruiseDf = ChannelCruise(self.channel_business.get_cruise(cruiseDict['cruise'])).pand()

        # channel-Stations
        adbFishingTripsCol = ['cruise_id','station_id','station_date','latitude','longitude','vessel_no']
        adbFishingTripsDf = pd.DataFrame([AdbFishingTrip(trip).dict() for trip in self.adb_business.get_fishing_trips(landing_from, landing_to)])

        #  Merge with cruise on cruise_id from stationDf
        # channelStationDf = channelStationDf.merge(channelCruiseDf[
        #     ['cruise_id','departure', 'arrival']
        #     ].rename(columns={'departure':'departure_date','arrival':'arrival_date'}), on='cruise_id', how='inner')

        # # Find the ADB-Fishing Trip for all the channel-Stations
        # self.update_trip_info(channelStationDf)
        #
        # # vessel, first get registration_nos / Remove duplicate and None
        # registration_nos = channelStationDf['vessel_no'].dropna().unique()
        # vesselDf = pd.DataFrame([VesselVessel(ves).dict() for ves in self.vessel_business.get_vessel(registration_nos)])
        #
        # # Merge with vessel on registration_no from sampleDf
        # # TODO þar líkleaa ekki þetta join nema kannski fyrir vessel_id
        # channelStationDf = channelStationDf.merge(vesselDf[['registration_no', 'vessel_id']], left_on='vessel_no', right_on='registration_no', how='inner')
        # channelStationDf.drop(columns=['vessel_no'], inplace=True)
        #
        # # TODO spurning um að hraða þessu með því að ná í allar hafnir/eða þær sem þarf - með einu kalli - og join svo datasettin
        # port_nos = pd.unique(
        #     pd.concat([
        #         channelStationDf['departure_port_no'],
        #         channelStationDf['landing_port_no'],
        #         vesselDf['home_port_no'],
        #     ]).dropna()
        # )
        # harbourDf = pd.DataFrame([Harbour(port).dict() for port in self.get_harbour(port_nos)])
        #
        # # Merge on key departure_port_no
        # channelStationDf = channelStationDf.merge(harbourDf.rename(columns={'harbour':'departure_harbour'}), left_on='departure_port_no', right_on='port_no', how='left')
        # channelStationDf.drop(columns=['departure_port_no','port_no'], inplace=True)
        #
        # # Update 'departure_harbour' with values from merged 'harbour' column
        # # channelStationDf['departure_harbour'] = channelStationDf['harbour'].combine_first(
        # #     channelStationDf['departure_harbour'])
        # # Optionally drop extra columns from merge (like 'harbour' and 'port_no')
        # # channelStationDf.drop(columns=['harbour', 'port_no'], inplace=True)
        #
        # # Merge on key landing_port_no
        # channelStationDf = channelStationDf.merge(harbourDf.rename(columns={'harbour':'landing_harbour'}), left_on='landing_port_no', right_on='port_no', how='left')
        # channelStationDf.drop(columns=['landing_port_no','port_no'], inplace=True)
        #
        # # Update 'landing_harbour' with values from merged 'harbour' column
        # # channelStationDf['landing_harbour'] = channelStationDf['harbour'].combine_first(
        # #     channelStationDf['landing_harbour'])
        # # Optionally drop extra columns from merge (like 'harbour' and 'port_no')
        # # channelStationDf.drop(columns=['harbour', 'port_no'], inplace=True)
        #
        # # Merge on key home_port_no
        # vesselDf = vesselDf.merge(harbourDf.rename(columns={'harbour':'home_harbour'}), left_on='home_port_no', right_on='port_no', how='left')
        # vesselDf.drop(columns=['home_port_no','port_no'], inplace=True)
        # vesselDf['year'] = year
        #
        # # TODO need to get a shapefile/geopackage/... for the areas
        # # TODO remove # lessi setning á að vera með, tekin út vegna slow
        # # TODO remove ? um að færa aftar og reikna á adb-lag/long
        # channelStationDf['area'] = channelStationDf.apply(
        #     lambda row: self.get_area(row['latitude'],row['longitude'] or {}), axis=1
        # )
        #
        # # Sample
        # station_ids = channelStationDf['station_id'].unique()
        # channelSampleCol = ['station_id', 'sample_id', 'target_assemblage']
        # channelSampleDf = pd.DataFrame([ChannelSample(samp).dict() for samp in self.channel_business.get_sample(station_ids)], columns=channelSampleCol)
        #
        # # TODO Áður en farið er að uppfæra fieldin i station/sample þarf að finna réttu stöðin í adb.fishing_station_id
        # # TODO það er gert með: match_closest_station
        # # TODO þegar búið er að finna stöðina má uppfæra fieldin
        #
        # # TODO First get all station for all the trips
        #
        # # Merge station and sample on station_id
        # channelStationSampleDf = channelStationDf.merge(channelSampleDf, on='station_id', how='inner')
        #
        # # Find the ADB-Fishing Trips for all the Sample taken
        # fishing_trip_ids = channelStationDf['fishing_trip_id'].dropna().unique()
        #
        # # Find the ADB-Fishing Stations for all the Fishing Trips
        # adbFishingStationDf = pd.DataFrame([AdbFishingStation(stat).dict() for stat in self.adb_business.get_fishing_station(fishing_trip_ids)])
        #
        # # gear, first get isscfg_no / Remove duplicate and None
        # fishing_gear_nos = adbFishingStationDf['fishing_gear_no'].dropna().unique()
        # fishingGearDf = pd.DataFrame([GearFishingGear(fg).dict() for fg in self.gear_business.get_fishing_gear(fishing_gear_nos)])
        # isscfg_nos = fishingGearDf['isscfg_no'].dropna().unique()
        # isscfgDf = pd.DataFrame([GearIsscfg(iss).dict() for iss in self.gear_business.get_isscfg(isscfg_nos)])
        # fishingGearDf = fishingGearDf.merge(isscfgDf.rename(columns={'stand_no':'fao_gear_code'}), on='isscfg_no', how='inner')
        #
        # # Merge with Fishing gear information
        # fishing_station_ids = adbFishingStationDf['fishing_station_id'].dropna().unique()
        # adbTrawlAndSeineNetDf = pd.DataFrame([AdbTrawlAndSeineNet(stat).dict() for stat in self.adb_business.get_trawl_and_seine_net(fishing_station_ids)])
        # adbFishingStationDf = adbFishingStationDf.merge(adbTrawlAndSeineNetDf[['fishing_station_id','mesh_size']], on='fishing_station_id', how='inner')
        #
        #
        # # Merge with station/sample
        # # TODO til bæði mesh_size_x og mesh_size_y. ? um að laga það
        # # channelStationSampleDf.drop(columns=['mesh_size'],inplace=True)
        # channelStationSampleDf = channelStationSampleDf.merge(adbFishingStationDf[
        #     ['fishing_trip_id', 'fishing_station_id', 'fishing_gear_no', 'fishing_start', 'fishing_end', 'latitude', 'longitude', 'latitude_end', 'longitude_end', 'mesh_size']
        #     ].rename(columns={'latitude':'tow_latitude','latitude_end':'tow_latitude_end','longitude':'tow_longitude','longitude_end':'tow_longitude_end'})
        #     , on='fishing_trip_id', how='left')
        # channelStationSampleDf['mesh_size'] = channelStationSampleDf['mesh_size'].astype('Int64')
        # channelStationSampleDf['fishing_gear_no'] = channelStationSampleDf['fishing_gear_no'].astype('Int64')
        #
        # # Find the nearest station to sample time and location
        # channelStationSampleDf = match_closest_station(channelStationSampleDf, time_weight=0.5)
        #
        # # Final SAMPLE
        # # TODO líka að taka þau sample senm eiga ekki fishing station (MAKR-2024 þá tapast eitt sýni vegna þessa, líklegast í næstu setn.)
        # # TODO sko það þarf að taka eitt tripDf fyrir allar ferðirnar því það geta verið fleri en eitt sample per trip, en það er það ekki í MAKR-2024
        # sampleDf = channelStationSampleDf[(channelStationSampleDf['scaled_score'] == 1.0) | (channelStationSampleDf['scaled_score'].isna())]
        #
        # # Merge with gear on isscfg_no from sampleDf
        # sampleDf = sampleDf.merge(fishingGearDf[['fishing_gear_no','fao_gear_code']], on='fishing_gear_no', how='left')
        #
        # # One get for each combination of area, stand_no, target species and mesh size
        # metierDf = sampleDf[['area','fao_gear_code','target_assemblage','mesh_size']]
        # metierDf = metierDf[['area','fao_gear_code','target_assemblage','mesh_size']].dropna(subset=['area','fao_gear_code','target_assemblage','mesh_size']).drop_duplicates()
        #
        # if not metierDf.empty:
        #     metierDf['metier6']  = metierDf.apply( lambda row: self.get_metier(
        #                                                 row['area'], row['fao_gear_code'], row['target_assemblage'], row['mesh_size']
        #                                             ) if pd.notna(row['area']) and pd.notna(row['fao_gear_code'])
        #                                                  and pd.notna(row['target_assemblage']) and pd.notna(row['mesh_size'])
        #                                             else None,
        #                                             axis=1
        #                                         )
        # # sampleDf.drop(columns=['metier6'],inplace=True)
        # sampleDf = sampleDf.merge(metierDf, on=['area','fao_gear_code','target_assemblage','mesh_size'], how='left')
        #
        # # Measure
        # sample_ids = sampleDf['sample_id'].unique()
        # biotaMeasureDf = pd.DataFrame([BiotaMeasure(meas).dict() for meas in self.channel_business.get_measure(sample_ids)])
        # biotaMeasureDf['species_no'] = biotaMeasureDf['species_no'].astype('Int64')
        #
        # # Species, first get species_no / remove duplicate and None
        # species_nos = biotaMeasureDf['species_no'].dropna().unique()
        # taxonSpeciesDf = pd.DataFrame([TaxonSpecies(spec).dict() for spec in self.channel_business.get_species(species_nos)])
        # taxonSpeciesDf['year'] = year
        #
        # biotaMeasureDf = biotaMeasureDf.merge(taxonSpeciesDf,on='species_no', how='left')
        #
        # # Otolith
        # measure_ids = biotaMeasureDf['measure_id'].unique()
        # otolithList = []
        # for ids_chunk in chunked(measure_ids, size=400):
        #     otol = self.channel_business.get_otolith(ids_chunk)
        #     if type(otol) == list:
        #         otolithList.extend(otol)
        # otolithDf = pd.DataFrame(otolithList)
        # otolithDf.drop(columns=['sample_id'], inplace=True)
        #
        # # Final MEASURE
        # measureDf = biotaMeasureDf.merge(otolithDf,on='measure_id', how='left')
        #
        # # All missing values across numeric, datetime, and extension types are replaced with actual Python None.
        # sampleDf = sampleDf.astype(object).where(pd.notna(sampleDf), None)
        #
        # # Convert all timestamp columns to string / skip None
        # # for col in sampleDf.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
        # #     sampleDf[col] = sampleDf[col].apply(
        # #         lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else None
        # #     )
        #
        # # measureDf = measureDf.astype(object).where(measureDf.notna(measureDf), None)
        # measureDf = measureDf.astype(object).where(pd.notna(measureDf), None)

        #
        # Effort Table ---------------------------------------------------------------------------------

        effortCE = pd.DataFrame([CommercialEffort(eff).dict() for eff in adbFishingTripsDf.to_dict(orient='records')])
        effortReport = validate_dataframe(effortCE, CommercialEffort(adbFishingTripsDf.to_dict(orient='records')[0]).validate())
        if dict_error(effortReport):
            errors = True
            errorsHtml['commercial_effort_errors'] = generate_html_from_dict(effortReport, 'Commercial Effort Validation')

        # if errors:
        #     return {'return': -1}, errorsHtml

        # Write ALL
        for rec in effortCE.to_dict('records'):
            effortRes = self.insert('commercial_effort', rec)

        return {'return': 0}



    def write_file(self, file_name, file_type):

        # Records read from DB
        # Suppost tables
        vessel_details = self.select('vessel_details')
        vessel_detailsDf = pd.DataFrame(vessel_details, columns=VesselDetails(None).columns())
        species_list = self.select('species_list')
        species_listDf = pd.DataFrame(species_list, columns=SpeciesList(None).columns())
        individual_species = self.select('individual_species')
        individual_speciesDf = pd.DataFrame(individual_species, columns=IndividualSpecies(None).columns())

        # Upper Hierarchy
        design = self.select('design')
        designDf = pd.DataFrame(design, columns=Design(None).columns())

        sampling_details = self.select('sampling_details')
        sampling_detailsDf = pd.DataFrame(sampling_details, columns=SamplingDetails(True).columns())

        fishing_trip = self.select('fishing_trip')
        fishing_tripDf = pd.DataFrame(fishing_trip, columns=FishingTrip(None).columns())

        fishing_operation = self.select('fishing_operation')
        fishing_operationDf = pd.DataFrame(fishing_operation, columns=FishingOperation(None).columns())

        species_selection = self.select('species_selection')
        species_selectionDf = pd.DataFrame(species_selection, columns=SpeciesSelection(None).columns())

        sample = self.select('sample')
        sampleDf = pd.DataFrame(sample, columns=Sample(None).columns())

        # Lower Hierarchy
        # sample = self.select('frequency_measure')
        biological_variable = self.select('biological_variable')
        biological_variableDf = pd.DataFrame(biological_variable, columns=BiologicalVariable(None).columns())
        biological_variableDf = biological_variableDf.astype({
            'bvnumbertotal': 'Int64',
            'bvnumbersampled': 'Int64'
        })

        if file_type == 'csv':
            return convert_to_csv(vessel_detailsDf,
                                  species_listDf,
                                  individual_speciesDf,
                                  designDf,
                                  sampling_detailsDf,
                                  fishing_tripDf,
                                  fishing_operationDf,
                                  species_selectionDf,
                                  sampleDf,
                                  biological_variableDf,
                                  file_name)
        elif file_type == 'xml':
            return convert_to_xml(designDf,
                                  vessel_details,
                                  sampling_detailsDf,
                                  fishing_tripDf,
                                  fishing_operationDf,
                                  species_selectionDf,
                                  sampleDf,
                                  biological_variableDf)


import pandas as pd
import csv

def convert_to_csv(
    vessel_detailsDf: pd.DataFrame,
    species_listDf: pd.DataFrame,
    individual_speciesDf: pd.DataFrame,
    designDf: pd.DataFrame,
    sampling_detailsDf: pd.DataFrame,
    fishing_tripDf: pd.DataFrame,
    fishing_operationDf: pd.DataFrame,
    species_selectionDf: pd.DataFrame,
    sampleDf: pd.DataFrame,
    biological_variableDf: pd.DataFrame,
    file_name: str,  # base name for files; outputs: f"{name}_HVD.csv", f"{name}_HSL.csv", f"{name}_H2.csv"
) -> None:
    """
    Writes three CSV files with no header. For each DF, only columns from the first
    '*recordtype' column (case-insensitive, name endswith 'recordtype') to the end are written.
    Earlier columns (like ids) are dropped from the output.

    - {file_name}_HVD.csv: vessel_detailsDf
    - {file_name}_HSL.csv: species_listDf then individual_speciesDf (stacked)
    - {file_name}_H2.csv : hierarchical, depth-first:
        designDf → sampling_detailsDf → fishing_tripDf → fishing_operationDf
                 → species_selectionDf → sampleDf → biological_variableDf
    """

    def cols_from_recordtype(df: pd.DataFrame):
        cols = list(df.columns)
        idx = next((i for i, c in enumerate(cols) if str(c).lower().endswith("recordtype")), None)
        if idx is None:
            raise ValueError("No '*recordtype' column found (name must end with 'recordtype').")
        return cols[idx:]

    def write_df_rows(writer, df: pd.DataFrame, keep_cols):
        for _, row in df.iterrows():
            vals = [row.get(c, None) for c in keep_cols]
            writer.writerow(["" if pd.isna(v) else v for v in vals])

    # ---------- HVD ----------
    hvd_path = f"{file_name}_HVD.csv"
    keep_vessel = cols_from_recordtype(vessel_detailsDf)
    with open(hvd_path, "w", newline="", encoding="utf-8") as f:
        hvd_writer = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        write_df_rows(hvd_writer, vessel_detailsDf, keep_vessel)

    # ---------- HSL (species_list then individual_species) ----------
    hsl_path = f"{file_name}_HSL.csv"
    keep_species_list       = cols_from_recordtype(species_listDf)
    keep_individual_species = cols_from_recordtype(individual_speciesDf)
    with open(hsl_path, "w", newline="", encoding="utf-8") as f:
        hsl_writer = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        write_df_rows(hsl_writer, species_listDf, keep_species_list)
        write_df_rows(hsl_writer, individual_speciesDf, keep_individual_species)

    # ---------- H2 (hierarchical, depth-first) ----------
    # group children using full DFs (with ids intact)
    sd_by_deid = {k: g for k, g in sampling_detailsDf.groupby("deid", sort=False)}
    ft_by_sdid = {k: g for k, g in fishing_tripDf.groupby("sdid", sort=False)}
    fo_by_ftid = {k: g for k, g in fishing_operationDf.groupby("ftid", sort=False)}
    ss_by_foid = {k: g for k, g in species_selectionDf.groupby("foid", sort=False)}
    sa_by_ssid = {k: g for k, g in sampleDf.groupby("ssid", sort=False)}
    bv_by_said = {k: g for k, g in biological_variableDf.groupby("said", sort=False)}

    keep_design            = cols_from_recordtype(designDf)
    keep_sampling_details  = cols_from_recordtype(sampling_detailsDf)
    keep_fishing_trip      = cols_from_recordtype(fishing_tripDf)
    keep_fishing_operation = cols_from_recordtype(fishing_operationDf)
    keep_species_selection = cols_from_recordtype(species_selectionDf)
    keep_sample            = cols_from_recordtype(sampleDf)
    keep_biological_var    = cols_from_recordtype(biological_variableDf)

    h2_path = f"{file_name}_H2.csv"
    with open(h2_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)

        def write_row(series: pd.Series, keep_cols):
            vals = [series.get(c, None) for c in keep_cols]
            writer.writerow(["" if pd.isna(v) else v for v in vals])

        for _, d in designDf.iterrows():
            write_row(d, keep_design)

            for _, sd in sd_by_deid.get(d["deid"], pd.DataFrame()).iterrows():
                write_row(sd, keep_sampling_details)

                for _, ft in ft_by_sdid.get(sd["sdid"], pd.DataFrame()).iterrows():
                    write_row(ft, keep_fishing_trip)

                    for _, fo in fo_by_ftid.get(ft["ftid"], pd.DataFrame()).iterrows():
                        write_row(fo, keep_fishing_operation)

                        for _, ss in ss_by_foid.get(fo["foid"], pd.DataFrame()).iterrows():
                            write_row(ss, keep_species_selection)

                            for _, sa in sa_by_ssid.get(ss["ssid"], pd.DataFrame()).iterrows():
                                write_row(sa, keep_sample)

                                for _, bv in bv_by_said.get(sa["said"], pd.DataFrame()).iterrows():
                                    write_row(bv, keep_biological_var)

def convert_to_xml( designDf,
                    sampling_detailsDf,
                    fishing_tripDf,
                    fishing_operationDf,
                    species_selectionDf,
                    sampleDf,
                    biological_variableDf,
                  ):

    # vesselDetailDf = pd.DataFrame(vessel_details)
    # df_cruise = pd.DataFrame([cruise.json()])
    # df_haul = pd.DataFrame(haul.json())
    # df_catch = pd.DataFrame(catch.json())
    # df_biology = pd.DataFrame(biology.json())
    # df_vocabulary = pd.DataFrame(vocabulary())
    # Convert to XML
    # return create_nested_xml(df_vocabulary, df_cruise, df_haul, df_catch, df_biology)
    return True

def nautical_miles(distance: float) -> float:
    return distance * 1852


def haulnumber(station_no: int, sample_no: int) -> int:
    return 10*station_no + nvl(sample_no)


def lengthcode(length: float) -> str:
    return 'mm' if nvl(length) > 0 else None


def lengthclass(length: float) -> int:
    return round(10*length) if length != None and length != '' else None


def weightunit(weight: float) -> str:
    return 'gr' if nvl(weight) > 0 else None


def sex(sex_no: int) -> str:
    if sex_no == 1:
        return 'M'
    elif sex_no == 2:
        return 'F'
    else:
        return None


def agesource(age: int, otolith_type: str) -> str:
    if age is not None:
        if otolith_type == 'OTOL':
            return 'Otolith'
        elif otolith_type == 'SCAL':
            return 'Scale'
        elif otolith_type == 'VERT':
            return 'Vertebra'
        else:
            return None
    else:
        return None


def validate_dataframe(df: pd.DataFrame, schema: list):
    """
    Validates a Pandas DataFrame based on a given schema.

    Parameters:
        df (pd.DataFrame): The DataFrame to validate.
        schema (list): A list of dictionaries defining expected column names, data types, and constraints.
            Example schema:
            [
                {"name": "column_name", "dtype": "int", "not_null": True, "allowed_values": [1, 2, 3], "range": (0, 100)}
            ]

    Returns:
        dict: A report containing validation results.
    """
    validation_report = {"missing_columns": [],
                         "type_errors": {},
                         "null_errors": {},
                         "value_errors": {},
                         "range_errors": {},
                         "computed_errors": {}}
    # print(schema)

    # Convert schema to dictionary format for easy lookup
    schema_dict = {col["name"]: col for col in schema}

    # Convert empty strings and pd.NA to None to ensure they are treated as missing values
    # FutureWarning: DataFrame.applymap has been deprecated. Use DataFrame.map instead.
    # df = df.applymap(lambda x: None if pd.isna(x) or x == "" else x)
    df = df.map(lambda x: None if pd.isna(x) or x == "" else x)

    # Check for missing columns
    for col in schema_dict.keys():
        if col not in df.columns:
            validation_report["missing_columns"].append(col)

    # Check column data types, null values, allowed values, and range constraints
    for col, rules in schema_dict.items():
        if col in df.columns:

            # Check null values and enforce not_null constraint
            if rules.get("not_null", False):
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    validation_report["null_errors"][col] = f"{null_count} Null values"

            # Skip further checks if column is completely empty
            if df[col].dropna().empty:
                continue

            # Convert column to expected dtype if possible
            expected_dtype = rules.get("dtype")
            type_error = None
            try:
                if expected_dtype == "int":
                    non_numeric_values = df[col].dropna().apply(
                        lambda x: x if isinstance(x, str) and not x.isdigit() else None).dropna().unique()
                    float_values = df[col].dropna().apply(
                        lambda x: x if isinstance(x, float) and not x.is_integer() else None).dropna().unique()
                    if len(non_numeric_values) > 0:
                        type_error = f"Invalid value(s) {list(non_numeric_values)} found in int field"
                    elif len(float_values) > 0:
                        type_error = f"Float value(s) {list(float_values)} found in int field"
                    df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')
                elif expected_dtype == "float":
                    non_numeric_values = df[col].dropna().apply(
                        lambda x: x if isinstance(x, str) and not x.replace('.', '',1)
                                                                   .replace('-','',2)
                                                                   .replace('E','',1)
                                                                   .isdigit() else None).dropna().unique()
                    if len(non_numeric_values) > 0:
                        type_error = f"Invalid value(s) {list(non_numeric_values)} found in float field"
                    df[col] = pd.to_numeric(df[col], errors='coerce', downcast='float')
                elif expected_dtype == "str":
                    df[col] = df[col].astype(str)
                else:
                    df[col] = df[col].astype(expected_dtype)
            except ValueError:
                type_error = f"Could not convert to {expected_dtype}"

            # Report type errors only if relevant
            if type_error:
                validation_report["type_errors"][col] = type_error

            # Check allowed values
            if "allowed_values" in rules:
                invalid_values = df[~df[col].isin([val for val in rules["allowed_values"] if val is not None])][
                    col].dropna().unique()
                invalid_values = [val for val in invalid_values if
                                  val not in [None, "None"]]  # Ensure None is not included
                if len(invalid_values) > 0:
                    validation_report["value_errors"][col] = invalid_values

            # Check range constraints
            if "range" in rules and pd.api.types.is_numeric_dtype(df[col]):
                min_val, max_val = rules["range"]
                out_of_range_values = df[(df[col] < min_val) | (df[col] > max_val)][col].dropna().tolist()
                if len(out_of_range_values) > 0:
                    validation_report["range_errors"][col] = f"Out of range values: {out_of_range_values}"

    # # Haul, computed validations
    # if all(col in df.columns for col in ["StartTime", "Duration", "StartLatitude", "StartLongitude", "StopLatitude", "StopLongitude", "Distance", "SpeedGround"]):
    #     validation_report["computed_errors"].update(validate_haul(df))
    #
    # # Biology, computed validations
    # if all(col in df.columns for col in ["LengthCode", "IndividualWeight", "SpeciesCode"]):
    #     validation_report["computed_errors"].update(validate_biology(df))

    return validation_report


def dict_error(error_dict):
    if error_dict.get("missing_columns", []):
        return True

    for error_type in ["type_errors", "null_errors"]:
        if error_dict.get(error_type, {}):
            return True

    for error_type in ["value_errors", "range_errors", "computed_errors"]:
        fields = error_dict.get(error_type, {})
        if isinstance(fields, dict):
            for values in fields.values():
                if any(values):  # If any list inside is not empty, there is an error
                    return True

    return False


def generate_html_from_dict(error_dict, title="Dictionary Display"):
    error_type_labels = {
        "missing_columns": "Missing columns",
        "type_errors": "Type validation",
        "null_errors": "Null validation",
        "value_errors": "Value validation",
        "range_errors": "Range validation",
        "computed_errors": "Computed validation",
    }

    error_types = list(error_type_labels.keys())

    html = f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid black;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <h2>{title}</h2>
    <table>
        <tr>
            <th>Type</th>
            <th>Field</th>
            <th>Values</th>
        </tr>"""

    for error_type in error_types:
        fields = error_dict.get(error_type, {})
        readable_error_type = error_type_labels[error_type]

        if error_type == "missing_columns":
            if fields:
                first_row = True
                for column in fields:
                    if first_row:
                        html += f"""
        <tr>
            <td rowspan='{len(fields)}'>{readable_error_type}</td>
            <td>{column}</td>
            <td></td>
        </tr>"""
                        first_row = False
                    else:
                        html += f"""
        <tr>
            <td>{column}</td>
            <td></td>
        </tr>"""
            else:
                html += f"""
        <tr>
            <td>{readable_error_type}</td>
            <td></td>
            <td></td>
        </tr>"""
        elif isinstance(fields, dict) and fields:
            first_row = True
            for field, values in fields.items():
                values_str = " ".join(str(v) for v in values) if isinstance(values, list) else str(values)
                values_str = values_str.replace("[", "").replace("]", "").replace("'", "")
                if first_row:
                    html += f"""
        <tr>
            <td rowspan='{len(fields)}'>{readable_error_type}</td>
            <td>{field}</td>
            <td>{values_str}</td>
        </tr>"""
                    first_row = False
                else:
                    html += f"""
        <tr>
            <td>{field}</td>
            <td>{values_str}</td>
        </tr>"""
        else:
            html += f"""
        <tr>
            <td>{readable_error_type}</td>
            <td></td>
            <td></td>
        </tr>"""

    html += """
    </table>
</body>
</html>"""

    # print(html.replace("\n", ""))
    return html.replace("\n", "")
