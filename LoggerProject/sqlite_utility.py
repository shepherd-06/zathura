from uuid import uuid4
from .sqlite_definition import ErrorLog, DebugLog, database_connection
from datetime import datetime
from .utility import Utility
from peewee import ModelSelect

class Sqlite_Utility:
    def __init__(self, *args, **kwargs):
        # TODO: should check if database is already connected or not.
        database_connection()  # initiate database connection before doing anything. 
        self.empty_result = {"total": 0, "log": []}

    def insert_error_log(self, user:str, error_name:str, error_description:str, point_of_origin:str):
        if user is not None and error_name is not None and error_description is not None and point_of_origin is not None:
            from uuid import uuid4
            error_log = ErrorLog(_id = str(uuid4()),user = user, error_name = error_name.lower(), error_description = error_description, point_of_origin = point_of_origin.lower())
            return error_log.save()  # number of modified rows are returned. (Always be 1)
            # TODO: for future, log if any errors occurred while storing.
        else:
            if user is None:
                print("username cannot be None. It would be easier to log against the user")
            if error_name is None:
                print("log against a specific error_name.")
            if error_description is None:
                print("give an appropiate error_description")
            if point_of_origin is None:
                print("Provide appropiate error entry registry for better understanding!")
            print("unknown error occurred")
            return 0
            
    def insert_debug_log(self, message_data:str, point_of_origin:str =None,  developer:str = 'Logger_Test_User'):
        """
        Insert debug and verbose logs. Logs will purge after a week.
        developer: the guy who is logging this message. It will be easier to find if u name urself.
        message_data: what u want to log
        point_of_origin: from where u are logging this message
        It's not going to print out anything right now.
        """
        if message_data is not None:
            from uuid import uuid4
            debug_log = DebugLog(_id = str(uuid4()), user=developer, message_data = message_data.lower(), point_of_origin = point_of_origin.lower() if point_of_origin is not None else None)
            return debug_log.save()
        else: 
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
    
    def __generate_error_return_payload(self, log_paylod: ModelSelect):
        """
        generates error payload for return
        """
        all_error_logs = list()
        for err in log_paylod:
            all_error_logs.append(self.__error_obj_to_dict(err))
        return {"total": len(all_error_logs), "log": all_error_logs}

    def __generate_verbose_return_payload(self, debug_payload: ModelSelect):
        """
        generates debug payload for return
        """
        all_logs = list()
        for log in debug_payload:
            all_logs.append(self.__debug_obj_to_dict(log))
        return {"total": len(all_logs), "log": all_logs}

    def get_all_error_log(self):
        # returns all error_log table data on a list
        err_logs = ErrorLog.select()
        return self.__generate_error_return_payload(err_logs)

    def get_all_debug_log(self):
        # returns all debug_log table data on a list
        debug_logs = DebugLog.select()
        return self.__generate_verbose_return_payload(debug_logs)

    def get_error_by_user(self, user: str, limit: int=0, asc:bool = True):
        # returns error generated for a user
        if len(user) == 0:
            print("Username cannot be empty for this function!")
            return self.empty_result
        errors = ErrorLog.select().where(ErrorLog.user == user)
        return self.__generate_error_return_payload(errors)

    def get_error_by_date_limit(self, beginning_limit: datetime, ending_limit: datetime = datetime.now(), limit:int = 0, asc: bool = True):
        if beginning_limit is None:
            print("First date limit cannot be empty!")
            return self.empty_result
        if type(ending_limit) != datetime:
            ending_limit = datetime.now()
        first_limit = Utility.unix_time_millis(beginning_limit)
        last_limit = Utility.unix_time_millis(ending_limit)

        errors = ErrorLog.select().where((ErrorLog.logged_at >= first_limit) & (ErrorLog.logged_at <= last_limit))
        return self.__generate_error_return_payload(errors)

    # def search by error_name
    def get_error_by_error_name(self, error_name: str):
        if error_name is None:
            print("Error name cannot be empty on this search")
            return self.empty_result
        if len(error_name) == 0:
            print("Error name cannot be empty on this search")
            return self.empty_result
        errors = ErrorLog.select().where(ErrorLog.error_name == error_name)
        return self.__generate_error_return_payload(errors)

    # def search by point_of_origin
    def get_error_by_origin(self, origin: str):
        if origin is None:
            print("Point of origin cannot be None")
            return self.empty_result
        if len(origin) == 0:
            print("Point of origin cannot be None")
            return self.empty_result
        errors = ErrorLog.select().where(ErrorLog.point_of_origin == origin.lower())
        return self.__generate_error_return_payload(errors)

    # verbose/debug print out
    def get_debug_by_origin(self, origin: str = '', first_limit: datetime = None, last_limit: datetime = None):
        """
        returns all debug data filters by origin; if neededd.
        first_limit: datetime filters out data before this limit
        last_limit: datetime filters out data after this limit
        origin: str point of origin of any debug msg that needs to be on this list.
        """
        if len(origin) == 0:
            return self.get_all_debug_log()

        if first_limit is None and last_limit is None:
            debugs = DebugLog.select().where(DebugLog.point_of_origin == origin.lower())
        else:
            if first_limit is not None and last_limit is None:
                last_limit = datetime.now()
            first_limit = Utility.unix_time_millis(first_limit)
            last_limit = Utility.unix_time_millis(last_limit)

            debugs = DebugLog.select().where((DebugLog.point_of_origin == origin.lower()) & (DebugLog.logged_at >= first_limit) & (DebugLog.logged_at <= last_limit))
        return self.__generate_verbose_return_payload(debugs)

    # verbose/debug search by developers name
    def get_debug_by_developers(self, developers_name: str = '', first_limit: datetime = None, last_limit: datetime = None):
        """
        returns all debug data filters by developers; if neededd.
        first_limit: datetime filters out data before this limit
        last_limit: datetime filters out data after this limit
        developers_name: str developers_name : who wrote the debug message. For debugging person. Could be None or empty string.
        """
        if len(developers_name) == 0:
            return self.get_all_debug_log()
        if first_limit is None and last_limit is None:
            debugs = DebugLog.select().where(DebugLog.user == developers_name)
        else:
            if first_limit is not None and last_limit is None:
                last_limit = datetime.now()
            first_limit = Utility.unix_time_millis(first_limit)
            last_limit = Utility.unix_time_millis(last_limit)

            debugs = DebugLog.select().where((DebugLog.user == developers_name) & (DebugLog.logged_at >= first_limit) & (DebugLog.logged_at <= last_limit))
        return self.__generate_verbose_return_payload(debugs)

