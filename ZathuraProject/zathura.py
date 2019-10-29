import inspect
from datetime import datetime

from ZathuraProject.bugtracker import send_data_to_bugtracker, send_verbose_log_to_bugtracker


class Zathura:
    def __init__(self, bugtracker_url: str = None, project_token: str = None):
        self.empty_result = {'error': True}
        self.verbose_url = None
        self.error_url = None
        self.project_token = project_token

        if bugtracker_url is not None:
            if bugtracker_url[-1:] != '/':
                bugtracker_url += '/'
            self.error_url = bugtracker_url + "project/error/log/"
            self.verbose_url = bugtracker_url + "project/verbose/log/"

    def send_error_log_bugtracker(self, error_name, error_description, user=None):
        """
        sends error log data on bugtracker website

        :returns: bool
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

    def send_verbose_log_bugtracker(self, descrption=None, user=None):
        """
        Sends the verbose log to bugtracker website.

        :returns: bool
        """
        point_of_origin = (inspect.stack()[1].function).lower()
        if self.verbose_url is not None:
            return send_verbose_log_to_bugtracker(
                origin=point_of_origin,
                description=descrption,
                project_token=self.project_token,
                bugtracker_url=self.verbose_url,
                user=user
            )
        return False
