#!/usr/local/bin/python3
# coding: utf-8

import geopandas as gpd
from shapely.geometry import Point


def get_fao_area(lat, lon,
                 gpkg_path=r"D:\services\rdbes\shapefiles\fao.gpkg",
                 layer_name="fao") -> str:
    """
    Returns the FAO area code for a given latitude and longitude.

    Parameters:
        lat (float): Latitude in decimal degrees (e.g., 56.78)
        lon (float): Longitude in decimal degrees (e.g., 12.34)
        gpkg_path (str): Path to the GeoPackage file
        layer_name (str): Name of the layer inside the GPKG to query

    Returns:
        str: FAO area code if found, else None
    """
    # Load the FAO layer
    gdf = gpd.read_file(gpkg_path, layer=layer_name)

    # Create a GeoDataFrame from the point
    point = Point(lon, lat)
    point_gdf = gpd.GeoDataFrame([{'geometry': point}], crs="EPSG:4326")

    # Reproject the point to match the layer's CRS
    if gdf.crs != point_gdf.crs:
        point_gdf = point_gdf.to_crs(gdf.crs)

    # Perform spatial join to find which polygon contains the point
    joined = gpd.sjoin(point_gdf, gdf, how="left", predicate="within")

    # Extract and return the FAO code
    if not joined.empty and "fao" in joined.columns:
        return joined.iloc[0]["fao"]
    else:
        return None
