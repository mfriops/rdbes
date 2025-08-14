#!/usr/local/bin/python3
# coding: utf-8

def get_country():
    return 'IS'

def get_organisation():
    return '4766'

def get_platform(registration_no):
    if registration_no == 2350:
        return '46AS'
    elif registration_no == 1131:
        return '46BS'

def get_gear():
    return 'PEL'

def get_stratum():
    return 'SURF'

def get_datatype():
    return 'R'

def get_speciesvalidity():
    return '1'
