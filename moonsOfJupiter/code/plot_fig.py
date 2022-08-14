import ctypes
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

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
    ephemeris = pd.read_csv(filepath, skiprows=start+1, skipfooter=len(lines)-end, header=None, names=columns, engine="python")
    
    return ephemeris

def get_body_name(filepath):
    """Get the name of target body from file header"""
    with open("ephemeris/"+filepath, "r") as f:
        body = f.readlines()[3]
    body = body.split(" ")[3]
    return body

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

# folder = sys.argv[1]
folder = 'uranus'


ephemeris_file_names = os.listdir('C:/Users/David/code/SpaceMap/moonsOfJupiter/data/%s/ephemeris'%folder)
ephemeris_files = [load_ephemeris("C:/Users/David/code/SpaceMap/moonsOfJupiter/data/%s/ephemeris/"%folder+f) for f in ephemeris_file_names]

for ephemeris in ephemeris_files:
    ephemeris['Calendar Date (TDB)'] = ephemeris['Calendar Date (TDB)'].str.replace("A.D. ", "")
    ephemeris['Calendar Date (TDB)'] = pd.to_datetime(ephemeris['Calendar Date (TDB)'])

# Plot

fig = plt.figure(figsize=(30,15))
fig.patch.set_facecolor("#251c2d")

gs = fig.add_gridspec(nrows=2, ncols=4)
ax = []

ax.append(fig.add_subplot(gs[0, 0]))
ax[-1].axis('off')

ax.append(fig.add_subplot(gs[0:2, 1:3]))
ax[-1].axis('off')

for df in ephemeris_files:
    # Limit to data upto and including today
    df = df[df['Calendar Date (TDB)'] <= pd.Timestamp.today()]
    # Limit to within the last 3 months
    df = df[df['Calendar Date (TDB)'] > pd.Timestamp.today() - pd.Timedelta(90, 'days')]
    neon_plot(df.X, df.Y, colour='#fd8f24')

#Plot central body
# plt.scatter(0,0, c="#fd8f24", s=50, zorder=10)
neon_point(pd.Series(0), pd.Series(0), colour="#83fdff")

# Set plot limits
plt.xlim([x*1.1 for x in plt.xlim()])
plt.ylim([x*1.1 for x in plt.ylim()])

# ax.append(fig.add_subplot(gs[2, 2]))
# ax[-1].scatter(range(5),range(5))

ax.append(fig.add_subplot(gs[0, 3]))
ax[-1].axis('off')
lastdate = df['Calendar Date (TDB)'].dt.strftime('%Y-%b-%d').iloc[-1]
ax[-1].text(0,0.5, lastdate, color="#f0e8da",
           fontsize=10,# **font
           )
plt.savefig(f"C:/Users/David/code/SpaceMap/moonsOfJupiter/data/{folder}/moons_of_{folder}.png")

# plt.show()

##########
#Update background
##########
ctypes.windll.user32.SystemParametersInfoW(20, 0, f"C:/Users/David/code/SpaceMap/moonsOfJupiter/data/{folder}/moons_of_{folder}.png", 3)