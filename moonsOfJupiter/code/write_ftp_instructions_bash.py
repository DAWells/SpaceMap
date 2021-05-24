import os

os.chdir("../data")

# Open file with ephemeris file name
with open("ephemeris_file_name.txt", "r") as f:
    # The name is the first line,
    # strip the white space
    ephemeris_file_name = f.readlines()[0].strip()
ephemeris_file_name

instructions = [
    "#!/bin/sh\n",
    "HOST='ssd.jpl.nasa.gov'\n",
    "USER='ftp'\n",
    "PASSWD='yeohwells@gmail.com'\n",
    "FILE='%s'\n"%(ephemeris_file_name),
    "\n",
    "ftp -n $HOST <<END_SCRIPT\n",
    "quote USER $USER\n",
    "quote PASS $PASSWD\n",
    "pass\n",
    "cd /pub/ssd/\n",
#     "get $FILE ephemeris/%s\n" %(ephemeris_file_name),
    "get $FILE ../data/ephemeris/$FILE\n",
    "quit\n",
    "END_SCRIPT\n",
    "exit 0\n"
]

with open("ftp_instructions_bash.sh", "wb") as f:
    for instruction in instructions:
        f.write(bytes(instruction, "UTF-8"))