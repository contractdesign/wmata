

import json

class wmata(object):
    'lookup the track # for a cid'
    d_cid2entry = dict()

    'lookup the station data for a cid'
    d_code2station = dict()
    d_cid2station = dict()

    'look up the route data for a cid'
    d_cid2route  = dict()
    

    def __init__(self):
        with open('json/circuits.json') as file_circuits:
            circuits = json.load( file_circuits )

        for tc in circuits['TrackCircuits']:
            self.d_cid2entry[ tc['CircuitId'] ] = tc

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

    def getData( self, cid ):
        '''return the entry associated with that cid'''
        return self.d_cid2entry.get( cid, None )

    def getTrack( self, cid ):
        '''return the track # for that cid'''
        return self.getData(cid)['Track']

    def getNeighbors(self, cid):
        '''return a tuple with lists of the left and right neighbors'''
        left = next((n['CircuitIds'] for n in self.getData(cid)['Neighbors'] if n['NeighborType']=='Left'), None)
        right = next((n['CircuitIds'] for n in self.getData(cid)['Neighbors'] if n['NeighborType']=='Right'), None)
        return (left, right)


    def allCids( self ):
        '''return all of the cids in the system'''
        return self.d_cid2entry.keys()

    def getEndCids( self ):
        l_cid = []
        for cid in self.d_cid2entry.keys():
            l, r = self.getNeighbors(cid)
            if not l or not r:
                l_cid.append( cid )
        return l_cid

    def getSwitchCids( self ):
        l_cid = []
        for cid in self.allCids():
            l, r = self.getNeighbors( cid )
            if l and r and len(l) + len(r) > 2:
                l_cid.append(cid)
        return l_cid

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

    def getPrev( self, cid, track, same=True ):
        track = self.getTrack( cid )

        left, right = self.getNeighbors(cid)

        if left:
            for n in left:
                if same:
                    if self.getTrack( n )==track: 
                        return n
                else:
                    if self.getTrack( n )!=track:
                        return n

        return None

    def getNext( self, cid, track, same=True ):
        track = self.getTrack( cid )

        left, right = self.getNeighbors(cid)
        if right:
            for n in right:
                if same:
                    if self.getTrack( n )==track: 
                        return n
                else:
                    if self.getTrack( n )!=track: 
                        return n

        return None

    def followSwitch( self, cid ):
        l_cid = [cid]

        track = self.getTrack(cid)
        left, right = self.getNeighbors(cid)

        # follow successors
        cid_next = None
        for r in right:
            if self.getTrack(r) != track:
                cid_next = r
                l_cid.append(cid_next)
                break
        if cid_next==None:
            print 'error'
            exit
        print l_cid
        exit
        while True:
            left, right = self.getNeighbors(cid_next)
            if not right or self.getTrack(cid_next)==2:
                break
            cid_next = right[0]
            l_cid.append( cid_next)
        return l_cid


    def expandCid( self, cid, same=True ):
        '''return a list of all of the cids on the same track'''
        
        l_cid = [cid]

        track = self.getTrack(cid)

        cid_temp = cid
        while True:
            cid_new = self.getNext( cid_temp, track, same )
            if not cid_new:
                break

            l_cid.append( cid_new )
            cid_temp = cid_new

        cid_temp = cid
        while True:
            cid_new = self.getPrev( cid_temp, track, same )
            if not cid_new:
                break

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

        left, right = self.getNeighbors( cid )
        if left:
            for n in left:
                if self.getTrack(n) != track:
                    print 'l: (%d:%d)' % (self.getTrack(n), n ),

        if right:
            for n in right:
                if self.getTrack(n) != track:
                    print 'r: (%d:%d)' % (self.getTrack(n), n ),
        print



    def printTrackSegment( self, l_cid ):
        map( self.printTrackUnit, l_cid )

        
        
