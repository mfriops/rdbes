#!/usr/local/bin/python3
# coding: utf-8

from client.business.misc import read_country, read_organisation, read_platform, read_gear, read_stratum, read_datatype, read_speciesvalidity


def country():
    return read_country()


def organisation():
    return read_organisation()


def platform(registration_no):
    return read_platform(registration_no)


def gear():
    return read_gear()


def stratum():
    return read_stratum()


def datatype():
    return read_datatype()


def speciesvalidity():
    return read_speciesvalidity()
