import random
import time
import unittest
from datetime import datetime, timedelta

from Test.test_run import RunTest
from ZathuraProject import Zathura


class TestBugtracker(unittest.TestCase):
    
    """
    for future testing
    make sure functions return the HTTP STATUS CODE. so not 200, will be considered False.
    """

    @classmethod
    def setUpClass(cls):
        """
        This function will input random data inside sqlit3 database
        There will 150 entries each time this function is called.
        """
        RunTest().self_destruct()  # Just in case
        zathura = Zathura(bugtracker_url="http://127.0.0.1:8000/",
                          project_token="835c0f58-8567-463a-9d36-a6af11bfdc87")
        
        for i in range(0, 2):
            error_name = "Test Error - {}".format(i)
            zathura.insert_error_log(
                "test123", error_name, "no description", warning=3)

    def test_error_insertion_for_bugtracker(self):
        """
        Test insertion for Bugtracker
        Setup is done entirely by itself.
        """
        zathura = Zathura(bugtracker_url="http://127.0.0.1:8000/",
                          project_token="835c0f58-8567-463a-9d36-a6af11bfdc87")
        counter = 0
        for i in range(0, 2):
            error_name = "Second Test error - {}".format(i)
            state = zathura.send_error_log_bugtracker(
                error_name,
                "no description")
            counter = counter + 1 if state else counter + 0
        self.assertEqual(counter, 2, "test insertion - inserted 5 data")
        
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
        zathura = Zathura(bugtracker_url="http://127.0.0.1:8000/",
                          project_token="835c0f58-8567-463a-9d36-a6af11bfdc87")
        counter = 0

        for i in range(0, 2):
            state = zathura.send_verbose_log_bugtracker(
                "Multiprocessing Test: {}".format(i))
            counter = counter + 1 if state else counter + 0
        self.assertEqual(
            counter, 2, "test verbose insertion - inserted 5 data")
        
        counter = 0
        for i in range(0, 2):
            state = zathura.send_verbose_log_bugtracker(
                "Multiprocessing Test: {}".format(i), "Test")
            counter = counter + 1 if state else counter + 0
        self.assertEqual(
            counter, 2, "Second verbose test")

    @classmethod
    def tearDownClass(cls):
        RunTest().self_destruct()


if __name__ == '__main__':
    unittest.main()
