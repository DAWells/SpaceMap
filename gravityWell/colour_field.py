"""
Convert vector to angle
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv


def d1to3(arr):
    return np.stack([arr[0], arr[1], arr[2]], axis=-1)


def XYtoRad(a):
    return np.arctan2(a[0], a[1])


def XYtoHSV(a):
    return (a[0], 1, a[1])


def scale_matrix(matrix):
    min_val = np.min(matrix)
    max_val = np.max(matrix)
    scaled_matrix = (matrix - min_val) / (max_val - min_val)
    return scaled_matrix


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
