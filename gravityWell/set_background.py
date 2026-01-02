"""
Set image as background. Must be run in windows environment, not wsl
"""

import os
import ctypes

image_path = r"C:\Users\david\Pictures\SpaceMap\galilean-gravity-well.png"
image_path = r"C:\Users\david\Pictures\SpaceMap\earthmoon-gravity-well.png"

os.path.isfile(image_path)

# Constants for SystemParametersInfo
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

ctypes.windll.user32.SystemParametersInfoW(
    SPI_SETDESKWALLPAPER,
    0,
    image_path,
    SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
)
