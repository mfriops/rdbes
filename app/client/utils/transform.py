#!/usr/local/bin/python3
# coding: utf-8

from app.client.utils.ora import nvl


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
