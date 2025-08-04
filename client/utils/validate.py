#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd
from client.utils.misc import haskey
from client.utils.geo import haversine
from client.utils.helper import parse_time


def validate_acoustic(acousticDict: dict) -> dict:

    errors = False
    errorsHtml = {}

    # Instrument
    instrumentDict = []
    if 'Instrument' in acousticDict['Acoustic']:
        if type(acousticDict['Acoustic']['Instrument']) == dict:
            instrumentDict.append(acousticDict['Acoustic']['Instrument'])
        else:
            for inst in acousticDict['Acoustic']['Instrument']:
                instrumentDict.append(inst)

    if instrumentDict != []:
        df_instrument = pd.DataFrame(instrumentDict)
        instrumentSchema = instrument_fields()
        instrumentReport = validate_dataframe(df_instrument, instrumentSchema)
        if dict_error(instrumentReport):
            errors = True
            errorsHtml['instrument_errors'] = generate_html_from_dict(instrumentReport, 'Instrument Errors')
        # print({'Instrument': instrumentReport})

    # Calibration
    calibrationDict = []
    if 'Calibration' in acousticDict['Acoustic']:
        if type(acousticDict['Acoustic']['Calibration']) == dict:
            calibrationDict.append(acousticDict['Acoustic']['Calibration'])
        else:
            for cal in acousticDict['Acoustic']['Calibration']:
                calibrationDict.append(cal)

    if calibrationDict != []:
        if type(calibrationDict) != list:
            calibrationDict = [calibrationDict]
        df_calibration = pd.DataFrame(calibrationDict)
        calibrationSchema = calibration_fields()
        calibrationReport = validate_dataframe(df_calibration, calibrationSchema)
        if dict_error(calibrationReport):
            errors = True
            errorsHtml['calibration_errors'] = generate_html_from_dict(calibrationReport, 'Calibration Errors')
        # print({'Calibration': calibrationReport})

    # Data Acquisition
    dataacquisitionDict = []
    if 'DataAcquisition' in acousticDict['Acoustic']:
        if type(acousticDict['Acoustic']['DataAcquisition']) == dict:
            dataacquisitionDict.append(acousticDict['Acoustic']['DataAcquisition'])
        else:
            for acquli in acousticDict['Acoustic']['DataAcquisition']:
                dataacquisitionDict.append(acquli)

    if dataacquisitionDict != []:
        df_dataacquisition = pd.DataFrame(dataacquisitionDict)
        dataacquisitionSchema = data_acquisition_fields()
        dataacquisitionReport = validate_dataframe(df_dataacquisition, dataacquisitionSchema)
        if dict_error(dataacquisitionReport):
            errors = True
            errorsHtml['dataacquisition_errors'] = generate_html_from_dict(dataacquisitionReport, 'DataAcquisition Errors')
        # print({'DataAcquisition': dataacquisitionReport})

    # Data Processing
    dataprocessingDict = []
    if 'DataProcessing' in acousticDict['Acoustic']:
        if type(acousticDict['Acoustic']['DataProcessing']) == dict:
            dataprocessingDict.append(acousticDict['Acoustic']['DataProcessing'])
        else:
            for process in acousticDict['Acoustic']['DataProcessing']:
                dataprocessingDict.append(process)

    if dataprocessingDict != []:
        df_dataprocessing = pd.DataFrame(dataprocessingDict)
        dataprocessingSchema = data_processing_fields()
        dataprocessingReport = validate_dataframe(df_dataprocessing, dataprocessingSchema)
        if dict_error(dataprocessingReport):
            errors = True
            errorsHtml['dataprocessing_errors'] = generate_html_from_dict(dataprocessingReport, 'DataProcessing Errors')
        # print({'DataProcessing': dataprocessingReport})

    # Echotype
    echotypeDict = []
    if 'EchoType' in acousticDict['Acoustic']:
        if type(acousticDict['Acoustic']['EchoType']) == dict:
            echotypeDict.append(acousticDict['Acoustic']['EchoType'])
        else:
            for echo in acousticDict['Acoustic']['Echotype']:
                echotypeDict.append(echo)

    if echotypeDict != []:
        df_echotype = pd.DataFrame(echotypeDict)
        echotypeSchema = echo_type_fields()
        echotypeReport = validate_dataframe(df_echotype, echotypeSchema)
        if dict_error(echotypeReport):
            errors = True
            errorsHtml['echotype_errors'] = generate_html_from_dict(echotypeReport, 'EchoType Errors')
        # print({'EchoType': echotypeReport})

    # Cruise
    cruiseDict = {}
    if 'Cruise' in acousticDict['Acoustic']:
        if type(acousticDict['Acoustic']['Cruise']) == dict:
            for key, value in acousticDict['Acoustic']['Cruise'].items():
                if key in ('Country', 'Organisation', 'Platform', 'StartDate', 'EndDate', 'Survey', 'LocalID'):
                    cruiseDict[key] = value
                if key == 'LocalID':
                    localID = value

    if cruiseDict != []:
        df_cruise = pd.DataFrame([cruiseDict])
        cruiseSchema = cruise_fields()
        cruiseReport = validate_dataframe(df_cruise, cruiseSchema)
        if dict_error(cruiseReport):
            errors = True
            errorsHtml['cruise_errors'] = generate_html_from_dict(cruiseReport, 'Cruise Errors')
        # print({'Cruise': cruiseReport})

    # Data
    dataDict = []
    if 'Log' in acousticDict['Acoustic']['Cruise']:
        for log in acousticDict['Acoustic']['Cruise']['Log']:
            dataDict.append(log)

    if dataDict != []:
        df_data = pd.DataFrame(dataDict)
        dataSchema = data_fields()
        dataReport = validate_dataframe(df_data, dataSchema)
        if dict_error(dataReport):
            errors = True
            errorsHtml['data_errors'] = generate_html_from_dict(dataReport, 'Data Errors')
        # print({'Data': dataReport})

    if errors:
        return {'return': -1}, errorsHtml
    else:
        return {'return': 1}, errorsHtml


def log_sample(sample, localID):
    logSample = {}
    logSample['ChannelDepthUpper'] = sample['ChannelDepthUpper']
    logSample['ChannelDepthLower'] = sample['ChannelDepthLower']
    logSample['PingAxisInterval'] = sample['PingAxisInterval']
    logSample['PingAxisIntervalType'] = sample['PingAxisIntervalType']
    logSample['PingAxisIntervalUnit'] = sample['PingAxisIntervalUnit']
    logSample['SvThreshold'] = sample['SvThreshold']
    logSample['Instrument'] = sample['Instrument']
    logSample['Calibration'] = sample['Calibration']
    logSample['DataAcquisition'] = sample['DataAcquisition']
    logSample['DataProcessing'] = sample['DataProcessing']
    logSample['EchoType'] = sample['EchoType']
    logSample['PingAxisIntervalOrigin'] = sample['PingAxisIntervalOrigin']
    logSample['CruiseLocalID'] = localID
    return logSample


def log_sample_data(data):
    logSampleData = {}
    logSampleData['SaCategory'] = data['SaCategory']
    logSampleData['Type'] = data['Type']
    logSampleData['Unit'] = data['Unit']
    logSampleData['Value'] = data['Value']
    return logSampleData


def validate_haul(df: pd.DataFrame):
    errors = []
    for idx, row in df.iterrows():
        try:
            deviation = 0.15
            haul = int(row["Haulnumber"]/10)                # haulnumber
            reported_duration = float(row["Duration"])      # min
            reported_distance = float(row["Distance"])      # sea miles
            reported_speed = float(row["SpeedGround"])      # knots

            distance_m = haversine(float(row["StartLatitude"]), float(row["StartLongitude"]), float(row["StopLatitude"]), float(row["StopLongitude"]), 6378137.0)
            distance_nm = haversine(float(row["StartLatitude"]), float(row["StartLongitude"]), float(row["StopLatitude"]), float(row["StopLongitude"]), 3440.065)
            speed_knots = distance_nm / (reported_duration / 60.0) if reported_duration > 0 else 0

            if abs(reported_distance - distance_m) / reported_distance > deviation:
                errors.append(f"Haul:{haul} - Distance mismatch: Computed={distance_m:.2f}, Reported={reported_distance:.2f}<br>")
            if abs(reported_speed - speed_knots) / reported_speed > deviation:
                errors.append(f"Haul:{haul} - Speed mismatch: Computed={speed_knots:.2f}, Reported={reported_speed:.2f}<br>")
        except Exception:
            continue

    return {"Haul consistency": errors} if errors else {}


def validate_biology(df: pd.DataFrame):
    lw_params = {
        "126417": (0.0033, 3.259, 0.30),     # herring (0.007, 3.00)
        "126735": (0.0005, 3.8264, 0.35),    # capelin (0.006, 2.85)
        "126439": (0.004, 3.1535, 0.30),     # blue whiting (0.01, 2.95)
        "127023": (0.004, 3.1535, 0.35)      # mackerel (0.005, 3.15)
    }

    errors = []
    for idx, row in df.iterrows():
        try:
            measure_id = row.get("FishID", "")
            species = row.get("SpeciesCode", "")
            reported_length = float(row["LengthClass"])/10
            reported_weight = float(row["IndividualWeight"])
            a, b, deviation = lw_params.get(species, (None, None))

            if a is not None and b is not None:
                expected_weight = a * reported_length ** b
                if abs(reported_weight - expected_weight) / max(reported_weight, expected_weight) > deviation:
                    errors.append(f"Measure_id: {measure_id} - Weight mismatch: Computed={expected_weight:.2f}, Reported={reported_weight:.2f}<br>")

        except Exception:
            continue

    return {"Biology Consistency": errors}


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
    df = df.applymap(lambda x: None if pd.isna(x) or x == "" else x)

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

    # Haul, computed validations
    if all(col in df.columns for col in ["StartTime", "Duration", "StartLatitude", "StartLongitude", "StopLatitude", "StopLongitude", "Distance", "SpeedGround"]):
        validation_report["computed_errors"].update(validate_haul(df))

    # Biology, computed validations
    if all(col in df.columns for col in ["LengthCode", "IndividualWeight", "SpeciesCode"]):
        validation_report["computed_errors"].update(validate_biology(df))
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


def combine_errors(errors: dict) -> str:
    errors_str = """<!DOCTYPE html>
<html lang="en">"""
    if haskey(errors, 'design_errors'):
        errors_str += errors['design_errors']
    if haskey(errors, 'sampling_details_errors'):
        errors_str += errors['sampling_details_errors']

    if haskey(errors, 'vessel_details_errors'):
        errors_str += errors['vessel_details_errors']
    if haskey(errors, 'fishing_trip_errors'):
        errors_str += errors['fishing_trip_errors']
    if haskey(errors, 'fishing_operation_errors'):
        errors_str += errors['fishing_operation_errors']

    if haskey(errors, 'individual_species_errors'):
        errors_str += errors['individual_species_errors']
    if haskey(errors, 'species_list_errors'):
        errors_str += errors['species_list_errors']
    if haskey(errors, 'species_selection_errors'):
        errors_str += errors['species_selection_errors']
    if haskey(errors, 'sample_errors'):
        errors_str += errors['sample_errors']

    if haskey(errors, 'frequency_measure_errors'):
        errors_str += errors['frequency_measure_errors']
    if haskey(errors, 'biological_variable_errors'):
        errors_str += errors['biological_variable_errors']

    if haskey(errors, 'commercial_landing_errors'):
        errors_str += errors['commercial_landing_errors']
    if haskey(errors, 'commercial_effort_errors'):
        errors_str += errors['commercial_effort_errors']

    return errors_str


def combine_acoustic_errors(errors: dict) -> str:
    errors_str = """<!DOCTYPE html>
<html lang="en">"""
    if haskey(errors, 'instrument_errors'):
        errors_str += errors['instrument_errors']
    if haskey(errors, 'calibration_errors'):
        errors_str += errors['calibration_errors']
    if haskey(errors, 'dataacquisition_errors'):
        errors_str += errors['dataacquisition_errors']
    if haskey(errors, 'dataprocessing_errors'):
        errors_str += errors['dataprocessing_errors']
    if haskey(errors, 'echotype_errors'):
        errors_str += errors['echotype_errors']
    if haskey(errors, 'data_errors'):
        errors_str += errors['data_errors']

    return errors_str
