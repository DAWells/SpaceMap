
from download.horizons import horizons_api

# Planets of the solar system
codes = [
    199,
    299,
    # 399, # We're measuring from Earth
    499,
    599,
    699,
    799,
    899,
    999
]

# Earth's center at Greenwich observatory
center = "500@399"

# Outputdir
outputdir = "data/external/solarWindRose"

for object in codes:
    ephem = horizons_api.get_horizons_data(OBJECT=object, COORD_CENTER=center)
    filepath = f"{outputdir}/{object}_ephem.txt"
    with open(filepath, "w") as f:
        f.write(ephem)

