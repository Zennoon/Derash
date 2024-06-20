#!/usr/bin/python3
"""
Contains:
    Functions
    =========
    calc_distance - Calculates the distance between to latitude,longitude coordinates
"""
from math import acos, cos, pi, sin


def calc_distance(coord1, coord2):
    """
    Calculates the distance between two coordinates (latitude and longitude tuples)
    """
    lat1, lon1 = coord1[0] * (pi / 180), coord1[1] * (pi / 180)
    lat2, lon2 = coord2[0] * (pi / 180), coord2[1] * (pi / 180)
    radius = 6371

    dist = acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1))*radius
    return (dist)

