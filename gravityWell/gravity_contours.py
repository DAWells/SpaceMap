import os
import datetime
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ctypes

def load_ephemeris(filepath):
    """Load HORIZONS ephemeris data into pandas dataframe"""

    #Read in ephemeris file
    with open(filepath, "r") as ephemeris:
        lines = ephemeris.readlines()

    #Get line number with start and end of ephemeris symbol
    start = [i for i,line in enumerate(lines) if "$$SOE" in line][0]
    end = [i for i,line in enumerate(lines) if "$$EOE" in line][0]

    # Get column names as two lines before start of ephemeris data
    columns = lines[start-2].split(",")
    columns = [name.strip() for name in columns]
    columns

    # Read the lines between start and end of ephemeris symbols
    # use identified columns as column names
    ephemeris = pd.read_csv(filepath, skiprows=start+1, skipfooter=len(lines)-end, header=None, names=columns)
    return ephemeris

###################
#                 #
#    Load data    #
#                 #
###################
# Load ephemeris data
datadir = "solarWindRose/data"

# Get today's date in the same calendar date format
calendarDateToday = datetime.datetime.now().strftime("%Y-%b-%d")

planets = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

planet_data = []
for planet in planets:
    df = load_ephemeris(f"{datadir}/{planet.lower()}.15")
    istoday = df['Calendar Date (TDB)'].str.contains(calendarDateToday)
    df = df[istoday]
    df['planet'] = planet
    planet_data.append(df)

planet_data = pd.concat(planet_data)
#Load mass and volume data
masses = pd.read_csv(f"{datadir}/planet_masses.csv")

planet_data = pd.merge(planet_data, masses, how="left", on="planet")

planet_data['normalised_mass'] = planet_data['Mass (kg)']/planet_data['Mass (kg)'].max()

plt.scatter(planet_data.X, planet_data.Y)
plt.scatter(planet_data.X, planet_data.Y, s=planet_data.normalised_mass*10000)
plt.show()

###########################
#                         #
#    Calculate gravity    #
#                         #
###########################

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = np.linspace(planet_data.X.min(), planet_data.X.max(), 50)
Y = np.linspace(planet_data.Y.min(), planet_data.Y.max(), 50)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()


############
#
# Surface plot
#
##############
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()