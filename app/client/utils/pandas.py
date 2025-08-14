#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd
import geopandas as gpd


def match_closest_station(merged_df, time_weight=0.5):
    """
    Compute proximity scores for each row and scale per fishing_trip_id
    so best match (lowest score) gets scaled_score = 1.0.

    Parameters:
        merged_df (DataFrame): Contains station and fishing trip data.
        time_weight (float): Weight for time in score calculation [0, 1].

    Returns:
        DataFrame with added columns:
            - spatial_distance (meters)
            - time_diff (seconds)
            - score
            - scaled_score (per fishing_trip_id, 1 = best match)
    """
    if not (0 <= time_weight <= 1):
        raise ValueError("time_weight must be between 0 and 1")

    df = merged_df.copy()

    # Parse timestamps
    df['station_date'] = pd.to_datetime(df['station_date'], errors='coerce')
    df['fishing_start'] = pd.to_datetime(df['fishing_start'], errors='coerce')
    df['fishing_end'] = pd.to_datetime(df['fishing_end'], errors='coerce')

    # Midpoints for location and time
    df['tow_time_mid'] = df['fishing_start'] + (df['fishing_end'] - df['fishing_start']) / 2
    df['tow_lat_mid'] = (df['tow_latitude'] + df['tow_latitude_end']) / 2
    df['tow_lon_mid'] = (df['tow_longitude'] + df['tow_longitude_end']) / 2

    # Identify valid rows
    required = [
        'latitude', 'longitude',
        'tow_lat_mid', 'tow_lon_mid',
        'station_date', 'tow_time_mid'
    ]
    df['is_valid'] = df[required].notnull().all(axis=1)

    valid = df[df['is_valid']].copy()
    valid['station_geom'] = gpd.points_from_xy(valid['longitude'], valid['latitude'], crs="EPSG:4326")
    valid['tow_geom'] = gpd.points_from_xy(valid['tow_lon_mid'], valid['tow_lat_mid'], crs="EPSG:4326")

    # Project to meters
    valid_gdf = gpd.GeoDataFrame(valid, geometry='station_geom', crs="EPSG:4326").to_crs(epsg=3857)
    valid_gdf['tow_geom'] = valid_gdf['tow_geom'].to_crs(epsg=3857)

    # Compute distances and time differences
    valid_gdf['spatial_distance'] = valid_gdf.geometry.distance(valid_gdf['tow_geom'])
    valid_gdf['time_diff'] = (valid_gdf['station_date'] - valid_gdf['tow_time_mid']).abs().dt.total_seconds()

    # Normalize globally
    s_max = valid_gdf['spatial_distance'].max()
    t_max = valid_gdf['time_diff'].max()
    valid_gdf['spatial_norm'] = valid_gdf['spatial_distance'] / s_max if s_max else 0
    valid_gdf['time_norm'] = valid_gdf['time_diff'] / t_max if t_max else 0

    # Compute combined score
    w = time_weight
    valid_gdf['score'] = (1 - w) * valid_gdf['spatial_norm'] + w * valid_gdf['time_norm']

    # Scale score per fishing_trip_id
    def scale_group(grp):
        if grp['score'].isnull().all():
            grp['scaled_score'] = pd.NA
        elif grp['score'].nunique() == 1:
            grp['scaled_score'] = 1.0
        else:
            min_s = grp['score'].min()
            max_s = grp['score'].max()
            grp['scaled_score'] = 1 - (grp['score'] - min_s) / (max_s - min_s)
        return grp

    if 'fishing_trip_id' in valid_gdf.columns:
        valid_gdf = valid_gdf.groupby('fishing_trip_id', group_keys=False).apply(scale_group)
    else:
        valid_gdf['scaled_score'] = 1 - (valid_gdf['score'] - valid_gdf['score'].min()) / (
            valid_gdf['score'].max() - valid_gdf['score'].min()
        )

    # Merge back into full DataFrame
    for col in ['spatial_distance', 'time_diff', 'score', 'scaled_score']:
        df[col] = pd.NA
        df.loc[valid_gdf.index, col] = valid_gdf[col]

    return df
