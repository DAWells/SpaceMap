import os

os.chdir("../data")

# Open file with ephemeris file name
with open("ephemeris_file_name.txt", "r") as f:
    # The name is the first line,
    # strip the white space
    ephemeris_file_name = f.readlines()[0].strip()
ephemeris_file_name

instructions = [
    "open ssd.jpl.nasa.gov\n",
    "ftp\n",
    "yeohwells@gmail.com\n",
    "cd /pub/ssd/\n",
    "get " + ephemeris_file_name + " ../data/ephemeris/" + ephemeris_file_name + "\n",
    "quit"
]

with open("ftp_instructions_windows.txt", "w") as f:
    for instruction in instructions:
        f.write(instruction)