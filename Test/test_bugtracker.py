import random
import time
import unittest
from datetime import datetime, timedelta

from decouple import config

from ZathuraProject import Zathura


class TestBugtracker(unittest.TestCase):

    """
    for future testing
    make sure functions return the HTTP STATUS CODE. so not 200, will be considered False.
    """

    def test_error_insertion_for_bugtracker(self):
        """
        Test insertion for Bugtracker
        Setup is done entirely by itself.
        """
        zathura = Zathura(bugtracker_url=config("bugtracker_local_url", ""),
                          project_token=config("bugtracker_project_api", ""))
        counter = 0
        for i in range(0, 2):
            error_name = "Second Test error - {}".format(i)
            state = zathura.send_error_log_bugtracker(
                error_name,
                "no description")
            counter = counter + 1 if state else counter + 0
        self.assertEqual(counter, 2, "test insertion - inserted 2 data")

        counter = 0
        for i in range(0, 2):
            error_name = "Third Test error - {}".format(i)
            state = zathura.send_error_log_bugtracker(
                error_name,
                "no description",
                "Test")
            counter = counter + 1 if state else counter + 0
        self.assertEqual(counter, 2, "Third test")

    def test_verbose_insertion_for_bugtracker(self):
        """
        Test debug data insertion for bugtracker
        """
        zathura = Zathura(bugtracker_url=config("bugtracker_local_url", ""),
                          project_token=config("bugtracker_project_api", ""))
        counter = 0

        for i in range(0, 2):
            state = zathura.send_verbose_log_bugtracker(
                "Multiprocessing Test: {}".format(i))
            counter = counter + 1 if state else counter + 0
        self.assertEqual(
            counter, 2, "test verbose insertion - inserted 2 data")

        counter = 0
        for i in range(0, 2):
            state = zathura.send_verbose_log_bugtracker(
                "Multiprocessing Test: {}".format(i), "Test")
            counter = counter + 1 if state else counter + 0
        self.assertEqual(
            counter, 2, "Second verbose test")


if __name__ == '__main__':
    unittest.main()
