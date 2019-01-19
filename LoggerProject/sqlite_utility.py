from uuid import uuid4
from .sqlite_definition import ErrorLog, DebugLog, database_connection
from datetime import datetime

class Sqlite_Utility:
    def __init__(self, *args, **kwargs):
        # TODO: should check if database is already connected or not.
        database_connection()  # initiate database connection before doing anything. 

    def insert_error_log(self, user, error_name, error_description, point_of_origin = None) -> int:
        if user is not None and error_name is not None and error_description is not None:
            error_log = ErrorLog(user = user, error_name = error_name, error_description = error_description, point_of_origin = point_of_origin)
            return error_log.save()  # number of modified rows are returned. (Always be 1)
            # TODO: for future, log if any errors occurred while storing.
        else:
            if user is None:
                print("username cannot be None. It would be easier to log against the user")
            if error_name is None:
                print("log against a specific error_name.")
            if error_description is None:
                print("give an appropiate error_description")
            print("unknown error occurred")
            return 0
            
    def insert_debug_log(self, user, message_data, point_of_origin=None) -> int:
        if user is not None and message_data is not None:
            debug_log = DebugLog(user=user, message_data = message_data, point_of_origin = point_of_origin)
            return debug_log.save()
        else:
            if user is None:
                print("username cannot be None. It would be easier to log against the user") 
            if message_data is None:
                print("message_data should not be NONE. Since it's what you are currently logging to remember right?")
            print("unknown error occurred")
            return 0
