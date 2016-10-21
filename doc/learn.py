#!/usr/bin/env python

import json
from pprint import pprint


with open('stations.json') as file_stations:
    stations = json.load( file_stations )

with open('routes.json') as file_routes:
    routes = json.load( file_routes )


def summarize( l_circuit ):
    '''return a list summarized into a list of ranges'''
    l_range = []
    l_elem = []
    prev = -1
    for c in l_circuit:
        current = int(c)
        if current != prev + 1:
            if prev > 0:
                l_elem.append( prev )
                l_range.append( l_elem )
                l_elem = []
            l_elem.append( current )
        prev = current
    return l_range


# read in stations and create dictionary with key name and value code
d_stations = {}

for station in stations['Stations']:
    d_stations[ station['Code'] ] = station['Name']


#
# print a summarized list of lines along with routes
#
for route in sorted( routes['StandardRoutes'], key=lambda r: r['LineCode'] ):
    print 'line:', route['LineCode'], ' track:', route['TrackNum']
    for r in summarize( [r['CircuitId'] for r in route['TrackCircuits']] ):
        print '   ', r[0], '-', r[1]
    print



