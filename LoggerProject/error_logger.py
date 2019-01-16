from datetime import datetime
from .utility import Utility
from .FileLogger.file_logger import LogDump
from pytz import timezone
from uuid import uuid4
from datetime import datetime

class LoggerP:

    def __init__(self):
        pass

    def log_error(self, user: str, error_name: str, error_description: str, point_of_origin: str= None, ):
        """
        records all error in this database. These errors will never be purged, only modification is if the error is resolved or not.
        user: for whom this error occurred. could be anything
        error_name: short error name, could be str(err) for error that has been caught
        error_description: long error description with much more details
        point_of_origin: in which function this error occurred. To be more precise. for example: function.__name__ using the magic function.

        """
        _id = str(uuid4())[0:10]  # just for future retreiving and uniqueness
        _occurred_at_unix = datetime.utcnow()
        _occurred_at = datetime.now().strftime(Utility.get_timeformat())
        _resolved = False
        _resolved_at = None
        _resolved_at_unix = None
        pass

    def log_debug(self, user: str, debug_text: str, point_of_origin: str= None):
        """
        records debug message data in sqlite for a week long. This is to reduce the size of the sqlite database.
        user: for whom this error occurred. could be anything
        debug_text: debug text we are recording. 
        point_of_origin: from which function or class are u recording this. Use the magic function, __name__ for ease.

        """
        _id = str(uuid4())[0:10]  # just for future retreiving and uniqueness
        _added_at = datetime.now().strftime(Utility.get_timeformat())
        _added_at_unix = datetime.utcnow()
        pass
