import json
import logging
import os
from datetime import datetime
from pytz import timezone
from logging.handlers import TimedRotatingFileHandler

class FileLog:
    def __init__(self):
        self.logger_message = logging.getLogger('logger_message_log')
        self.logger_error_log = logging.getLogger('logger_error_log')

    def error_logging(self, user_id: str, error_payload: dict):
        """
        sets up error logging in file
        :param user_id: any sort of identifier
        :param error_payload: error payload dictionary
        :return: None
        """
        try:
            if not self.logger_error_log.handlers:
                log_path = os.path.join('logs', 'Error', user_id)
                if not os.path.exists(log_path):
                    os.makedirs(log_path)
                log_handler = TimedRotatingFileHandler(
                    filename=os.path.join(log_path, '{}.log'
                                          .format(user_id + "_"
                                                  + datetime.now().strftime('%A_%d_%B_%Y'))),
                    when='midnight',
                    backupCount=7
                )
                self.logger_error_log.addHandler(log_handler)
                self.logger_error_log.setLevel(logging.CRITICAL)
            self.logger_error_log.critical(json.dumps(error_payload))
            self.logger_error_log.critical('\n\n')
        finally:
            return

    def message_log_data(self, user_id: str, message: dict):
        """
        set logging gets activated here
        :param user_id:
        :param message:
        :return: None
        """
        try:
            if not self.logger_message.handlers:
                log_path = os.path.join('logs', 'Message_log', user_id)
                if not os.path.exists(log_path):
                    os.makedirs(log_path)
                log_handler = TimedRotatingFileHandler(
                    filename=os.path.join(log_path, '{}.log'
                                          .format(user_id + "_"
                                                  + datetime.now().strftime('%A_%d_%B_%Y'))),
                    when='midnight',
                    backupCount=7
                )
                self.logger_message.addHandler(log_handler)
                self.logger_message.setLevel(logging.DEBUG)
            error_payload = dict()
            error_payload['user_id'] = user_id
            error_payload['logged_at'] = self.bd_timezone.localize(datetime.now()).strftime('%A %d %B %Y - %I:%M:%S %p')
            error_payload['message_data'] = message
            self.logger_message.debug(json.dumps(error_payload))
            self.logger_message.debug('\n\n')
        except Exception as error:
            self.error_logging(user_id, {
                "message": "error logging the log data",
                "error:": str(error)}, self.message_log_data.__name__)
        finally:
            return