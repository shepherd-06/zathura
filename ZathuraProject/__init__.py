import inspect
import os
import sys
import time
from datetime import datetime
from uuid import uuid4

import pkg_resources
import pyfiglet

from ZathuraProject.bugtracker import (send_data_to_bugtracker,
                                       send_verbose_log_to_bugtracker)

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
    """
    Prints out Zathura using pyfiglet package, speed font.
    """
    print(pyfiglet.figlet_format("Zathura", font="speed"))


class Zathura:
    def __init__(self, bugtracker_url: str = None,
                 project_token: str = None):
        """
        Initiates zathura using bugtracker url and project token.
        
        :param: bugtracker_url: str 
        :param: project_token: str
        """
        self.verbose_url = None
        self.error_url = None
        self.project_token = project_token

        if bugtracker_url is not None:
            if bugtracker_url[-1:] != '/':
                bugtracker_url += '/'
            self.error_url = bugtracker_url + "project/error/log/"
            self.verbose_url = bugtracker_url + "project/verbose/log/"

    def log_error(self, error_name, error_description, user=None):
        """
        logs error in bugtracker server.
        
        :param: error_name, error name.
        :param: error_description: str This should include all the necessary details of an exception.
        :param: user: str It's an optional field. This will help to uniquely identify a user.

        :returns: bool whether log has been logged successfully
        """
        point_of_origin = (inspect.stack()[1].function).lower()
        if self.error_url is not None:
            return send_data_to_bugtracker(
                name=error_name,
                description=error_description,
                origin=point_of_origin,
                token=self.project_token,
                url=self.error_url,
                user=user
            )
        return False

    def log_verbose(self, description=None, user=None):
        """
        logs verbose (debug) in bugtracker server.
        
        :param: description: str This could be a long description of any debug message you want to see.
        :param: user: str It's an optional field. This will help to uniquely identify a user.

        :returns: bool whether log has been logged successfully
        """
        point_of_origin = (inspect.stack()[1].function).lower()
        if self.verbose_url is not None:
            return send_verbose_log_to_bugtracker(
                origin=point_of_origin,
                description=description,
                project_token=self.project_token,
                bugtracker_url=self.verbose_url,
                user=user
            )
        return False
