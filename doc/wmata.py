

import json

class wmata(object):
    'lookup the track # for a cid'
    d_cid2track = dict()
    d_cid2neighbors = dict()
    d_cid2tc = dict()

    'lookup the station data for a cid'
    d_code2station = dict()
    d_cid2station = dict()

    'look up the route data for a cid'
    d_cid2route  = dict()
    

    def __init__(self):
        with open('json/circuits.json') as file_circuits:
            circuits = json.load( file_circuits )

        for tc in circuits['TrackCircuits']:
            self.d_cid2track[ tc['CircuitId'] ] = tc['Track']

        for tc in circuits['TrackCircuits']:
            cid = tc['CircuitId']
            track = tc['Track']
            self.d_cid2tc[cid] = tc

            d_entry = dict()
            for n in tc['Neighbors']:
                if n['NeighborType']=='Left':
                    for c in n['CircuitIds']:
                        if self.getTrack(c)==track:
                            d_entry['previous']=c
                        else:
                            d_entry['previous_switch']=c

                if n['NeighborType']=='Right':
                    for c in n['CircuitIds']:
                        if self.getTrack(c)==track:
                            d_entry['next']=c
                        else:
                            d_entry['next_switch']=c
            self.d_cid2neighbors[cid] = d_entry

        with open('json/stations.json') as file_stations:
            stations = json.load( file_stations )

        for station in stations['Stations']:
            self.d_code2station[ station['Code'] ] = station

        with open('json/routes.json') as file_routes:
            routes = json.load( file_routes )

        for route in routes['StandardRoutes']:
            for tc in route['TrackCircuits']:

                # a circuit could belong to multiple lines
                if tc['CircuitId'] not in self.d_cid2route:
                    self.d_cid2route[ tc['CircuitId'] ]= []

                self.d_cid2route[ tc['CircuitId'] ].append( { 'StationCode': tc['StationCode'],
                                                              'LineCode': route['LineCode'],
                                                              'SeqNum': tc['SeqNum'] } )

                self.d_cid2station[ tc['CircuitId'] ] = self.d_code2station.get( tc['StationCode'], None )

    def getTrack( self, cid ):
        '''return the track # for that cid'''
        return self.d_cid2track.get(cid, None)


    def getPrevious( self, cid ):
        return self.d_cid2neighbors[cid].get( 'previous', None )

    def getNext( self, cid ):
        return self.d_cid2neighbors[cid].get( 'next', None )

    def getPreviousSwitch( self, cid ):
        return self.d_cid2neighbors[cid].get( 'previous_switch', None )

    def getNextSwitch( self, cid ):
        return self.d_cid2neighbors[cid].get( 'next_switch', None )


    def getNeighbors( self, cid ):
        l_cid = []

        cid_temp = self.getPrevious( cid )
        if cid_temp:
            l_cid.append( cid_temp )

        cid_temp = self.getNext( cid )
        if cid_temp:
            l_cid.append( cid_temp )

        cid_temp = self.getPreviousSwitch( cid )
        if cid_temp:
            l_cid.append( cid_temp )

        cid_temp = self.getNextSwitch( cid )
        if cid_temp:
            l_cid.append( cid_temp )

        return l_cid




    def allCids( self ):
        '''return all of the cids in the system'''
        return self.d_cid2track.keys()

    def getEndCids( self ):
        l_cid = []
        for cid in self.d_cid2entry.keys():
            if not self.getPrevious(cid) or not self.getNext(cid):
                l_cid.append(cid)
        return l_cid

#    def getSwitchCids( self ):
#        l_cid = []
#        for cid in self.allCids():
#            if 
#        return l_cid

    def allStationCodes( self ):
        return self.d_code2station.keys()

    def getStationData( self, code ):
        return self.d_code2station.get( code, None )

    def getRoute( self, cid ):
        if cid in self.d_cid2route:
            return self.d_cid2route[cid].get( 'LineCode', '' )
        else:
            return None

    def getSeqNum( self, cid ):
        if cid in self.d_cid2route:
            return self.d_cid2route[cid].get( 'SeqNum', '' )
        else:
            return None

    def getStation( self, cid ):
        '''return the station name for that cid'''
        s = self.d_cid2station.get( cid, None )
        if s:
            return s['Name']
        else:
            return ''

    # TODO add lambda
    def expandSwitch( self, cid ):
        l_cid = [cid]

        # assume that has a switch
        cid_temp = self.getNextSwitch( cid )
        if not cid_temp:
            print 'error'
            exit()

        while True:
            cid_next = self.getNext( cid_temp )
            cid_next_switch = self.getNextSwitch( cid_temp )
            if not cid_next and cid_next_switch:
                l_cid.append( cid_temp )
                l_cid.append( cid_next_switch)
                break

            l_cid.append( cid_temp )
            cid_temp = cid_next

        return l_cid

        


    def expandCid( self, cid ):
        '''return a list of all of the cids on the same track'''
        l_cid = [cid]
 
        # walk forwards
        cid_temp = cid
        while True:
            cid_new = self.getNext( cid_temp )
            if not cid_new:
                break
            else:
                l_cid.append( cid_new )
                cid_temp = cid_new

        # walk backwards
        cid_temp = cid
        while True:
            cid_new = self.getPrevious( cid_temp )
            if not cid_new:
                break
            else:
                # TODO consider deque
                l_cid.insert( 0, cid_new )
                cid_temp = cid_new

        return l_cid


    def getLines( self, cid ):
        l_line = []
        if cid in self.d_cid2route:
            for line in self.d_cid2route[cid]:
                l_line.append( (line['LineCode'], line['SeqNum']) )
        return l_line

    def printTrackUnit( self, cid ):
        track = self.getTrack(cid)
        print '(%d:%d)\t|' % (track, cid),

        lines = self.getLines(cid)
        if lines:
            for line in lines:
                print '%s #%s' % (line[0] , line[1]),
        print '\t', self.getStation( cid ),

        n = self.getPreviousSwitch( cid )
        if n:
            print '/ (%d:%d)' % (self.getTrack(n), n ),

        n = self.getNextSwitch( cid )
        if n:
            print '\ (%d:%d)' % (self.getTrack(n), n ),


        print



    def printTrackSegment( self, l_cid ):
        map( self.printTrackUnit, l_cid )

        
        
