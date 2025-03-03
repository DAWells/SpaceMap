import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.constants
from matplotlib import cm

def space_field(min:float, max:float, res:int):
    """Create the XY grid of space"""
    X = np.linspace(min, max, res)
    Y = np.linspace(min, max, res)
    X, Y = np.meshgrid(X, Y)
    XY = np.stack([X,Y], axis=0)
    return XY


def displacement_field(r, XY):
    """Calculate displacement vector between r and each point in XY plane"""
    r_field = XY - r.reshape((2,1,1))
    return r_field

def g_magfield(M, r_field, mg):
    """Calculat magnitude of gravitation force given a MG or mass and displacment field"""
    distance = np.linalg.norm(r_field, axis=0, keepdims=True)
    if mg:
        g_magnitude = M/distance**2
    else:
        g_magnitude = M * scipy.constants.G/distance**2
    return g_magnitude

def g_forcefield(M, r_field, mg):
    """Calculate gravitation vector field"""
    distance = np.linalg.norm(r_field, axis=0, keepdims=True)
    unit_vectorfield = r_field/distance
    g_magnitude = g_magfield(M, r_field, mg)
    g_vector = g_magnitude * unit_vectorfield
    return g_vector


if __name__ == "__main__":

    planet = {
        "mass": 1e8,
        "x": 1e3,
        "y": 1e4
    }

    M = planet['mass']
    r = np.array([planet['x'], planet['y']])
    XY = space_field(r.min(), r.max(), res=20)
    r_field = displacement_field(r=r, XY=XY)
    gmag = g_magfield(M=M, r_field=r_field)
    gforce = g_forcefield(M=M, r_field=r_field)

    fig, ax = plt.subplots()
    ax.matshow(gmag[0,:,:], cmap="plasma")
    plt.show()

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(XY[0], XY[1], gmag[0,:,:], cmap="plasma")
    plt.show()

    ###########
    filepath = "eg_ephem.txt"
    ephem = load_ephemeris(filepath)
    physical_data = load_physical_data(filepath)
    planet = {
        "x": ephem.loc[0, "X"],
        "y": ephem.loc[0, "Y"],
        "mass": physical_data['Mass x10^23 (kg)      ']
    }

