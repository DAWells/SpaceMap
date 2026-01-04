# Solar Wind Rose ✨

Create a wind rose image based on the relative positions of the planets. The current planetary positions are available through the [JPL HORIZONS interface](https://ssd.jpl.nasa.gov/?horizons).

## Get data: `download_solar_system`
Use `download/horizons/horizons_api.py` to download planet positions.
The location is relative to Greenwich observatory on Earth's surface.
The body codes for plannets are $n$99 where $n$ is the planet number from the sun.

## Preprocess data: `preprocess_solar_system`
Horizons format data is reformatted using `preprocess/horizons.py`.

## Generate figure: `plot_solar_system`.
On the left hand side is each of the 8 planets and pluto (9 in total) arranged nearest to the sun to further from top to bottom. The size of the planet is proportional to the planet's volume. The polar bar plot indicates the direction and distance (ignoring the z dimension) of each planet from Earth, specifically Greenwich observatory by default. The width of each bar is scaled so that, under the assumption that the bars are triangular, the area is fixed.
