import os
import sys

# First positional argument is a folder in data/
folder = sys.argv[1]

# Open file with ephemeris file name
with open("data/ephemeris_file_name.txt", "r") as f:
    # The name is the first line,
    # strip the white space
    ephemeris_file_name = f.readlines()[0].strip()

ephemeris_file_name

instructions = [
    "#!/usr/bin/env bash\n",
    "HOST='ssd.jpl.nasa.gov'\n",
    "USER='ftp'\n",
    "PASSWD='spacemap@gmail.com'\n",
    "FILE='%s'\n"%(ephemeris_file_name),
    "\n",
    "ftp -n $HOST <<END_SCRIPT\n",
    "quote USER $USER\n",
    "quote PASS $PASSWD\n",
    "pass\n",
    "cd /pub/ssd/\n",
#     "get $FILE ephemeris/%s\n" %(ephemeris_file_name),
    "get $FILE data/%s/ephemeris/$FILE\n"%folder,
    "quit\n",
    "END_SCRIPT\n",
    "exit 0\n"
]

with open("data/ftp_instructions_bash.sh", "wb") as f:
    for instruction in instructions:
        f.write(bytes(instruction, "UTF-8"))