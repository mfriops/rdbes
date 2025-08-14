#!/usr/local/bin/python3
# coding: utf-8

# server/services/rdbes/fao_lookup.py  (example path)
import os
import math
import geopandas as gpd
from functools import lru_cache
from shapely.geometry import Point

# Env-driven config (works in Docker and locally)
FAO_GPKG_PATH  = os.getenv("FAO_GPKG_PATH", "/opt/geo/fao.gpkg")
FAO_GPKG_LAYER = os.getenv("FAO_GPKG_LAYER", "fao")
FAO_CODE_FIELD = os.getenv("FAO_GPKG_CODE_FIELD", "fao")  # change if your column name differs

@lru_cache(maxsize=1)
def _load_fao(path: str, layer: str) -> gpd.GeoDataFrame:
    # Use pyogrio for simpler GDAL deps; fall back to default if unavailable
    kwargs = {"engine": "pyogrio"} if os.getenv("GPKG_ENGINE", "pyogrio") == "pyogrio" else {}
    gdf = gpd.read_file(path, layer=layer, **kwargs)
    if gdf.crs is None:
        raise RuntimeError(f"GeoPackage layer {layer} has no CRS defined")
    # Touch sindex to build spatial index once
    _ = gdf.sindex
    return gdf

def get_fao_area(
    lat: float,
    lon: float,
    gpkg_path: str | None = None,
    layer_name: str | None = None,
    code_field: str | None = None
) -> str | None:
    """
    Return the FAO area code for a given (lat, lon).  WGS84 expected.
    """
    path  = gpkg_path  or FAO_GPKG_PATH
    layer = layer_name or FAO_GPKG_LAYER
    code  = code_field or FAO_CODE_FIELD

    # Load the FAO layer
    gdf = _load_fao(path, layer)

    # Create a GeoDataFrame from the point
    pt_gdf = gpd.GeoDataFrame([{"geometry": Point(lon, lat)}], crs="EPSG:4326")
    if gdf.crs != pt_gdf.crs:
        pt_gdf = pt_gdf.to_crs(gdf.crs)

    # Only keep geometry + code to reduce join payload
    cols = [c for c in gdf.columns if c == code] + [gdf.geometry.name]
    joined = gpd.sjoin(pt_gdf, gdf[cols], how="left", predicate="within")

    # Extract and return the FAO code
    if joined.empty or code not in joined.columns:
        return None

    val = joined.iloc[0][code]
    if isinstance(val, float) and math.isnan(val):
        return None
    return str(val)
