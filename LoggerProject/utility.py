from time import time
from datetime import datetime
class Utility:
    @staticmethod
    def get_timeformat():
        return '%A %d %B %Y - %I:%M:%S %p'
    
    # lamda function
    current_time_in_milli = lambda: int(round(time() * 1000))

    # unix time to current time in milli converstion
    @staticmethod
    def unix_time_millis(dt: datetime):
        epoch = datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000.0