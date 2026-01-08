#!/usr/bin/env bash

# First positional argument is a folder in data/
# which contains a text file, moon_list.txt, with
# a single ephemeris ID on each line

mapfile -t variables < data/$1/input.txt
declare "${variables[@]}"

# Load moons
# readarray -t moons < data/moons_jupiter.txt
# readarray -t moons < data/uranus/moon_list.txt
# For some fucking reason the array is not quite the same 
# if it's not defined manually
# readarray moons < data/${1}/moon_list.txt

#uranus
moons=(723 716 720 721 717 724 718 719)

rm data/$1/ephemeris/*

#moonLauncher
for I in ${moons[@]};do
	echo $I
	code/expect_horizon $I $COORD_CENTER $START $END $INTERVAL
	python3 code/write_ftp_instructions_bash.py $1
	data/ftp_instructions_bash.sh
	echo "We didn't use that moon anyway."
done

# Plot
python3 code/plot_fig.py $1