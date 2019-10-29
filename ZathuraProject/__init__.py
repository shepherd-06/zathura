import os
import sys
import time
from datetime import datetime
from uuid import uuid4

import pkg_resources
import pyfiglet

from ZathuraProject.zathura import Zathura

CURRENT_VERSION = "v0.0.6 beta"


def create_app():
    if sys.version_info < (3, 0, 0):
        print("Zathura needs python3.x to perform normally!")
        sys.exit(255)

    pyfiglet_ascii()  # spits out zathura in speed font

    print("*#$" * 20)
    print("Current version: {}".format(CURRENT_VERSION))
    print("*#$" * 20)
    return


def pyfiglet_ascii():
    print(pyfiglet.figlet_format("Zathura", font="speed"))
