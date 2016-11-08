#!/usr/bin/env python2.7

'''
try to create a dot file for the redline

'''

import pydot
from wmata import wmata

d_line2color = { 'BL': '#0795d3',
                 'RD': '#be1337',
                 'OR': '#da8707',
                 'YL': '#f5d415',
                 'GR': '#00b050',
                 'SV': '#a2a4a1' }



def draw():
    g = pydot.Dot( graph_type='graph')
    g.set( 'concentrate', 'true' )
    g.set_node_defaults( shape='record' )

    # divide the cids into switches or track units
    for cid in w.allCids():
        color = 'black'
        lines = w.getLines(cid)
        s_lines = ''
        if lines:
            color = d_line2color.get( lines[0][0], 'black' )
            s_lines = ','.join( map( lambda x: x[0], lines ) )

        station = w.getStation(cid)
        if station:
            label = '{<f0> %d | <f1> %d } | {<f3> %s | <f4> %s}' % \
                    (w.getTrack(cid), cid, s_lines, station)
        else:
            label = '{<f0> %d | <f1> %d } | <f3> %s ' % \
                    (w.getTrack(cid), cid, s_lines)
        g.add_node( pydot.Node( cid, color=color, label=label ) )


    # create edges
    for cid in w.allCids():
        if w.getNext(cid):
            g.add_edge( pydot.Edge( cid, w.getNext(cid) ) )

        if w.getPrevious(cid):
            g.add_edge( pydot.Edge( w.getPrevious(cid), cid ) )

        
#        for n in w.getNeighbors(cid):
#            g.add_edge( pydot.Edge( cid, n ) )


    g.write_svg( 'test.svg' )

w = wmata()
draw()



