#!/usr/bin/env bash
HOST='ssd.jpl.nasa.gov'
USER='ftp'
PASSWD='spacemap@gmail.com'
FILE='wld29518.15'

ftp -n $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
pass
cd /pub/ssd/
get $FILE data/uranus/ephemeris/$FILE
quit
END_SCRIPT
exit 0
