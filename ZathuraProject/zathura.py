import inspect
import logging
from datetime import datetime

from peewee import ModelSelect

from ZathuraProject.bugtracker import send_data_to_bugtracker, send_verbose_log_to_bugtracker
from ZathuraProject.sqlite_definition import (DebugLog, ErrorLog, close_db,
                                              database_connection,
                                              database_start)
from ZathuraProject.utility import Utility


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

    def insert_error_log(self, user, error_name, error_description, warning: int = 0):
        """
        Inserts error log on a sqlite db 
        """
        if error_name is not None and error_description is not None:
            from uuid import uuid4
            try:
                # initiate database connection before doing anything.
                database_connection()
                point_of_origin = (inspect.stack()[1].function).lower()

                error_log = ErrorLog(_id=str(uuid4()),
                                     user="user",
                                     error_name=error_name.lower(),
                                     error_description=error_description,
                                     point_of_origin=point_of_origin,
                                     warning_level=0)
                return error_log.save()  # number of modified rows are returned. (Always be 1)
            except ValueError:
                pass
            except SyntaxError:
                pass
            finally:
                close_db()
        return 0

    def insert_debug_log(self, message_data: str,  developer: str = 'zathura'):
        """
        # Insert debug and verbose logs. Logs will purge after a week.
        # It's not going to print out anything right now.
        developer: the guy who is logging this message. It will be easier to find if u name yourself.
        message_data: what u want to log
        point_of_origin: from where u are logging this message
        """
        if message_data is not None:
            from uuid import uuid4
            # initiate database connection before doing anything.
            database_connection()
            origin = (inspect.stack()[1].function).lower()
            debug_log = DebugLog(_id=str(uuid4()), user=developer,
                                 message_data=message_data, point_of_origin=origin)
            close_db()
            return debug_log.save()
        else:
            return 0
