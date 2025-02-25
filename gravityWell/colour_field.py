"""
Convert vector to angle
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv


def d1to3(arr):
    """Convert 1st dimension to 3rd dimension
    
    It's easier to work with 3D matrices if the 1st dimension
    splites RGB for example. But for plotting it needs to be
    the 3rd dimension"""
    return np.stack([arr[0], arr[1], arr[2]], axis=-1)


def XYtoRad(a):
    """Convert a 2D vector into an angle in radians"""
    return np.arctan2(a[0], a[1])


def XYtoHSV(a):
    """Convert a 2D vector to HSV
    
    1st dimention is Hue, 2nd dimension is value,
    saturation is always 1"""
    return (a[0], 1, a[1])


def scale_matrix(matrix):
    """Normalise a matrix to 0-1"""
    min_val = np.nanmin(matrix)
    max_val = np.nanmax(matrix)
    scaled_matrix = (matrix - min_val) / (max_val - min_val)
    return scaled_matrix

def scale_radian_matrix(matrix):
    """Normalise matrix of radians where min and max are pi"""
    min_val = -np.pi
    max_val = np.pi
    scaled_matrix = (matrix - min_val) / (max_val - min_val)
    return scaled_matrix

def vfield_to_magnitude(vfield):
    magnitude = np.linalg.norm(vfield, axis=0)
    # magnitude = scale_matrix(magnitude)
    return magnitude

def vfield_to_angle(vfield):
    angle = np.apply_along_axis(XYtoRad, axis=0, arr=vfield)
    # angle = scale_matrix(angle)
    return angle

def angle_magnitude_to_rgb(angle, magnitude):
    angle = scale_radian_matrix(angle)
    magnitude = scale_matrix(magnitude)
    mangle = np.stack([angle, magnitude], axis=0)
    hsv = np.apply_along_axis(XYtoHSV, axis=0, arr=mangle)
    # assert (hsv[0] == angle).all()
    # assert (hsv[2] == magnitude).all()
    rgb = np.apply_along_axis(hsv_to_rgb, axis=0, arr=hsv)
    namask = np.isnan(hsv)
    rgb[namask] = np.nan
    np.apply_along_axis(lambda a:"-".join([str(round(x,1)) for x in a]), axis=0, arr=hsv)
    np.apply_along_axis(rgb_to_hsv, axis=0, arr=rgb)
    rgb3 = d1to3(rgb)
    return rgb3

if __name__ == "__main__":
    # field of 2d vectors
    # 1st D to hue, 2nd D to value
    n=4
    x = np.linspace(0, 1, n)
    y = x
    x,y = np.meshgrid(x, y)
    xy = np.stack([x,y], axis=0)
    hsv = np.apply_along_axis(XYtoHSV, axis=0, arr=xy)
    rgb = np.apply_along_axis(hsv_to_rgb, axis=0, arr=hsv)
    # rgb3 = np.stack([rgb[0], rgb[1], rgb[2]], axis=-1)
    rgb3 = d1to3(rgb)
    plt.imshow(
        rgb3
    )
    plt.show()

    # Map 2 values to an angle
    n=12
    x = np.linspace(-1, 1, int(n/2))
    x = np.concat([x, x[::-1]])
    y = np.concat([
        np.linspace(0, 1, int(n/4)),
        np.linspace(1, 0, int(n/4)),
        np.linspace(0, -1, int(n/4)),
        np.linspace(-1, 0, int(n/4))
    ])
    plt.plot(x,y)
    plt.scatter(x,y, c=[np.arctan2(a,b) for a,b in zip(x,y)])
    plt.show()

    # Vector field
    n=40
    x = np.linspace(-1, 1, n)
    x,y = np.meshgrid(x, x)
    xy = np.stack([x,y], axis=0)
    magnitude = np.linalg.norm(xy, axis=0)
    magnitude = scale_matrix(magnitude)
    angle = np.apply_along_axis(XYtoRad, axis=0, arr=xy)
    angle = scale_matrix(angle)
    mangle = np.stack([angle, magnitude], axis=0)
    hsv = np.apply_along_axis(XYtoHSV, axis=0, arr=mangle)
    hsv[0] == angle
    hsv[2] == magnitude
    rgb = np.apply_along_axis(hsv_to_rgb, axis=0, arr=hsv)
    np.apply_along_axis(lambda a:"-".join([str(round(x,1)) for x in a]), axis=0, arr=hsv)
    np.apply_along_axis(rgb_to_hsv, axis=0, arr=rgb)
    rgb3 = d1to3(rgb)

    fig,ax = plt.subplots(3)
    ax[0].imshow(rgb3)
    ax[1].imshow(angle)
    ax[2].imshow(magnitude)
    plt.show()
