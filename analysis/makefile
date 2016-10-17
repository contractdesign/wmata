
#
# makefile for analyzing circuits encountered by trains as they
# pass through their routes
#
# This requires a database of trains and the circuit ids they encountered
# (DB_NAME below)
# To run
# $ make all
#


DB_NAME=positions_2016-10-17.db
DEMO_KEY=6b700f7ea9db408e9745c207da7ca827


#
# download the official list of track circuits from WMATA
#
TrackCircuits.json:
	curl -v -X GET "https://api.wmata.com/TrainPositions/StandardRoutes?contentType={contentType}" -H "api_key: $(DEMO_KEY)" --data-ascii "{body}" | jq . > TrackCircuits.json; \


#
# extract the valid circuit ids from the JSON file to a file
#
CircuitId_official.txt: TrackCircuits.json
	grep CircuitId TrackCircuits.json | cut -d: -f2 | sed -e 's/,//g' -e 's/ //g' | sort -n | uniq > CircuitId_official.txt


#
# create a file with the observed circuit ids
#


make_SQL_commands:
	echo ".output CircuitId_observed.txt" > commands.sq3
	echo "select distinct circuitid from positions order by circuitid;" >> commands.sq3
	echo ".quit" >> commands.sq3


CircuitId_observed.txt: make_SQL_commands
	sqlite3 -batch $(DB_NAME) < commands.sq3
	rm commands.sq3


diff.txt:
	diff CircuitId_observed.txt CircuitId_official.txt > diff.txt


all: clean CircuitId_observed.txt CircuitId_official.txt diff.txt


clean:
	rm -f *.txt *.json

