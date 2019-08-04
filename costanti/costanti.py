import glob
import os
import ctypes
# import win32api


def get_level_name(num):
    return "LEVEL_"+str(num)+".json"


DEBUG = 0

LEVEL_DIR = "levels\\"
IMAGE_DIR = "immagini\\"
MAX_CLN = 13
MAX_ROW = 18

N_LEVELS = len(glob.glob1(LEVEL_DIR, "*.json"))

# DISPLAY_WIDTH, DISPLAY_HEIGHT = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)  # 1920, 1080
DISPLAY_WIDTH, DISPLAY_HEIGHT = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

ID_NONE = None

ID_BLUE = 'blue'
ID_GREEN = 'green'
ID_PURPLE = 'purple'
ID_RED = 'red'
ID_ORANGE = 'orange'
ID_LIGHT_BLUE = 'light_blue'
ID_YELLOW = 'yellow'
ID_DARK_GREEN = 'dark_green'
ID_BROWN = 'brown'
ID_GREY = 'grey'

ID_SIMPLE = 'simple'
ID_DOUBLE = 'double'
ID_IMMORTAL = 'immortal'

colors = [ID_BLUE, ID_GREEN, ID_PURPLE, ID_RED, ID_ORANGE, ID_LIGHT_BLUE, ID_YELLOW, ID_DARK_GREEN, ID_BROWN]
type_bt = [ID_SIMPLE, ID_DOUBLE, ID_IMMORTAL]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    base_path = os.path.abspath(".")
    path = os.path.join(base_path, relative_path)
    if DEBUG:
        print(path)

    return path
