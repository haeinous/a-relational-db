#!/usr/bin/python3

"""
Implement a Scan node that yields a single record each time its next method is called, as well as 
a Selection node initialized with a predicate function (one which returns true or false), which yields
the next record for which the predicate function returns true whenever its own next method is called.
"""

