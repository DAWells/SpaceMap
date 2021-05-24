# Moons of Jupiter 🌔
- `expect_horizon` script gets ephemeris file name (run in linux but from the `projects/moonsOfJupiter/data` folder)
- and maybe size of body?
- `write_ftp_instructions` puts this file name into a text file that can be run to get the file via ftp `ftp_instructions`
- from the windows cmd prompt run `ftp -s:ftp_instructions.txt` (based on answer [here](https://stackoverflow.com/questions/936108/how-to-script-ftp-upload-and-download)) to get ephemeris data
- alternatively run `./ftp_instructions_bash.sh` from the linux terminal.
- The list of jovian moons is available from [here](https://ssd.jpl.nasa.gov/?sat_ephem)
