
DEMO_KEY=6b700f7ea9db408e9745c207da7ca827
CMD_CURL=curl -H "api_key: ${DEMO_KEY}" --data-ascii "{body}" -X GET


# get all of the train positions
positions.json:
	${CMD_CURL} "https://api.wmata.com/TrainPositions/TrainPositions?contentType={contentType}" | jq . > positions.json; \
	sleep 5

# get the standard routes

routes.json:
	${CMD_CURL} "https://api.wmata.com/TrainPositions/StandardRoutes?contentType={contentType}" | jq . > routes.json; \
	sleep 5

# stations
stations.json:
	${CMD_CURL} "https://api.wmata.com/Rail.svc/json/jStations" | jq . > stations.json; \
	sleep 5

# circuits
circuits.json:
	${CMD_CURL} "https://api.wmata.com/TrainPositions/TrackCircuits?contentType={contentType}" | jq . > circuits.json

json: positions.json routes.json stations.json circuits.json


CircuitIds.txt:
	./learn.py > CircuitIds.txt

clean:
	-rm -rf *.json *.txt



