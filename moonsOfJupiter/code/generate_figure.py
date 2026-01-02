import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv
from horizons.code import horizons_api
from gravityWell import colour_field, vector_field
from matplotlib.ticker import LogLocator
from datetime import datetime, timedelta

res = 500
# galilean moons, and Jupiter
codes = [500, 501, 502, 503, 504]
# From center of Jupiter
center = "500@599"

today = datetime.today()
END = today.strftime("%Y-%b-%d")
START = today - timedelta(days=5)
START = START.strftime("%Y-%b-%d")

for object in codes:
    ephem = horizons_api.get_horizons_data(
        OBJECT=object,
        COORD_CENTER=center,
        START=START,
        END=END
    )
    filepath = f"gravityWell/data/${object}_ephem.txt"
    with open(filepath, "w") as f:
        f.write(ephem)

planets = []
for object in codes:
    filepath = f"gravityWell/data/${object}_ephem.txt"
    ephem = horizons_api.load_ephemeris(filepath)
    planets.append(ephem)

def neon_plot(x, y, n_lines=5, colour="#83fdff"):
#     n_lines = 5
    for i in range(1,n_lines):
        plt.plot(x, y, c=colour,
                 linewidth=10*i,
                 alpha=0.03,
                 solid_capstyle="round")

    plt.plot(x, y, c=colour, solid_capstyle="round")
#     plt.plot(x, y, c="white", linewidth=0.5)
    plt.scatter(x.iloc[-1], y.iloc[-1], c=colour)

def neon_point(x, y, n_lines=5, colour="#83fdff"):
#     colour = "#83fdff"
#     n_lines = 5
    for i in range(1,n_lines):
        plt.scatter(x.iloc[-1], y.iloc[-1], c=colour,
                 s=100*i,
                 alpha=0.03,
                 zorder=5
                )
    plt.scatter(x.iloc[-1], y.iloc[-1], c=colour)


fig = plt.figure(figsize=(30,30))
fig = plt.figure()
fig.patch.set_facecolor("#251c2d")

gs = fig.add_gridspec(nrows=3, ncols=3)
ax = []

ax.append(fig.add_subplot(gs[0:2, 0:2]))
ax[-1].axis('off')

neon_point(df.X, df.Y)
neon_plot(df.X, df.Y)

for df,name in zip(ephemeris_files, bodynames):
    if name in innerMoons:
#         pass
        neon_point(df.X, df.Y)
    elif name in galileanMoons:
#         pass
        neon_point(df.X, df.Y)
        if df.X.iloc[-1]>0:
            plt.text(df.X.iloc[-1], df.Y.iloc[-1]+0.005, 
                     name, horizontalalignment="left",
                     color="#f0e8da", fontsize=10)
        else:
            plt.text(df.X.iloc[-1], df.Y.iloc[-1]+0.005, 
                     name, horizontalalignment="right",
                     color="#f0e8da", fontsize=10)
    else:
#         pass
        neon_plot(df.X, df.Y)

#Plot central body
# plt.scatter(0,0, c="#fd8f24", s=50, zorder=10)
neon_point(pd.Series(0), pd.Series(0), colour="#fd8f24")


# ax.append(fig.add_subplot(gs[2, 2]))
# ax[-1].scatter(range(5),range(5))

ax.append(fig.add_subplot(gs[0, 1]))
ax[-1].axis('off')
lastdate = df['Calendar Date (TDB)'].dt.strftime('%Y-%b-%d').iloc[-1]
lastdate = df['date_str']#.dt.strftime('%Y-%b-%d').iloc[-1]
ax[-1].text(0,0.5, lastdate, color="#f0e8da",
    fontsize=10,# **font
)
plt.show()