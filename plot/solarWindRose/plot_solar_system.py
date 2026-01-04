import os
import datetime
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

planets = pd.read_csv("data/processed/solarWindRose/planets.csv")
masses = pd.read_csv("data/raw/planet_masses.csv")
planetmasses = pd.merge(
    planets,
    masses,
    on="body_code",
    how="outer"
)
# Colour pallete (missing Earth)
planetary_colours = {
    199: "#828585",
    299: "#e68c7c",
    399: "forestgreen",
    499: "#e34057",
    599: "#fd8f24",
    699: "#FFE700",
    799: "#37f4dd",
    899: "#018aee",
    999: "#f8eed1"
}

# Prepare data
# Get bearing angle
planets['theta'] = planets.apply(lambda x: math.atan(x.Y/x.X) if x.X >= 0 else (math.atan(x.Y/x.X) - np.pi), axis=1)
# Get XY distance
planets['distance'] = planets.apply(lambda x: np.sqrt((x.X**2) + (x.Y**2)), axis=1)
theta = planets.theta
radii = np.cbrt(planets.distance)
radii = radii/radii.max()
#Fixed area of bars (ignoring curvature)
fab = np.pi/10
width = [fab]*8
width = fab/np.cbrt(radii)
colours = planets.body_code.apply(lambda x: planetary_colours[x])

# Create figure
fig = plt.figure()
fig.patch.set_facecolor("#251c2d")

# Use GridSpec for customising layout
gs = fig.add_gridspec(nrows=10, ncols=10)
ax = []

# Date
ax.append(fig.add_subplot(gs[1,9]))
ax[-1].axis('off')
#font = {'fontname':'Times New Roman'}
datestring = planets.datetime.iloc[0]
datestring = pd.to_datetime(datestring.replace(" TDB", ""), format="%Y-%b-%d %H:%M:%S.%f")
datestring = datestring.strftime("%d %b %Y")
ax[-1].text(
    0,0.5,
    datestring,
    color="#f0e8da",
    fontsize=10,# **font
)

# Wind rose
ax.append(fig.add_subplot(gs[0:9,1:9], projection="polar", facecolor="#251c2d"))
ax[-1].spines['polar'].set_visible(False)
ax[-1].axis('off')
# Add each planet as a separate bar to control zorder
for i,row in planets.reset_index(drop=True).iterrows():
    ax[-1].bar(
        theta[i],
        radii[i],
        width=width[i],
        color=colours[i],
        alpha=1,
        edgecolor="None",
        bottom=0.1,
        zorder=1/radii[i]
    )

# Planet size side bar
for i,row in planetmasses.reset_index(drop=True).iterrows():
    i
    row
    ax.append(fig.add_subplot(gs[i+1,0], facecolor="#251c2d"))
    ax[-1].axis('off')
    ax[-1].scatter(
        0,
        0,
        color = planetary_colours[row.body_code],
        s=row['Vol. Mean Radius (km)']/200
)

plt.show()