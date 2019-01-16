class MessengerLogger:

    def __init__(self, mongo_con, timezone = None):
        self.mongo_con = mongo_con
        if timezone is not None:
            self.bd_timezone = timezone
        else:
            self.bd_timezone = None
        self.STRF_TIMEFORMAT = '%A %d %B %Y - %I:%M:%S %p'

    def messenger_logger(self):
        print("Work in progress!")
