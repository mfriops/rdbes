#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd
from datetime import datetime


def parse_time(t):
    try:
        return pd.to_datetime(t)
    except Exception:
        return None


# Parse two date-time strings into datetime objects.
def datetime_parse(dt_str):
    return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")


def datetime_diff(dt_from_str: str, dt_to_str: str) -> float:
    dt_from = datetime_parse(dt_from_str)
    dt_to = datetime_parse(dt_to_str)
    delta = dt_to - dt_from
    return delta.total_seconds() / (24 * 3600)


def to_id(p_dict, p_key):
    if p_key in p_dict:
        return p_dict[p_key]
    return p_dict['ID']


def to_int(value):
    return round(value) if value != '' else None


def to_float(value, decimal = 2):
    return round(value, decimal) if value != '' else None


def to_text(p_str):
    return "" if p_str == None else str(int(p_str))


def key_to_id(p_str):
    return p_str[p_str.rfind('@')+1:len(p_str)]


def val_to_id(p_str):
    return p_str[p_str.rfind('_')+1:len(p_str)]


def vokabulary_AC(p_str):
    return p_str[p_str.rfind('_')+1:len(p_str)] if p_str.find('AC_') > -1 else p_str


def vokabulary(p_str):
    return p_str[p_str.rfind('_')+1:len(p_str)] if p_str.find('_') > -1 else p_str


def merge_dict(dict1, dict2):
    return(dict2.update(dict1))


def add_dict(p_dict):
    q_dict = {}
    for key, value in p_dict.items():
        val = "" if value == None else value
        if key == '@ID':
            key = key_to_id(key)
            val = val_to_id(value)
        if type(value) is dict:
            if '@IDREF' in value:
                val = vokabulary_AC(value['@IDREF'])
        q_dict[key] = vokabulary_AC(val)
    q_dict['Comments'] = q_dict['ID']
    return q_dict


def add_list(p_list):
    q_list = []
    for dict in p_list:
        q_list.append(add_dict(dict))
    return q_list
