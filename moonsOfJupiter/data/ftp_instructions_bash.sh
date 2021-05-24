#!/bin/sh
HOST='ssd.jpl.nasa.gov'
USER='ftp'
PASSWD='yeohwells@gmail.com'
FILE='wld1787.15'

ftp -n $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
pass
cd /pub/ssd/
get $FILE ../data/ephemeris/$FILE
quit
END_SCRIPT
exit 0
