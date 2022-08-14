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
    "open ssd.jpl.nasa.gov\n",
    "ftp\n",
    "spacemap@gmail.com\n",
    "cd /pub/ssd/\n",
    "get " + ephemeris_file_name + " data/%s/ephemeris/" %(folder) + ephemeris_file_name + "\n",
    "quit"
]

with open("ftp_instructions_windows.txt", "w") as f:
    for instruction in instructions:
        f.write(instruction)