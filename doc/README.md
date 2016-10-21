# Documentation
This directory contains documentation on the WMATA system.

- `CircuitIds.txt`: a summary of the circuit ids used by each line (do `make CircuitIds.txt` to create)
- `make json`: retrieve the JSON files via WMATA API


## Observations from circuits.json
The system has 4 tracks, numbered from 0 to 3.

CircuitIds are integers from 1 to 3486 that uniquely indicate the
position of a train on a track in the system.

Each CircuitId belongs to 1 of the 4 tracks.



