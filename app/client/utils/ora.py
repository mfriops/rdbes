#!/usr/local/bin/python3
# coding: utf-8

"""
Mimics Oracle's NULL value.
"""
def null():
    return None


"""
Mimics Oracle's NVL function.
"""
def nvl(value, null_value = 0):
    return null_value if value is None or value is '' else value

"""
Mimics Oracle's DECODE function.
"""
def decode(value, chk_value, if_value, else_value):
    return if_value if value == chk_value else else_value


"""
Mimics Oracle's LEAST function.

Returns the smallest value from the provided arguments.
If any argument is None (to represent SQL NULL), returns None.
"""
def least(*args):
    # If any argument is None, mimic Oracle behavior by returning None.
    if any(arg is None for arg in args):
        return None

    return min(args)


"""
Mimics Oracle's GREATEST function.

Returns the largest value from the provided arguments.
If any argument is None (to represent SQL NULL), returns None.
"""
def greatest(*args):
    # If any argument is None, mimic Oracle behavior by returning None.
    if any(arg is None for arg in args):
        return None

    return max(args)


"""
Mimics Oracle's COALESCE function.

Returns the first non-None value from the provided arguments.
If all arguments are None, returns None.
"""
def coalesce(*args):
    for arg in args:
        if arg is not None:
            return arg
    return None
