"""Jupiter's Galilean moons gravity"""

import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv
import scipy.constants
from horizons.code import horizons_api
from gravityWell import colour_field, vector_field
from matplotlib.ticker import LogLocator


res = 100

# planet codes
codes = [199, 299, 399, 499]
# earth center
center = "000@399"

# galilean moons, and Jupiter
codes = [501, 502, 503, 504]
# From center of Jupiter
center = "500@599"

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
    try:
        mass_index = [i for i in physical_data.index if re.search(r"Mass x *10", i, re.IGNORECASE)][0]
        mass = float(physical_data[mass_index])
    except IndexError:
        mass = np.nan
    massG_index = [i for i in physical_data.index if re.search(r"GM *\(km\^3/s\^2\)", i, re.IGNORECASE)][0]
    massG = float(physical_data[massG_index])
    vol_index = [i for i in physical_data.index if re.search(r"Mean Radius \(km\)", i, re.IGNORECASE)][0]
    planet = {
        "mass": mass,
        "massG": massG,
        "volume": physical_data[vol_index],
        "x": float(ephem.loc[0, "X"]),
        "y": float(ephem.loc[0, "Y"])
    }
    planets.append(planet)

space_min = np.min([(p['x'], p['y']) for p in planets])
space_max = np.max([(p['x'], p['y']) for p in planets])
margin = 0.5
space_min = space_min - margin*(space_max-space_min)
space_max = space_max + margin*(space_max-space_min)
XY = vector_field.space_field(
    space_min,
    space_max,
    res=res
)

gforces = []
for planet in planets:
    Mg = planet['massG']
    r = np.array([planet['x'], planet['y']])
    # XY = vector_field.space_field(r.min(), r.max(), res=res)
    r_field = vector_field.displacement_field(r=r, XY=XY)
    gmag = vector_field.g_magfield(M=Mg, r_field=r_field, mg=True)
    gforce = vector_field.g_forcefield(M=Mg, r_field=r_field, mg=True)
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
magnitude = np.cbrt(magnitude)
rgb = colour_field.angle_magnitude_to_rgb(
    angle=angle,
    magnitude=magnitude
)
rgb = colour_field.scale_matrix(rgb)

interpolation = None
# interpolation = "bilinear"
mosaic = [
    ['rgb','angle', 'mag'],
    ['location','contour',''],
]
fig,ax = plt.subplot_mosaic(mosaic, sharex=True, sharey=True)
ax['rgb'].imshow(rgb, interpolation=interpolation)
ax['angle'].imshow(angle, interpolation=interpolation, cmap="hsv")
ax['mag'].imshow(magnitude, interpolation=interpolation)
ax['location'].scatter(
    ([p['x'] for p in planets]-space_min)/(space_max-space_min) * res,
    ([p['y'] for p in planets]-space_min)/(space_max-space_min) * res,
    c=[p['massG'] for p in planets]
)
ax['contour'].contour(
    magnitude,
    # levels=20,
    levels=LogLocator(
        subs='auto',
    ).tick_values(
        magnitude.min(),
        magnitude.max(),
    ),
    cmap='plasma',
)
plt.show()


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(XY[0], XY[1], gmag[0,:,:], cmap="plasma")
plt.show()

plt.imshow(angle,
    # alpha=0.5,
    cmap="twilight"
)
plt.contour(magnitude,
    levels=20,
    # cmap='plasma',
    colors="white"
)
plt.show()

