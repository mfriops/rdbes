#!/usr/local/bin/python3
# coding: utf-8

from app.client.api.misc import get_country, get_organisation, get_platform, \
                            get_gear, get_stratum, get_datatype, get_speciesvalidity

def read_country():
    return get_country()

def read_organisation():
    return get_organisation()

def read_platform(registration_no):
    return get_platform(registration_no)

def read_gear():
    return get_gear()

def read_stratum():
    return get_stratum()

def read_datatype():
    return get_datatype()

def read_speciesvalidity():
    return get_speciesvalidity()
