# Moons of Jupiter 🌔
```
code/moonLauncher.sh [planet]
```
Needs pandas and matplotlib.

- Set `input.txt`, currently the choice of moons are specified in `moonLauncher.sh`
- run `moonLauncher.sh [planet]` in bash (i.e. from within wsl) but from the project's `moonsOfJupiter` folder. `[planet]` is the folder to store the data. This calls `expect_horizon`, `write_ftp_instructions_bash.py`, and `data/ftp_instructions_bash.sh` for each moon. Then it generates the figure using `code/plot_fig.py`. However, the python
libraries needed to plot are not installed in wsl. So call it manually.

- `set_wallpaper.bat` is the batch file that must be scheduled to update the wall
paper.

- `expect_horizon` uses expect to tell horizon to generate the emphemeris data.
- `write_ftp_instuctions` writes the script to get that emphemeris data.
- `ftp_instructions_bash.sh` are these instructions. Alternatively, from the windows cmd prompt run `ftp -s:ftp_instructions.txt` (based on answer [here](https://stackoverflow.com/questions/936108/how-to-script-ftp-upload-and-download)) to get ephemeris data. Not actually used.
- `plot_fig.py` Plots the ephemeris data
- The list of jovian moons is available from [here](https://ssd.jpl.nasa.gov/?sat_ephem)
