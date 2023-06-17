import os
import sys

from get_sys import getSystemInfo

# ------------------------------------------------------- #

PROJECT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
SYS = getSystemInfo()

BASE_FILTERS = [
    "private",
    "work",
    "family"
]

BASE_SETTINGS = {
    "user": {
        "uuid": ""
    },
    "color": {
        "theme": "Dark",
        "primary": "Red",
        "hue": "500"
    },
    "encryption": {
        "level": 5
    },
    "session": {
        "filter": ""
    }
}