#!/usr/local/bin/python3
# coding: utf-8

from lxml import etree


def create_nested_xml(df_vocabulary, df_cruise, df_haul, df_catch, df_biology):
    """
    Create a nested XML structure from master and detail DataFrames.
    :return: An XML string.
    """

    # Create the root element
    root = etree.Element('Biotic')

    for _, vocabulary_row in df_vocabulary.iterrows():
        # Create a master record element
        vocabulary_elem = etree.SubElement(root, 'Vocabulary')

        # For each column in the Vocabulary row, create a IDREF element
        for vocabulary_col in df_vocabulary.columns:
            # Example: <ID>1</ID>, <Name>Alpha</Name>, etc.
            child = etree.SubElement(vocabulary_elem, vocabulary_col)

            # Crusie
            if vocabulary_col == 'Survey':
                for tag in df_cruise[df_cruise['Survey'] != '']['Survey'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'Country':
                for tag in df_cruise[df_cruise['Country'] != '']['Country'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'Platform':
                for tag in df_cruise[df_cruise['Platform'] != '']['Platform'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'Organisation':
                for tag in df_cruise[df_cruise['Organisation'] != '']['Organisation'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)

            # Haul
            elif vocabulary_col == 'gear':
                for tag in df_haul[df_haul['gear'] != '']['gear'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'HaulValidity':
                for tag in df_haul[df_haul['Validity'] != '']['Validity'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'Stratum':
                for tag in df_haul[df_haul['Stratum'] != '']['Stratum'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)

            # Catch
            elif vocabulary_col == 'DataType':
                for tag in df_catch[df_catch['DataType'] != '']['DataType'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'SpeciesCode':
                for tag in df_catch[df_catch['SpeciesCode'] != '']['SpeciesCode'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'SpeciesValidity':
                for tag in df_catch[df_catch['SpeciesValidity'] != '']['SpeciesValidity'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)

            # Biology
            elif vocabulary_col == 'StockCode':
                for tag in df_biology[df_biology['StockCode'] != '']['StockCode'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'GeneticPopulationCode':
                for tag in df_biology[df_biology['GeneticPopulationCode'] != '']['GeneticPopulationCode'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'LengthCode':
                for tag in df_biology[df_biology['LengthCode'] != '']['LengthCode'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'WeightUnit':
                for tag in df_biology[df_biology['WeightUnit'] != '']['WeightUnit'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'Sex':
                for tag in df_biology[df_biology['IndividualSex'] != '']['IndividualSex'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'Maturity':
                for tag in df_biology[df_biology['IndividualMaturity'] != '']['IndividualMaturity'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)
            elif vocabulary_col == 'MaturityScale':
                for tag in df_biology[df_biology['MaturityScale'] != '']['MaturityScale'].unique():
                    code = etree.SubElement(child, 'Code')
                    code.set('ID', str(vocabulary_row[vocabulary_col])+'_'+tag)
                    code.set('CodeType', http_CodeType()+str(vocabulary_row[vocabulary_col])+'.xml')
                    code.text = str(tag)

    # Iterate over each record in the master DataFrame
    for _, cruise_row in df_cruise.iterrows():
        # Create a Cruise record element
        cruise_elem = etree.SubElement(root, 'Cruise')

        # For each column in the master row, create a child element
        for cruise_col in df_cruise.columns:
            # Optionally skip the key column or keep it if you want
            if cruise_col in ('Cruise', 'Record', 'cruise_id'):
                continue
            # Example: <ID>1</ID>, <Name>Alpha</Name>, etc.
            if str(cruise_row[cruise_col]) != "":
                child = etree.SubElement(cruise_elem, cruise_col)
                if cruise_col == 'Country':
                    child.set('IDREF', df_vocabulary['Country'].iloc[0]+"_"+str(cruise_row[cruise_col]))
                elif cruise_col == 'Organisation':
                    child.set('IDREF', df_vocabulary['Organisation'].iloc[0]+"_"+str(cruise_row[cruise_col]))
                elif cruise_col == 'Platform':
                    child.set('IDREF', df_vocabulary['Platform'].iloc[0]+"_"+str(cruise_row[cruise_col]))
                elif cruise_col == 'Survey':
                    code = etree.SubElement(child, 'Code')
                    code.set('IDREF', df_vocabulary['Survey'].iloc[0]+"_"+str(cruise_row[cruise_col]))
                else:
                    child.text = str(cruise_row[cruise_col])

        # Create a container for detail records
        # haul_elem = etree.SubElement(cruise_elem, 'Haul')

        # Filter the detail DataFrame to match the current master record
        haul_subset = df_haul[df_haul['LocalID'] == cruise_row['LocalID']]

        # Iterate over each detail record
        for _, haul_row in haul_subset.iterrows():
            # Create a detail record element
            haul_elem = etree.SubElement(cruise_elem, 'Haul')

            # For each column in the detail row (except the key, if desired), create a child element
            for haul_col in df_haul.columns:
                # Optionally skip the key column or keep it if you want
                if haul_col in ('Haul', 'Record', 'LocalID'):
                    continue

                # Example: <ID>1</ID>, <Name>Alpha</Name>, etc.
                if str(haul_row[haul_col]) != "":
                    child = etree.SubElement(haul_elem, haul_col)
                    if haul_col == 'gear':
                        child.set('IDREF', "Gear_"+str(haul_row[haul_col]))
                    elif haul_col == 'Validity':
                        child.set('IDREF', df_vocabulary['HaulValidity'].iloc[0]+"_"+str(haul_row[haul_col]))
                    elif haul_col == 'Stratum':
                        child.set('IDREF', df_vocabulary['Stratum'].iloc[0]+"_"+str(haul_row[haul_col]))
                    else:
                        child.text = str(haul_row[haul_col])

            # Catch
            catch_subset = df_catch[
                (df_catch['LocalID'] == haul_row['LocalID']) & (df_catch['gear'] == haul_row['gear']) & (
                            df_catch['Haulnumber'] == haul_row['Number'])]

            # Iterate over each detail record
            for _, catch_row in catch_subset.iterrows():
                # Create a detail record element
                catch_elem = etree.SubElement(haul_elem, 'Catch')

                # For each column in the detail row (except the key, if desired), create a child element
                for catch_col in df_catch.columns:
                    # Optionally skip the key column or keep it if you want
                    if catch_col in ('Catch', 'Record', 'LocalID', 'gear', 'Haulnumber'):
                        continue
                    if str(catch_row[catch_col]) != "":
                        child = etree.SubElement(catch_elem, catch_col)
                        if catch_col == 'DataType':
                            child.set('IDREF', df_vocabulary['DataType'].iloc[0]+"_"+str(catch_row[catch_col]))
                        elif catch_col == 'SpeciesCode':
                            child.set('IDREF', df_vocabulary['SpeciesCode'].iloc[0]+"_"+str(catch_row[catch_col]))
                        elif catch_col == 'SpeciesValidity':
                            child.set('IDREF', df_vocabulary['SpeciesValidity'].iloc[0]+"_"+str(catch_row[catch_col]))
                        elif catch_col == 'WeightUnit':
                            child.set('IDREF', df_vocabulary['WeightUnit'].iloc[0]+"_"+str(catch_row[catch_col]))
                        else:
                            child.text = str(catch_row[catch_col])

                # Biology
                biology_subset = df_biology[
                    (df_biology['LocalID'] == catch_row['LocalID']) & (df_biology['gear'] == catch_row['gear']) & (
                                df_biology['Haulnumber'] == catch_row['Haulnumber']) & (
                                df_biology['SpeciesCode'] == catch_row['SpeciesCode']) & (
                                df_biology['SpeciesCategory'] == catch_row['SpeciesCategory'])]

                # Iterate over each detail record
                for _, biology_row in biology_subset.iterrows():
                    # Create a detail record element
                    biology_elem = etree.SubElement(catch_elem, 'Biology')

                    # For each column in the detail row (except the key, if desired), create a child element
                    for biology_col in df_biology.columns:
                        # Optionally skip the key column or keep it if you want
                        if biology_col in ('Biology', 'Record', 'LocalID', 'gear', 'Haulnumber', 'SpeciesCode', 'SpeciesCategory'):
                            continue
                        if str(biology_row[biology_col]) != "":
                            child = etree.SubElement(biology_elem, biology_col)
                            if biology_col == 'StockCode':
                                child.set('IDREF', df_vocabulary['StockCode'].iloc[0]+"_"+str(biology_row[biology_col]))
                            elif biology_col == 'GeneticPopulationCode':
                                child.set('IDREF', df_vocabulary['GeneticPopulationCode'].iloc[0]+"_"+str(biology_row[biology_col]))
                            elif biology_col == 'LengthCode':
                                child.set('IDREF', df_vocabulary['LengthCode'].iloc[0]+"_"+str(biology_row[biology_col]))
                            elif biology_col == 'WeightUnit':
                                child.set('IDREF', df_vocabulary['WeightUnit'].iloc[0]+"_"+str(biology_row[biology_col]))
                            elif biology_col == 'IndividualSex':
                                child.set('IDREF', df_vocabulary['Sex'].iloc[0]+"_"+str(biology_row[biology_col]))
                            elif biology_col == 'IndividualMaturity':
                                child.set('IDREF', df_vocabulary['Maturity'].iloc[0]+"_"+str(biology_row[biology_col]))
                            elif biology_col == 'MaturityScale':
                                child.set('IDREF', df_vocabulary['MaturityScale'].iloc[0]+"_"+str(biology_row[biology_col]))
                            else:
                                child.text = str(biology_row[biology_col])

        # Return a pretty-printed XML string
        #    return test
        return etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')


def vocabulary():
    return [{
        "Survey": "AC_Survey",
        "Country": "ISO_3166",
        "Platform": "SHIPC",
        "Organisation": "EDMO",
        "gear": "gear",
        "HaulValidity": "AC_HaulValidity",
        "DataType": "AC_CatchDataType",
        "SpeciesCode": "SpecWoRMS",
        "StockCode": "ICES_StockCode",
        "GeneticPopulationCode": "GeneticPopulation",
        "SpeciesValidity": "AC_SpeciesValidity",
        "Sex": "AC_Sex",
        "LengthCode": "AC_LengthCode",
        "WeightUnit": "AC_WeightUnit",
        "Maturity": "AC_MaturityCode",
        "MaturityScale": "AC_MaturityScale",
        "Stratum": "AC_Stratum"
    }]


def cruise_csv_fields():
    return ['Cruise',
            'Header',
            'CruiseSurvey',
            'CruiseCountry',
            'CruisePlatform',
            'CruiseStartDate',
            'CruiseEndDate',
            'CruiseOrganisation',
            'CruiseLocalID'
    ]


def haul_csv_fields():
    return ['Haul',
            'Header',
            'CruiseLocalID',
            'HaulGear',
            'HaulNumber',
            'HaulStationName',
            'HaulStartTime',
            'HaulDuration',
            'HaulValidity',
            'HaulStartLatitude',
            'HaulStartLongitude',
            'HaulStopLatitude',
            'HaulStopLongitude',
            'HaulStatisticalRectangle',
            'HaulMinTrawlDepth',
            'HaulMaxTrawlDepth',
            'HaulBottomDepth',
            'HaulDistance',
            'HaulNetopening',
            'HaulCodendMesh',
            'HaulSweepLength',
            'HaulGearExceptions',
            'HaulDoorType',
            'HaulWarpLength',
            'HaulWarpDiameter',
            'HaulWarpDensity',
            'HaulDoorSurface',
            'HaulDoorWeight',
            'HaulDoorSpread',
            'HaulWingSpread',
            'HaulBuoyancy',
            'HaulKiteArea',
            'HaulGroundRopeWeight',
            'HaulRigging',
            'HaulTickler',
            'HaulHydrographicStationID',
            'HaulTowDirection',
            'HaulSpeedGround',
            'HaulSpeedWater',
            'HaulWindDirection',
            'HaulWindSpeed',
            'HaulSwellDirection',
            'HaulSwellHeight',
            'HaulLogDistance',
            'HaulStratum']


def catch_csv_fields():
    return ['Catch',
            'Header',
            'CruiseLocalID',
            'HaulGear',
            'HaulNumber',
            'CatchDataType',
            'CatchSpeciesCode',
            'CatchSpeciesValidity',
            'CatchSpeciesCategory',
            'CatchSpeciesCategoryNumber',
            'CatchWeightUnit',
            'CatchSpeciesCategoryWeight',
            'CatchSpeciesSex',
            'CatchSubsampledNumber',
            'CatchSubsamplingFactor',
            'CatchSubsampleWeight',
            'CatchLengthCode',
            'CatchLengthClass',
            'CatchLengthType',
            'CatchNumberAtLength',
            'CatchWeightAtLength']


def biology_csv_fields():
    return ['Biology',
            'Header',
            'CruiseLocalID',
            'HaulGear',
            'HaulNumber',
            'CatchSpeciesCode',
            'CatchSpeciesCategory',
            'BiologyStockCode',
            'BiologyFishID',
            'BiologyLengthCode',
            'BiologyLengthClass',
            'BiologyWeightUnit',
            'BiologyIndividualWeight',
            'BiologyIndividualSex',
            'BiologyIndividualMaturity',
            'BiologyMaturityScale',
            'BiologyIndividualAge',
            'BiologyAgePlusGroup',
            'BiologyAgeSource',
            'BiologyGeneticSamplingFlag',
            'BiologyStomachSamplingFlag',
            'BiologyParasiteSamplingFlag',
            'BiologyIndividualVertebraeCount']


def http_CodeType():
    return "https://acoustic.ices.dk/Services/Schema/XML/"
