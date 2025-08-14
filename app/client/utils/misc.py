#!/usr/local/bin/python3
# coding: utf-8

import functools


def haskey(d, path):
    try:
        functools.reduce(lambda x, y: x[y], path.split("."), d)
        return True
    except KeyError:
        return False


def chunked(iterable, size=200):
    """yield successive `size`-sized chunks from iterable."""
    for i in range(0, len(iterable), size):
        yield iterable[i: i + size]
