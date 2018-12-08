from datetime import datetime
from .utility import Utility

class ErrorLogger:
    def __init__(self, mongo_con, collection_name, timezone = None):
        self.mongo_con = mongo_con
        self.collection_name = collection_name
        if timezone is not None:
            self.bd_timezone = timezone
        else:
            self.bd_timezone = None
        self.STRF_TIMEFORMAT = '%A %d %B %Y - %I:%M:%S %p'

    def error_logging(self, user_id: str, message: str, 
        point_of_origin: str = None, error_code: int = 400):
        """
        sets up error logging in mongo
        :param user_id: current facebook user id of the user
        :param message: message to write on the error dump log
        :param point_of_origin: point of origin of the error
        :return: None
        """
        try:
            error_payload = dict()
            error_payload['user_id'] = user_id
            if self.bd_timezone is not None:
                error_payload['logged_at'] = self.bd_timezone.localize(datetime.now()).strftime(self.STRF_TIMEFORMAT)
            else:
                error_payload['logged_at'] = datetime.now().strftime(self.STRF_TIMEFORMAT)
            error_payload['point_of_origin'] = point_of_origin
            error_payload['error_message'] = message
            error_payload['error_code'] = error_code  # 400 is default

            status = Utility.mongo_insert(self.mongo_con[self.collection_name], error_payload)
            if not status:
                # TODO: add filebased logging here!
                print("Error occurred logging error!")
        finally:
            return