#!/usr/bin/env python2.7

'''
try to create a dot file for the redline

'''

import pydot
from wmata import wmata

def pswitch(cid):
    '''return true if cid is a switch'''
    return len(w.neighbors(cid))>2

def addSegment( g, l_cid ):

    d_line2color = { 'BL': '#0795d3',
                     'RD': '#be1337',
                     'OR': '#da8707',
                     'YL': '#f5d415',
                     'YLRP': '#f5d415',
                     'GR': '#00b050',
                     'SV': '#a2a4a1' }

    for cid in l_cid:
        color = 'black'

        d_line2seq = dict()
        lines = w.getLines(cid)
        for line,seq in lines:
            d_line2seq[line] = seq


        if lines:
            s_line = '<TR>'
            for line in sorted(d_line2color.keys()):
                if line in d_line2seq:
                    s_line+= ('<TD BGCOLOR="%s">%s</TD>' % (d_line2color[line], d_line2seq[line] ) )
                else:
                    s_line+= '<TD></TD>'
            s_line += '</TR>'
        else:
            s_line = ''


        station = w.getStation(cid)
        if station:
            label = """< <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                            <TR><TD>%d</TD> <TD COLSPAN="6">%d</TD> </TR>
                            <TR> <TD COLSPAN="7">%s</TD> </TR>
                            %s
                         </TABLE> >""" % (w.getTrack(cid), cid, station, s_line)
        else:
            label = """< <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                            <TR><TD>%d</TD> <TD COLSPAN="6">%d</TD> </TR>
                            %s
                         </TABLE> >""" % (w.getTrack(cid), cid, s_line )


        g.add_node( pydot.Node( cid, color=color, label=label ) )


    # create edges
    for cid in l_cid:
        if w.getNext(cid):
            g.add_edge( pydot.Edge( cid, w.getNext(cid) ) )

        if w.getPrevious(cid):
            g.add_edge( pydot.Edge( w.getPrevious(cid), cid ) )

def expandRight( cid, f ):
    '''return a list of all of the cids on the same track'''
    l_cid = [cid]
 
    # walk forwards
    cid_temp = cid
    while True:
        cid_new = w.getNext( cid_temp )
        if not cid_new or f(cid_temp):
            break
        else:
            l_cid.append( cid_new )
            cid_temp = cid_new

    return l_cid

def pswitch(cid):
    '''return true if cid is a switch'''
    return len(w.getNeighbors(cid))>2


w = wmata()
g = pydot.Dot( graph_type='graph')
g.set( 'concentrate', 'true' )
g.set_node_defaults( shape='none' )

l_cid_lines = [3146, 3281, 2599, 2674, 1, 204, 2769, 2928]

l_cid_total = set()
for cid in l_cid_lines:
    l_cid_temp = expandRight( cid, lambda x:False )
    addSegment( g, l_cid_temp )
    l_cid_total |= set(l_cid_temp)

for cid in l_cid_lines:
    for c in expandRight( cid, lambda x:False ):
        if pswitch(c) and w.getNextSwitch(c):
            cid_switch = w.getNextSwitch(c)

            l_cid_temp = expandRight( cid_switch, lambda x:False )
            l_cid_total |= set(l_cid_temp)
            addSegment( g, l_cid_temp  )

            g.add_edge( pydot.Edge( c, cid_switch ) )

            for n in w.getNeighbors( l_cid_temp[-1] ):
                if w.getTrack(n)==1 or w.getTrack(n)==2:
                    g.add_edge( pydot.Edge( l_cid_temp[-1], n ) )    


# print missing cids
#for i in range(1,3486+1):
#    if i not in l_cid_total:
#        print i


g.write_svg( 'all.svg' )

