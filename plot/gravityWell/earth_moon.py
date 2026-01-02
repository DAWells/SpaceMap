"""Earth and moon's gravity"""

import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv
from horizons.code import horizons_api
from gravityWell import colour_field, vector_field
from matplotlib.ticker import LogLocator


res = 500
# Earth, moon and, sun
codes = [10, 399, 301]
# From center of Earth
center = "500@399"

for object in codes:
    ephem = horizons_api.get_horizons_data(OBJECT=object, COORD_CENTER=center)
    filepath = f"gravityWell/data/${object}_ephem.txt"
    with open(filepath, "w") as f:
        f.write(ephem)

planets = []
for object in codes:
    filepath = f"gravityWell/data/${object}_ephem.txt"
    ephem = horizons_api.load_ephemeris(filepath)
    physical_data = horizons_api.load_physical_data(filepath)
    mass_index = [i for i in physical_data.index if re.search(r"Mass,* x* *10", i, re.IGNORECASE)][0]
    mass = float(physical_data[mass_index])
    vol_index = [i for i in physical_data.index if re.search(r"Mean Radius", i, re.IGNORECASE)][0]
    planet = {
        "mass": mass,
        "volume": physical_data[vol_index],
        "x": float(ephem.loc[0, "X"]),
        "y": float(ephem.loc[0, "Y"])
    }
    planets.append(planet)

space_min = np.min([(p['x'], p['y']) for p in planets[1:]])
space_max = np.max([(p['x'], p['y']) for p in planets[1:]])
margin = 0.3
space_min = space_min - margin*(space_max-space_min)
space_max = space_max + margin*(space_max-space_min)
XY = vector_field.space_field(
    space_min,
    space_max,
    res=res
)

gforces = []
for planet in planets:
    M = planet['mass']
    r = np.array([planet['x'], planet['y']])
    # XY = vector_field.space_field(r.min(), r.max(), res=res)
    r_field = vector_field.displacement_field(r=r, XY=XY)
    gmag = vector_field.g_magfield(M=M, r_field=r_field, mg=False)
    gforce = vector_field.g_forcefield(M=M, r_field=r_field, mg=False)
    # Mask pixels in the planet
    distance = np.linalg.norm(r_field, axis=0, keepdims=False)
    mask = distance <= planet['volume']
    mask = np.stack([mask, mask], axis=0)
    gforce[mask] = np.nan
    gforces.append(gforce)

# Sum gforce of all objects
gforce = np.sum(gforces, axis=0)
gmag = np.linalg.norm(gforce, axis=0, keepdims=True)
gmag = np.cbrt(gmag)

# Scaling is applied in vfield_to_angle/magnitude
# So if we want to mask values do it before that
angle = colour_field.vfield_to_angle(gforce)
magnitude = colour_field.vfield_to_magnitude(gforce)
# magnitude = np.cbrt(magnitude)
# rgb = colour_field.angle_magnitude_to_rgb(
#     angle=angle,
#     magnitude=magnitude
# )
# rgb = colour_field.scale_matrix(rgb)

# levels = np.linspace(magnitude.min(), magnitude.max(), 5)
# levels = np.power(
#     np.linspace(
#         np.sqrt(magnitude.min()),
#         np.sqrt(magnitude.max()),
#         5
#     ),
# 2)
# levels = np.sqrt(
#     np.linspace(
#         np.power(magnitude.min(),2),
#         np.power(magnitude.max(),2),
#         5
#     ),
# )
# levels=np.geomspace(magnitude.min(),magnitude.max(), 7)
# levels=LogLocator(
#         subs='auto',
#     ).tick_values(
#         magnitude.min(),
#         magnitude.max(),
#     )
levels=LogLocator(
        subs=[21, 46, 98], #evenly spaced on log scale
    ).tick_values(
    np.nanmin(magnitude),
    np.nanmax(magnitude),
)

fig,ax = plt.subplots()
fig.patch.set_facecolor("#251c2d")
ax.axis("off")
ax.imshow(angle,
    alpha=0.5,
    cmap="twilight",
    interpolation="nearest"
)
ax.contour(magnitude,
    levels=levels,
    # cmap='plasma',
    colors="white",
    alpha=0.3
)
plt.savefig("/mnt/c/Users/david/Pictures/SpaceMap/earthmoon-gravity-well.png")
plt.close()
# plt.show()
