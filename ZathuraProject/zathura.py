from ZathuraProject.sqlite_definition import ErrorLog, DebugLog, database_connection
from datetime import datetime
from ZathuraProject.utility import Utility
from peewee import ModelSelect


class Zathura:
    def __init__(self):
        # TODO: should check if database is already connected or not.
        database_connection()  # initiate database connection before doing anything. 
        self.empty_result = {'error': True}

    def insert_error_log(self, user:str, error_name:str, error_description:str, point_of_origin:str, warning:int = 0):
        """
        Inserts error log on a sqlite db
        """
        if user is not None and error_name is not None and error_description is not None and point_of_origin is not None:
            from uuid import uuid4
            try:
                warning = int(warning)
                if warning < 0:
                    warning = 0
                elif warning > 3:
                    warning = 3
                error_log = ErrorLog(_id = str(uuid4()),user = user, error_name = error_name.lower(), error_description = error_description, point_of_origin = point_of_origin.lower(), warning_level=warning)
                return error_log.save()  # number of modified rows are returned. (Always be 1)
            except ValueError:
                # TODO: add logger 
                print("Wrong warning field value")
            except SyntaxError:
                # TODO: add logger
                print("Wrong warning field value")
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
        # Insert debug and verbose logs. Logs will purge after a week.
        # It's not going to print out anything right now.
        developer: the guy who is logging this message. It will be easier to find if u name urself.
        message_data: what u want to log
        point_of_origin: from where u are logging this message
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
        """
        # generates and returns a dictionary from ErrorLog object
        error_log_object: ErrorLog a ErrorLog object
        """
        return {
            'user': error_log_object.user,
            'error_name': error_log_object.error_name,
            'error_description': error_log_object.error_description,
            'point_of_origin': error_log_object.point_of_origin,
            'logged_at': Utility.milli_to_datetime(error_log_object.logged_at),
            'is_resolved': "Resolved" if error_log_object.is_resolved else "Not Resolved",  
            'resolved_at': error_log_object.resolved_at if error_log_object.resolved_at is None else Utility.milli_to_datetime(error_log_object.resolved_at),
            'warning_level': self.__get_warning_level_in_text(error_log_object.warning_level),
        }

    @staticmethod
    def __debug_obj_to_dict(debug_log_object: DebugLog):
        """
        # generates & returns a dictionary from a DebugLog object.
        debug_log_object: DebugLog a DebugLog object
        """
        return {
            "user": debug_log_object.user,
            "message-data": debug_log_object.message_data,
            "point_of_origin": debug_log_object.point_of_origin,
            "logged_at": Utility.milli_to_datetime(debug_log_object.logged_at),
        }
    
    def __generate_error_return_payload(self, log_paylod: ModelSelect):
        """
        # generates error payload for return
        """
        all_error_logs = list()
        for err in log_paylod:
            all_error_logs.append(self.__error_obj_to_dict(err))
        return {"total": len(all_error_logs), "log": all_error_logs}

    @staticmethod
    def __get_warning_level_in_text(warning_level: int):
        _ = {
            '0': 'warning',
            '1': 'Level - 1',
            '2': 'Level - 2',
            '3': 'Critical'
        }
        return _[str(warning_level)]

    def __generate_verbose_return_payload(self, debug_payload: ModelSelect):
        """
        # generates debug payload for return
        """
        all_logs = list()
        for log in debug_payload:
            all_logs.append(self.__debug_obj_to_dict(log))
        return {"total": len(all_logs), "log": all_logs}

    def get_all_error_log(self, show_all: bool = False, desc: bool = False):
        """
        # returns all error_log table data on a list which are not resolved yet
        show_all: bool filters out the is_resolved = True value if show_all is False
        """
        if show_all:
            if desc: 
                err_logs = ErrorLog.select().order_by(ErrorLog.logged_at.desc())
            else:
                err_logs = ErrorLog.select()
        else:
            if desc:
                err_logs = ErrorLog.select().where(ErrorLog.is_resolved != True).order_by(ErrorLog.logged_at.desc())
            else:
                err_logs = ErrorLog.select().where(ErrorLog.is_resolved != True)
        return self.__generate_error_return_payload(err_logs)

    def get_all_debug_log(self):
        """
        # returns all debug_log table data on a list
        """
        debug_logs = DebugLog.select()
        return self.__generate_verbose_return_payload(debug_logs)

    def get_error_by_user(self, user: str, limit: int=0, desc:bool = False, first_limit: datetime = None, last_limit: datetime = None):
        """
        # returns error generated for a user. datetime is not both inclusive, exclude the last date.
        # username is mandatory in this case.
        # ascending order is by default otherwise.
        # ordering is when the error is logged.
        user: str error report generated under a particular user
        limit: int limits the number of error searchable
        desc: bool whether to show the result in ascending or descending order
        first_limit: datetime shows result after this limit
        last_limit: shows result before this limit (exclusive)
        """
        if len(user) == 0:
            result = self.empty_result
            result['message'] = "Username cannot be empty for this function!"
            return result
        user = user.strip()
        if first_limit is None and last_limit is None: 
            if limit != 0:
                if desc:
                    # descending order with limit
                    errors = ErrorLog.select().where(ErrorLog.user == user).order_by(ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # ascending order with limit
                    errors = ErrorLog.select().where(ErrorLog.user == user).limit(limit)
            else:
                if desc:
                    # descending order without limit
                    errors = ErrorLog.select().where(ErrorLog.user == user).order_by(ErrorLog.logged_at.desc())
                else:
                    # ascending order without limit
                    errors = ErrorLog.select().where(ErrorLog.user == user)
        else:
            # filter by datetime. and same limit order
            first_limit = Utility.unix_time_millis(first_limit)
            if last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)
            param_user = (ErrorLog.user == user)
            param_date_filter_one = (ErrorLog.logged_at >= first_limit)
            param_date_filter_two = (ErrorLog.logged_at <= last_limit)
            if limit != 0:
                if desc:
                    # descending order with limit date filter included
                    errors = ErrorLog.select().where(param_user & param_date_filter_one & param_date_filter_two).order_by(ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # ascending order without limit date filter included
                    errors = ErrorLog.select().where(param_user & param_date_filter_one & param_date_filter_two).limit(limit)
            else:
                if desc:
                    # descending order without limit date filter included
                    errors = ErrorLog.select().where(param_user & param_date_filter_one & param_date_filter_two).order_by(ErrorLog.logged_at.desc())
                else:
                    # ascending order without limit date filter included
                    errors = ErrorLog.select().where(param_user & param_date_filter_one & param_date_filter_two)
        return self.__generate_error_return_payload(errors)

    def get_error_by_date_limit(self, beginning_limit: datetime, ending_limit: datetime = None, limit:int = 0, desc: bool = False):
        """
        # get reports under a date limit from all users
        beginning_limit: datetime starting time, inclusive
        ending_limit: datetime ending time, exclusive
        limit: int limits the number of search result.
        desc: bool whether to show the result in descending order
        """
        if beginning_limit is None:
            result = self.empty_result
            result['message'] = "Please insert the first date to search after a specific time."
            return result
        first_limit = Utility.unix_time_millis(beginning_limit)
        if ending_limit is None:
            ending_limit = Utility.current_time_in_milli()
        else:
            last_limit = Utility.unix_time_millis(ending_limit)

        param_filter_one = (ErrorLog.logged_at >= first_limit)
        param_filter_two = (ErrorLog.logged_at <= last_limit)

        if limit != 0:
            if desc:
                # search under a limit in descending order
                errors = ErrorLog.select().where(param_filter_one & param_filter_two).order_by(ErrorLog.logged_at.desc()).limit(limit)
            else:
                # search under a limit in ascending order
                errors = ErrorLog.select().where(param_filter_one & param_filter_two).limit(limit)
        else:
            if desc:
                # search without limit in descending order
                errors = ErrorLog.select().where(param_filter_one & param_filter_two).order_by(ErrorLog.logged_at.desc())
            else:
                # search without limit in ascending order
                errors = ErrorLog.select().where(param_filter_one & param_filter_two)
        return self.__generate_error_return_payload(errors)

    # def search by error_name
    def get_error_by_error_name(self, error_name: str, first_limit: datetime = None, last_limit: datetime = None, limit: int = 0, desc: bool = False):
        """
        # searches errors by error name. filters will be applied based on parameter
        error_name: what's the name of error you want to search under.
        first_limit: first date limit to be applied
        last_limit: last date limit to be applied, not inclusive
        limit: limits the number of data on search result.
        desc: sort the result in descending order or ascending order. (By default, ascending order)
        """
        if error_name is None or len(error_name) == 0:
            result = self.empty_result
            result['message'] = "Error name cannot be empty on this search"
            return result
        error_name = error_name.strip()
        if first_limit is None and last_limit is None:
            if limit != 0:
                if desc:
                    # search with limit in descending order under no date limit
                    errors = ErrorLog.select().where(ErrorLog.error_name == error_name).order_by(ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # search with limit in ascending order under no date limit
                    errors = ErrorLog.select().where(ErrorLog.error_name == error_name).limit(limit)
            else:
                if desc:
                    # search without limit in descending order under no date limit
                    errors = ErrorLog.select().where(ErrorLog.error_name == error_name).order_by(ErrorLog.logged_at.desc())
                else:
                    # search without limit in ascending order under no date limit
                    errors = ErrorLog.select().where(ErrorLog.error_name == error_name)
        else:
            # filter under date limit
            first_limit = Utility.unix_time_millis(first_limit)
            if last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)

            param_filter_one = (ErrorLog.error_name == error_name)
            param_filter_two = (ErrorLog.logged_at >= first_limit)
            param_filter_three = (ErrorLog.logged_at <= last_limit)

            if limit != 0:
                if desc:
                    # search with limit in descending order under date limit
                    errors = ErrorLog.select().where(param_filter_one & param_filter_two & param_filter_three).order_by(ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # search with limit in ascending order under date limit
                    errors = ErrorLog.select().where(param_filter_one & param_filter_two & param_filter_three).limit(limit)
            else:
                if desc:
                    # search without limit in descending order under date limit
                    errors = ErrorLog.select().where(param_filter_one & param_filter_two & param_filter_three).order_by(ErrorLog.logged_at.desc())
                else:
                    # search without limit in ascending order under date limit
                    errors = ErrorLog.select().where(param_filter_one & param_filter_two & param_filter_three)
        return self.__generate_error_return_payload(errors)

    def get_error_by_origin(self, origin: str, first_limit: datetime= None, last_limit: datetime = None, limit:int = 0, desc:bool = False):
        """
        # searches error by point of origin, where the error is originated when the error is logged.
        # But you better catch the error with an except block. and manually register it. 
        origin: str name of the function or class
        first_limit: datetime first date limit for filtering purpose
        last_limit: datetime last date limit to filter out 
        limit: int limits the amount of returned result.
        desc: bool filter the data in descending order (Ascending is by default)
        """
        if origin is not None or len(origin) != 0:
            # Point of origin can be None.
            origin = origin.strip()
            origin = origin.lower()

        if first_limit is None and last_limit is None:
            if limit != 0:
                # search with limit and no date limit applied
                if desc:
                    # show result in descending order with limit but no date filter
                    errors = ErrorLog.select().where(ErrorLog.point_of_origin == origin).order_by(ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # show result in ascending order with limit but no date filter
                    errors = ErrorLog.select().where(ErrorLog.point_of_origin == origin).limit(limit)
            else:
                if desc:
                    # show result in descending order without limit but no date filter
                    errors = ErrorLog.select().where(ErrorLog.point_of_origin == origin).order_by(ErrorLog.logged_at.desc())
                else:
                    # show result in ascending order without but no date filter
                    errors = ErrorLog.select().where(ErrorLog.point_of_origin == origin)
        else:
            first_limit = Utility.unix_time_millis(first_limit)
            if last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)
            filter_param_one = (ErrorLog.point_of_origin == origin)
            filter_param_two = (ErrorLog.logged_at >= first_limit)
            filter_param_three = (ErrorLog.logged_at <= last_limit)
            
            if limit != 0:
                # search with limit and no date limit applied
                if desc:
                    # show result in descending order with limit WITH date filter
                    errors = ErrorLog.select().where(filter_param_one & filter_param_two & filter_param_three).order_by(ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # show result in ascending order with limit WITH date filter
                    errors = ErrorLog.select().where(filter_param_one & filter_param_two & filter_param_three).limit(limit)
            else:
                if desc:
                    # show result in descending order without limit WITH date filter
                    errors = ErrorLog.select().where(filter_param_one & filter_param_two & filter_param_three).order_by(ErrorLog.logged_at.desc())
                else:
                    # show result in ascending order without WITH date filter
                    errors = ErrorLog.select().where(filter_param_one & filter_param_two & filter_param_three)
        return self.__generate_error_return_payload(errors)

    def get_debug_by_origin(self, origin: str = '', first_limit: datetime = None, last_limit: datetime = None):
        """
        # returns all debug data filters by origin; if neededd.
        first_limit: datetime filters out data before this limit
        last_limit: datetime filters out data after this limit
        origin: str point of origin of any debug msg that needs to be on this list.
        """
        if origin is not None or len(origin) != 0:
            origin = origin.strip()
            origin = origin.lower()

        if first_limit is None and last_limit is None:
            debugs = DebugLog.select().where(DebugLog.point_of_origin == origin.lower())
        else:
            first_limit = Utility.unix_time_millis(first_limit)
            if first_limit is not None and last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)

            debugs = DebugLog.select().where((DebugLog.point_of_origin == origin.lower()) & (DebugLog.logged_at >= first_limit) & (DebugLog.logged_at <= last_limit))
        return self.__generate_verbose_return_payload(debugs)

    def get_debug_by_developers(self, developers_name: str = '', first_limit: datetime = None, last_limit: datetime = None):
        """
        # returns all debug data filters by developers; if neededd.
        first_limit: datetime filters out data before this limit
        last_limit: datetime filters out data after this limit
        developers_name: str developers_name : who wrote the debug message. For debugging person. Could be None or empty string.
        """
        if len(developers_name) == 0:
            return self.get_all_debug_log()
        if first_limit is None and last_limit is None:
            debugs = DebugLog.select().where(DebugLog.user == developers_name)
        else:
            first_limit = Utility.unix_time_millis(first_limit)    
            if first_limit is not None and last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)
            debugs = DebugLog.select().where((DebugLog.user == developers_name) & (DebugLog.logged_at >= first_limit) & (DebugLog.logged_at <= last_limit))
        return self.__generate_verbose_return_payload(debugs)

    def mark_resolve(self, error_name: str, origin: str):
        """
        # Mark resolved some errors
        error_name: str the error name u want to mark as resolved.
        origin: str point of origin of this particular error.
        they are both necessary
        """
        result = self.empty_result
        if error_name is None or len(error_name) == 0:
            result['message'] = "missing error name!"
            return result
        if origin is None or len(origin) == 0:
            result['message'] = 'missing error origin!'
            return result
        
        filter_one = (ErrorLog.error_name == error_name)
        filter_two = (ErrorLog.point_of_origin == origin)
        filter_three = (ErrorLog.is_resolved != True)
        query = (ErrorLog.update({ErrorLog.is_resolved: True, ErrorLog.resolved_at: Utility.current_time_in_milli()}).where(filter_one & filter_two & filter_three))
        result = query.execute()
        return result

    @staticmethod
    def delete_old_debug():
        from datetime import timedelta
        limit = (datetime.now() - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        print("Deleting record older than {}".format(limit.strftime('%A, %d %B, %Y')))
        today = Utility.unix_time_millis(limit)
        delete_stuff = DebugLog.delete().where(DebugLog.logged_at < today)
        result = delete_stuff.execute()

        print("Deleted {} debug entries".format(result))
