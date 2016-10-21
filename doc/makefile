
DEMO_KEY=6b700f7ea9db408e9745c207da7ca827


# get all of the train positions
positions.json:
	curl -v -X GET "https://api.wmata.com/TrainPositions/TrainPositions?contentType={contentType}" -H "api_key: ${DEMO_KEY}" --data-ascii "{body}" | jq . > positions.json; \
	sleep 5

# get the standard routes

routes.json:
	curl -v -X GET "https://api.wmata.com/TrainPositions/StandardRoutes?contentType={contentType}" -H "api_key: ${DEMO_KEY}" --data-ascii "{body}" | jq . > routes.json; \
	sleep 5

# stations
stations.json:
	curl -v -X GET "https://api.wmata.com/Rail.svc/json/jStations" -H "api_key: ${DEMO_KEY}" | jq . > stations.json; \
	sleep 5

# circuits
circuits.json:
	curl -v -X GET "https://api.wmata.com/TrainPositions/TrackCircuits?contentType={contentType}" -H "api_key: ${DEMO_KEY}" --data-ascii "{body}" | jq . > circuits.json

all: positions.json routes.json stations.json circuits.json

clean:
	-rm -rf *.json


