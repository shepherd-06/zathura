from uuid import uuid4
from .sqlite_definition import ErrorLog, DebugLog, database_connection
from datetime import datetime

class Sqlite_Utility:
    def __init__(self, *args, **kwargs):
        # TODO: should check if database is already connected or not.
        database_connection()  # initiate database connection before doing anything. 

    def insert_error_log(self, user, error_name, error_description, point_of_origin = None):
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
            
    def insert_debug_log(self, user, message_data, point_of_origin=None):
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

    def __error_obj_to_dict(self, error_log_object: ErrorLog):
        return {
            '_id': error_log_object._id,
            'user': error_log_object.user,
            'error_name': error_log_object.error_name,
            'error_description': error_log_object.error_description,
            'point_of_origin': error_log_object.point_of_origin,
            'logged_at': error_log_object.logged_at,
            'is_resolved': error_log_object.is_resolved,
            'resolved_at': error_log_object.resolved_at,
        }

    def __debug_obj_to_dict(self, debug_log_object: DebugLog):
        return {
            "_id": debug_log_object._id,
            "user": debug_log_object.user,
            "message-data": debug_log_object.message_data,
            "point_of_origin": debug_log_object.point_of_origin,
            "logged_at": debug_log_object.logged_at,
        }

    def get_all_error_log(self):
        # returns all error_log table data on a list
        err_logs = ErrorLog.select()
        all_logs = list()
        for logs in err_logs:
            all_logs.append(self.__error_obj_to_dict(logs))
        all_logs.append({"total": len(all_logs)})
        return all_logs

    def get_all_debug_log(self):
        # returns all debug_log table data on a list
        debug_logs = DebugLog.select()
        all_logs = list()
        for log in debug_logs:
            all_logs.append(self.__debug_obj_to_dict(log))
        all_logs.append({"total": len(all_logs)})
        return all_logs

    def get_error_by_user(self, user):
        # returns error generated for a user
        errors = ErrorLog.select().where(ErrorLog.user == user.split())
        all_error_logs = list()
        for err in errors:
            all_error_logs.append(self.__error_obj_to_dict(err))
        all_error_logs.append({"total": len(all_error_logs)})
        return all_error_logs

