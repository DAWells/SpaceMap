#!/bin/bash

#moonLauncher
for I in 501	502	503	504 505	514	515	516 506	507	508	509	510	511	512	513	517	518	519	520	521	522	523	524	525	526	527	528	529	530	531	532	533	534	535	536	537	538	539	540	541	542	543	544	545	546	547	548	549	550	551	552	553 55060	55061	55062	55063	55064	55065	55066	55067	55068	55069	55070	55071	55074	55075
do
	echo $I
	./expect_horizon $I
	python ./write_ftp_instructions_bash.py
	../data/ftp_instructions_bash.sh
	echo "We didn't use that moon anyway."
done