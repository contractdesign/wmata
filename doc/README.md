# Documentation

This directory contains documentation related to the real-time train position
API offered by WMATA


## Terminology

- Track Circuit: a sensor on the track that reports the presence of a
  train.  It can also report 
- Circuit Id: an integer associated with each Track Circuit


## System Description

The following JSON files were retrieved from the WMATA API (via `make
json`) and contain descriptions of the WMATA track layout and train
positions.

`json/routes.json`: an ordered list of all of the Track Circuits
comprising each line.  This is a static file.

`json/circuits.json`: a list of Track Circuits comprising the entire
system with their connections to adjacent Track Circuits.  This is a
static file.

`json/stations.json`: a list of the stations, the line to which they
belong, their GPS coordinates, and the line to which they belong.

`json/positions.json`: the positions of all of the trains active in
the system.  This data changes every time it is retrieved.


## Derived Information

These files contain information derived from the JSON files.

`CircuitIds.txt` is a summary of the circuit ids used by each line.  This is
created by doing `make CircuitIds.txt`.

`switches.txt` is a listing of all Track Circuits not having exactly
two adjacent Track Circuits.  Those with single neighbors are the end
of a track.  Those with three neighbors are switches.

The system has 4 tracks, numbered from 0 to 3.

CircuitIds are integers from 1 to 3486 that uniquely indicate the
position of a train on a track in the system.  This was verified
through programmatic examination of `json/routes.json`.

Each CircuitId belongs to 1 of the 4 tracks.


## Track Circuits

The sensors on the tracks to detect the position of a train are
[Ansaldo AF-800W AFTC](http://www.ansaldo-sts.com/sites/ansaldosts.message-asp.com/files/manuali-ansaldo/CatalogCutSheets/RSE-1F2_AF-Gen%20II%20Components.pdf) (Audio Frequency Track Circuit)
modules (see [report](http://www.wmata.com/about_metro/board_of_directors/board_docs/092414_3BATOUpdate20140924.pdf), p. 3).
[Alsom Generator II AFTCs](http://www.alstomsignalingsolutions.com/Data/Documents/Track_Circuit_09.pdf) were used previously but were
replaced after a crash in 2009 due to an issue with parasitic
oscillation in the sensors (see [blog](http://www.welovedc.com/2009/07/03/sensors-and-indicators-in-plain-english-wmatas-wee-z-issue/) for an layman's
explanation).

