#!/usr/local/bin/python3
# coding: utf-8

import geopandas as gpd
from math import floor, copysign, trunc, radians, sin, cos, acos, sqrt, atan2, pi
from shapely.geometry import Point


# https://gis.ices.dk/sf/index.html?widget=StatRec

# In: Decimal, latitude / longitude
# Out: ICES rectangle (55C5)
def d2ir(p_lat: float, p_lon: float, useI: bool = False) -> str:
    if p_lat < 36 or p_lat >= 85.5 or p_lon <= -44 or p_lon > 68.5:
        return None  # Positions outside of ICES statistical area

    lat = floor(p_lat * 2) - 71
    ir = f"{lat:02d}"

    # Put a space at the beginning of the strings because in python,
    # strings start at 0 but in oracle pl/sql at 1 and the function is translated from pl/sql
    if useI:
        letters_used = " ABCDEFGHIJKL"  # First 12 letters
    else:
        letters_used = " ABCDEFGHJKLM"  # First 8 letters + last 4 skipping 'I'

    s_lon1 = letters_used[int((p_lon + 60) // 10)]

    if s_lon1 == 'A':
        s_lon2 = int(p_lon - 4 * (p_lon // 4))
    else:
        s_lon2 = int(p_lon - 10 * (p_lon // 10))

    return f"{ir}{s_lon1}{s_lon2}"


#  In: Decimal, latitude / longitude
#  Out: ggmi99, latitude / longitude
def geoinverse(F: float) -> float:
    s = copysign(1, F)
    F_abs = abs(F)
    A = int(F_abs)
    x = 6000 * F_abs + 4000 * A
    return s * x


#  In: ggmi99, latitude / longitude
#  Out: Decimal, latitude / longitude
def geoconvert(y: float) -> float:
    if y is None:
        return None
    i = copysign(1, y)
    x = abs(y)
    x1 = x % 10000
    tmp = (x / 100) - trunc(x / 10000) * 100
    tmp = (i * (x + (200 / 3) * tmp)) / 10000
    return tmp


def haversine(lat, lon, lat2, lon2, R):
    # Earth radii in different units
    # R = 6378137.0         # Meters
    # R = 6371.0          # Kilometers
    # R = 3958.8          # Miles
    # R = 3440.065        # Nautical miles (sea miles)

    # Convert coordinates from degrees to radians
    phi1, phi2 = map(radians, [lat, lat2])

    # Differences
    delta_phi = radians(lat2 - lat)
    delta_lambda = radians(lon2 - lon)

    # Haversine formula
    a = sin(delta_phi / 2.0) ** 2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2.0) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Compute distances (in different units)
    distance = R * c

    return distance


def ices_statistical_rectangle(lat: float, lon: float):
    """
    Compute the ICES Statistical Rectangle for a given latitude and longitude.

    Parameters:
    - lat: Latitude in decimal degrees
    - lon: Longitude in decimal degrees

    Returns:
    - ICES rectangle as a string (e.g., '37F3') or None if out of bounds
    """

    if not (lat == None or lon == None):
        return None  # Data/input not sufficient

    if not (36.0 <= lat <= 85.5 and -44.0 <= lon <= 68.0):
        return None  # Out of ICES area

    # Latitude bands start at 36°N in 0.5° steps
    lat_band = int((lat - 36.0) * 2)

    # Longitude bands start at 44°W (represented as -44) in 1° steps
    lon_band = int(lon + 44.0)

    # Latitude part is always two digits
    lat_part = f"{lat_band:02d}"

    # Longitude letters start from A (0) to Z (25), then a (26), b (27), ...
    if 0 <= lon_band < 26:
        lon_letter = chr(ord('A') + lon_band)
    else:
        lon_letter = chr(ord('a') + lon_band - 26)

    # Determine the quadrant (1, 2, 3, 4)
    lat_mod = (lat - 36.0) * 2 - lat_band
    lon_mod = lon + 44.0 - lon_band

    if lat_mod >= 0.5:
        if lon_mod >= 0.5:
            quadrant = '4'
        else:
            quadrant = '3'
    else:
        if lon_mod >= 0.5:
            quadrant = '2'
        else:
            quadrant = '1'

    return f"{lat_part}{lon_letter}{quadrant}"



def get_gsa(lat, lon):
# TODO þarf að finna GSA_shapefile.shp hjá ICES
    # Load the GSA shapefile
    # gsa_map = gpd.read_file("GSA_shapefile.shp")  # download from FAO site
    # gsa_map = gpd.read_file(
    #     "D:\\clients\\rdbes\\shapefiles\\GSA_Federal_Locations\\GSA_shapefile.shp")  # download from FAO site
    gsa_map = gpd.read_file("D:/clients/rdbes/shapefiles/ICES_areas/ICES_Areas_20160601_cut_dense_3857.shp")  # download from FAO site

    point = Point(lon, lat)  # Note: lon first in Point()
    for _, row in gsa_map.iterrows():
        if row['geometry'].contains(point):
            return row['GSA_Name']  # or 'GSA_ID'
    return None


# for _, row in gsa_map.iterrows():
#     if row['geometry'].contains(point):
#         print(row['OBJECTID'])  # or 'GSA_ID'
#
# for _, row in gsa_map.iterrows():
#     print(row['OBJECTID'])  # or 'GSA_ID'


################################################################
## Functions below needs to bee tested and verified
################################################################


#  In: latitude / longitude
#     teg: T tíundakerfi
#          G formi ggmi99 gg:gráður; mi:mínútur 99:hundraðshl. úr mín.
#  Out:  reitur
# def d2r(p_lat: float, p_lon: float, teg: str = 'T') -> int:
#     lat = p_lat
#     lon = abs(p_lon)
#
#     if teg != 'T':
#         lat = geoconvert(lat)
#         lon = geoconvert(lon)
#
#     reitur = math.floor(lat) * 100 + math.floor(lon) - 6000
#
#     if (lat - math.floor(lat)) > 0.5:
#         reitur += 50
#
#     return reitur


#  Inntak: latitude / longitude
#     teg: T tíundakerfi
#          G formi ggmi99 gg:gráður; mi:mínútur 99:hundraðshl. úr mín.
#  Out:  reitur+smáreitur
# def d2rs(p_lon: float, p_lat: float):
#     l1 = math.floor(p_lat / 100)
#     l2 = p_lat - (100 * l1)
#     l2 = round(l2 / 60, 2)
#
#     b1 = math.floor(p_lon / 100)
#     b2 = p_lon - (100 * b1)
#     b2 = round(b2 / 60, 2)
#
#     r1 = ((l1 - 60) * 100) + b1
#
#     if l2 >= 0.5:
#         r1 += 50
#         l2 -= 0.5
#
#     if l2 >= 0.25 and b2 >= 0.5:
#         smrt = 1
#     elif l2 >= 0.25 and b2 < 0.5:
#         smrt = 2
#     elif l2 < 0.25 and b2 >= 0.5:
#         smrt = 3
#     else:
#         smrt = 4
#
#     reit = r1 if r1 >= 0 else None
#     smrt = smrt if r1 >= 0 else None
#
#     return reit, smrt


#  Inntak: latitude / longitude
#     teg: T tíundakerfi
#          G formi ggmi99 gg:gráður; mi:mínútur 99:hundraðshl. úr mín.
#  Out:  reitur+smáreitur
# def d2sr(p_lat: float, p_lon: float, teg: str = 'T') -> int:
#     lat = p_lat
#     lon = abs(p_lon)
#
#     if teg != 'T':
#         lat = geoconvert(lat)
#         lon = geoconvert(lon)
#
#     reitur = d2r(lat, lon)
#     smareitur = postosmareit(lat, lon)
#
#     if reitur < 0:
#         reitar = reitur * 10 - smareitur
#     else:
#         reitar = reitur * 10 + smareitur
#
#     return reitar


#  Inntak: ICES reitur (55C5)
#  Out:  latitude (63.25) ef teg = 'LAT' annars longitude (-24.5)
# def ir2d(ir: str, teg: str = 'LAT', useI: bool = False) -> float:
#     lat = int(ir[:2])
#     lat = (lat + 71) / 2 + 0.25
#
#     s_lon1 = ir[2].upper()
#     lon1 = string.ascii_uppercase.index(s_lon1) + 1
#
#     if not useI and lon1 > 8:
#         lon1 -= 1
#
#     lon1 -= 2
#     lon2 = int(ir[3])
#
#     if lon1 < 0:
#         lon = -44 + lon2 + 0.5
#     else:
#         lon = -40 + 10 * lon1 + lon2 + 0.5
#
#     return lon if teg != 'LAT' else lat


#  Inntak: latitude / longitude
#     teg: T tíundakerfi
#          G formi ggmi99 gg:gráður; mi:mínútur 99:hundraðshl. úr mín.
# def postosmareit(p_lat1: float, p_lon1: float, teg: str = 'T') -> int:
#     lat1 = p_lat1
#     lon1 = abs(p_lon1)
#
#     if teg == 'T':
#         lat1 = geoinverse(p_lat1)
#         lon1 = geoinverse(abs(p_lon1))
#
#     lat = lat1 / 10000
#     lon = lon1 / 10000
#
#     lat = math.floor(lat) + (lat - math.floor(lat)) / 0.6
#     lon = math.floor(lon) + (lon - math.floor(lon)) / 0.6
#
#     reitur = math.floor(lat) * 100 + math.floor(lon) - 6000
#
#     if (lat - math.floor(lat)) > 0.5:
#         reitur += 50
#
#     lat -= math.floor(lat)
#     lon -= math.floor(lon)
#
#     if lat > 0.5:
#         lat -= 0.5
#
#     if lat >= 0.25 and lon >= 0.5:
#         smareitur = 1
#     elif lat >= 0.25 and lon < 0.5:
#         smareitur = 2
#     elif lat < 0.25 and lon >= 0.5:
#         smareitur = 3
#     else:
#         smareitur = 4
#
#     return smareitur


#  Inntak: r = reitur
#          teg =  LAT fyrir latitute eða LON fyrir longitude.
#  Out:  latitute eða longitude eftir hvað er valið í degr.
# def r2d(r: float, teg: str = 'LAT') -> float:
#     lat = math.floor(r / 100)
#     lon = (r - lat * 100) % 50
#     halfb = (r - 100 * lat - lon) / 100
#     lon = -(lon + 0.5)
#     lat = lat + 60 + halfb + 0.25
#
#     return lon if teg != 'LAT' else lat


#  Inntak: sr = smáreitur
#          teg =  LAT fyrir latitute eða LON fyrir longitude
#  Out:  latitute eða longitude eftir hvað er valið í teg.
# def sr2d(sr: float, teg: str = 'LAT') -> float:
#     r = math.floor(sr / 10)
#     s = round(sr - r * 10, 0) + 1
#
#     lat = math.floor(r / 100)
#     lon = (r - lat * 100) % 50
#     halfb = (r - 100 * lat - lon) / 100
#     lon = -(lon + 0.5)
#     lat = lat + 60 + halfb + 0.25
#
#     if s == 1:
#         lat += 0
#         lon += 0
#     elif s == 2:
#         lat += 0.125
#         lon -= 0.25
#     elif s == 3:
#         lat += 0.125
#         lon += 0.25
#     elif s == 4:
#         lat -= 0.125
#         lon -= 0.25
#
#     return lon if teg != 'LAT' else lat


def arcdist(lat: float, lon: float, lat2: float, lon2: float, scale: str = 'nmi') -> float:
    if scale == 'nmi':
        miles = 1.852
    else:
        miles = 1

    rad = 6367
    mult1 = rad / miles
    mult2 = pi / 180

    tmp = (
            sin(mult2 * lat) * sin(mult2 * lat2) +
            cos(mult2 * lat) * cos(mult2 * lat2) * cos(mult2 * lon - mult2 * lon2)
    )

    dist = mult1 * acos(max(min(tmp, 1), -1))
    return dist


def towlength(lat: float, lon: float, lat2: float, lon2: float) -> float:

    # Convert degrees to radians
    x = lat * (pi / 180)

    # Compute towing distance in nautical miles
    towdistance = round(60 * sqrt((lat2 - lat) ** 2 + (cos(x) ** 2) * (lon2 - lon) ** 2), 2)

    return towdistance
