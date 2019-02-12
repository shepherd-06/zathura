from time import time
from datetime import datetime


class Utility:

    Tag_User = 'user'
    Tag_Error_Name = 'error_name'
    Tag_Error_Description = 'error_description'
    Tag_Origin = 'point_of_origin'
    Tag_Logged_At = 'logged_at'
    Tag_Logged_At_Unix = 'logged_at_unix'
    Tag_Is_Resolved = 'is_resolved'
    Tag_Resolved_At = 'resolved_at'
    Tag_Resolved_At_Unix = 'resolved_at_unix'
    Tag_Warning_Level = 'warning_level'
    Tag_Message = 'message-data'
    Tag_Total = 'total'
    Tag_Log = 'log'
    Tag_Log_CRITICAL = 5
    Tag_Log_ERROR = 4
    Tag_Log_WARNING = 3
    Tag_Log_INFO = 2
    Tag_Log_DEBUG = 1
    Tag_Log_NotSet = 0
    Tag_error_message = 'message'
    Tag_Text_Resolved = 'Resolved'
    Tag_Text_Not_Resolved = 'Not Resolved'

    @staticmethod
    def get_timeformat():
        """
        time format
        """
        return '%A, %d %B, %Y at %H:%M:%S.%f'

    @staticmethod
    def get_print_timeformat():
        """
        time format
        """
        return '%A, %d %B, %Y at 12 AM'

    # lamda function
    @staticmethod
    def current_time_in_milli():
        return int(round(time() * 1000))

    # unix time to current time in milli converstion
    @staticmethod
    def unix_time_millis(dt: datetime):
        """
        Datetime to milisecond conversion in from UNIX time.
        """
        epoch = datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000.0

    @staticmethod
    def milli_to_datetime(time: int):
        """
        convert milisecond value to datetime instance.
        """
        return datetime.fromtimestamp(time/1000.0).strftime(Utility.get_timeformat())
