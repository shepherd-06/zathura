import sys
from datetime import datetime
from .utility import Utility
from .mongo_connection import main_con
from .error_logger import ErrorLogger

def create_app():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            print("Hello World - {}".format(create_app.__name__))
            print("Test running at {}".format(datetime.now().strftime(Utility.get_timeformat())))
            local_test_db = main_con()
            local_test_db = local_test_db['E-Logger_Test']
            error_logger = ErrorLogger(local_test_db, 'ErrorLog')
            for i in range(0, 10):
                print("Woring - {} || user_id - {}".format(i,'123456'))
                error_logger.error_logging(user_id = '123456',
                message = 'Hello World', point_of_origin = create_app.__name__, 
                error_code = 400, file_dump=True)
        else:
            print("unknown command")