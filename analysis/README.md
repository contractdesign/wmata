
# Missing CircuitIds

Some CircuitIds were not observed to be "lit" by a train crossing them
over a 24-hour period from 10/16/2016 - 10/17/2016.  The file
``missing.txt`` contains the complete list of missing CircuitIds.

This directory contains the following files are offered as support:
- ``missing.txt``: see above
- `TrackCircuits.json`: a cached version of the [Track Circuits API call](https://developer.wmata.com/docs/services/5763fa6ff91823096cac1057/operations/57644238031f59363c586dcb "None")
- `CircuitId_official.txt`: a list of all of the CircuitIds appearing in ``TrackCircuits.json``
- `CircuitId_observed.txt`: a list of all CircuitIds observed from 10/16 - 10/17/2016
- diff.txt: the result of the BASH `diff` command of the preceeding two files
- makefile: file used to generate this data (`make all`)

Note: the sqlite3 database that captured the data is not present in
this directory.
