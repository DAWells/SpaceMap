""" Preprocess solar system """

from preprocess import horizons
import pandas as pd

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

ephemeris = []
for code in codes:
    planet_emphemeris, _  = horizons.parse_horizons(f"data/external/solarWindRose/{code}_ephem.txt")
    planet_emphemeris['body_code'] = code
    ephemeris.append(planet_emphemeris)

ephemeris = pd.concat(ephemeris)
ephemeris = ephemeris.drop_duplicates(subset=["body_code"])

ephemeris.to_csv("data/processed/solarWindRose/planets.csv")
