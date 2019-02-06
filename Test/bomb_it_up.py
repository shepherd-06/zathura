from datetime import datetime, timedelta
from Test.run_test import RunTest
from ZathuraProject import Zathura
import unittest
import time
import random

class TestAll(unittest.TestCase):

    def database_setup(self):
        """
        This function will input random data inside sqlit3 database
        There will 150 entries each time this function is called.
        """
        zathura = Zathura()
        counter = 0
        for i in range(0, 50):
            error_name = "No error - {}".format(i)
            rows = zathura.insert_error_log("test123", error_name, "no description", warning=3)
            counter += rows
        for i in range(0, 50):
            error_name = "No error - {}".format(i)
            rows = zathura.insert_error_log("test123", error_name, "no description", warning=3)
            counter += rows
        for i in range(0, 50):
            error_name = "No error - {}".format(i)
            rows = zathura.insert_error_log("test123", error_name, "no description", warning=3)
            counter += rows

    def database_teardown(self):
        """
        This function will remove the database file.
        """
        RunTest().self_destruct()  # Delete the test db


    def test_insertion(self):
        """
        Test insertion inside the database.
        Setup is done entirely by itself.
        TODO: this function needs some extensive testing
        """
        zathura = Zathura()
        counter = 0
        for i in range(0, 50):
            error_name = "No error - {}".format(i)
            rows = zathura.insert_error_log("test123", error_name, "no description", warning=3)
            counter += rows
        self.assertEqual(counter, 50, "test insertion - inserted 50 data")


    def test_search_by_error_name(self):
        """
        Test search by error name. 
        Every error log inserted into sqlite got an error name, either the exception name or 
        any other the user (developer) intends to give. 
        This function will test that.
        TODO: These test cases were written on a rush. Must do a new check.
        """
        self.database_teardown()
        self.database_setup()
        zathura = Zathura()
        # ----------------------------------------------------------------------
        random_error_name = "No error - {}".format(random.randint(0, 50))
        errors = zathura.get_error_by_error_name(random_error_name)
        _logs = errors['log']
        # Test one - matching error name.
        for log in _logs:
            self.assertEqual( log['error_name'], random_error_name.lower(), 'Search by error name [no filter] - search parameter and request field did not match!')
        # ----------------------------------------------------------------------
        
        # ----------------------------------------------------------------------
        random_error_name = "No error - {}".format(random.randint(0, 50))
        _datetime_limit = datetime.now() - timedelta(days=1)
        errors = zathura.get_error_by_error_name(random_error_name, first_limit=_datetime_limit, desc= True)
        _logs = errors['log'] if 'log' in errors else list()
        _error_name = errors['log'][0]['error_name']  # TODO: make it dynamic later may be.
        _logged_at_index_zero = datetime.fromtimestamp(int(_logs[0]['logged_at_unix']) / 1000)
        
        # Test Two - first datelimit and descending
        for log in _logs:
            _logged_at = datetime.fromtimestamp(int(log['logged_at_unix']) / 1000)
            self.assertGreaterEqual(_logged_at_index_zero, _logged_at, 'Search by error name, first datelimit and descending order - descending order not working')
            _logged_at_index_zero = _logged_at
        # -----------------------------------------------------------------------
        
        # ----------------------------------------------------------------------
        # Test Three - first datelimit and ascending
        random_error_name = "No error - {}".format(random.randint(0, 50))
        _datetime_limit = datetime.now() - timedelta(days=1)
        errors = zathura.get_error_by_error_name(random_error_name, first_limit=_datetime_limit)
        _logs = errors['log'] if 'log' in errors else list()
        _logged_at_index_zero = datetime.fromtimestamp(int(_logs[0]['logged_at_unix']) / 1000)
        
        # Test Three - first datelimit and ascending
        for log in _logs:
            _logged_at = datetime.fromtimestamp(int(log['logged_at_unix']) / 1000)
            self.assertLessEqual(_logged_at_index_zero, _logged_at, 'Search by error name and first date limit - ascending order not working')
            _logged_at_index_zero = _logged_at
        # ----------------------------------------------------------------------
        
        # ----------------------------------------------------------------------
        # Test Four - first date, last datelimit and descending
        random_error_name = "No error - {}".format(random.randint(0, 50))
        _datetime_limit = datetime.now() - timedelta(days=1)
        _last_date = datetime.now() + timedelta(days=1)
        errors = zathura.get_error_by_error_name(random_error_name, first_limit=_datetime_limit, last_limit=_last_date, desc=True)
        _logs = errors['log'] if 'log' in errors else list()
        _logged_at_index_zero = datetime.fromtimestamp(int(_logs[0]['logged_at_unix']) / 1000)
        
        # Test Three - first datelimit and ascending
        for log in _logs:
            _logged_at = datetime.fromtimestamp(int(log['logged_at_unix']) / 1000)
            self.assertGreaterEqual(_logged_at_index_zero, _logged_at, 'Search by error name, first date, last date limit - descending order not working')
            _logged_at_index_zero = _logged_at
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # Test Five - First datetime, last datelimit and ascending
        random_error_name = "No error - {}".format(random.randint(0, 50))
        _datetime_limit = datetime.now() - timedelta(days=1)
        _last_date = datetime.now() + timedelta(days=1)
        errors = zathura.get_error_by_error_name(random_error_name, first_limit=_datetime_limit, last_limit=_last_date, desc=False)
        _logs = errors['log'] if 'log' in errors else list()
        _logged_at_index_zero = datetime.fromtimestamp(int(_logs[0]['logged_at_unix']) / 1000)
        
        # Test Three - first datelimit and ascending
        for log in _logs:
            _logged_at = datetime.fromtimestamp(int(log['logged_at_unix']) / 1000)
            self.assertGreaterEqual(_logged_at_index_zero, _logged_at, 'Search by error name, first date, last date limit - ascending order not working')
            _logged_at_index_zero = _logged_at
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # Test Six - First datetime, last datelimit, descending, limit
        random_error_name = "No error - {}".format(random.randint(0, 50))
        _datetime_limit = datetime.now() - timedelta(days=1)
        _last_date = datetime.now() + timedelta(days=1)
        errors = zathura.get_error_by_error_name(random_error_name, first_limit=_datetime_limit, last_limit=_last_date, desc=True, limit=2)
        _logs = errors['log'] if 'log' in errors else list()
        _logged_at_index_zero = datetime.fromtimestamp(int(_logs[0]['logged_at_unix']) / 1000)
        total = errors['total'] if 'total' in errors else -1
        self.assertEqual(total, 2, 'Search by name, first date limit, last date limit, descending order and limit: Limit did not work.')
        # Test Three - first datelimit and ascending
        for log in _logs:
            _logged_at = datetime.fromtimestamp(int(log['logged_at_unix']) / 1000)
            self.assertGreaterEqual(_logged_at_index_zero, _logged_at, 'Searchc by name, first date limit, last date limit, descending order: order did not work')
            _logged_at_index_zero = _logged_at
        # ----------------------------------------------------------------------

        # Test Seven - Mandatory failed with out of scope error name
        random_error_name = 'osijsgg'
        errors = zathura.get_error_by_error_name(random_error_name)
        total = errors['total'] if 'total' in errors else -1
        self.assertEqual(total, 0, 'Random error name came out wrong or something. This must come out False')


    def test_search_by_error_origin(self):
        """
        Test search by origin
        Every error registers on the sqlite3 database, will register 
        the point of origin (caller function). 
        It will check if that function works properly
        """
        self.database_teardown()
        self.database_setup()
        zathura = Zathura()
        origin = self.test_search_by_error_origin.__name__
        
        # ---------------------------------------------------------
        # Test 1 - Plain search by origin name
        errors = zathura.get_error_by_origin(origin)
        logs = errors['log'] if 'log' in errors else list()
        total = errors['total'] if 'total' in errors else -1
        self.assertNotEqual(len(logs), 0, 'logs are empty! It cant be!')
        self.assertEqual(len(logs), total, 'log length and total value not matching matching')
        self.assertLessEqual(total, 1, "there is noooo value inside logs or db")
        for log in logs:
            log_origin = log['point_of_origin']
            self.assertEquals(log_origin, origin, 'origin did not match! WOT WOT @.o')
        print("------------------")
        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # Test 2 - Origin name + first date limit
        first_date = datetime.now() - timedelta(days=random.randint(1, 30))
        errors = zathura.get_error_by_origin(origin, first_limit=first_date)
        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # Test 3 - origin name + first date limit, limit
        first_date = datetime.now() - timedelta(days=random.randint(1, 30))
        limit = random.randint(1, 149)
        errors = zathura.get_error_by_origin(origin, first_limit= first_date, limit= limit, desc= True)
        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # Test 4 - origin name + first date limit, limit, descending
        first_date = datetime.now() - timedelta(days=random.randint(1, 30))
        limit = random.randint(1, 149)
        errors = zathura.get_error_by_origin(origin, first_limit= first_date, limit= limit, desc= True)
        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # Test 5 - origin name + first date, last date
        first_date = datetime.now() - timedelta(days=random.randint(1, 30))
        last_date = datetime.now() + timedelta(days=random.randint(0, 30))
        errors = zathura.get_error_by_origin(origin, first_limit= first_date, last_limit=last_date)
        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # Test 6 - origin name + first date, last date, limit, descending
        first_date = datetime.now() - timedelta(days=random.randint(1, 30))
        last_date = datetime.now() + timedelta(days=random.randint(0, 30))
        limit = random.randint(1, 149)
        errors = zathura.get_error_by_origin(origin, first_limit= first_date, last_limit=last_date, limit=limit, desc=True)
        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # Test 7 - search by wrong origin name
        errors = zathura.get_error_by_origin("kljisksknnkshs")
        # ---------------------------------------------------------


    def test_search_in_between_dates(self):
        pass

    def test_mark_resolve(self):
        """
        """
        self.database_teardown()
        self.database_setup()
        zathura = Zathura()
        import random
        all_errors = zathura.get_all_error_log()
        total = all_errors['total'] if 'total' in all_errors else 0
        self.assertNotEqual(total, 0, 'There is not enough value in test database!')
        for _ in range(0, 50):
            do_or_not_do = int(random.randint(100, 1000)) % 7
            if do_or_not_do == 0:
                # mark it resolved.
                result = zathura.mark_resolve("No error - {}".format(_), 'database_setup')
                if isinstance(result, int):
                    status = True if result > 0 else False
                else:
                    status = False
                self.assertTrue(status, 'Mark Resolve: came False for {}'.format("No error - {}".format(_)))
        

    def test_all_error(self):
        """
        Tests search all error against no filter or is_resolved filter on
        This function is moderately stable right now
        """
        # Total 4 major test
        zathura = Zathura()
        # ----------------------------------------------------------------
        # Test 1
        all_errors = zathura.get_all_error_log(show_all=True)
        total = all_errors['total'] if 'total' in all_errors else -1
        self.assertEqual(total, 150, 'Test all error - Not all value were including in sending all data')
        # ----------------------------------------------------------------

        # ----------------------------------------------------------------
        # Test 2
        all_errors = zathura.get_all_error_log(show_all=False, desc=True)
        total = all_errors['total'] if 'total' in all_errors else -1
        self.assertNotEqual(total, -1, 'Test all error - Total is not -1')
        self.assertLessEqual(total, 150, 'Test all error - Total is less than or equal to 150 now')
        logs = all_errors['log'] if 'log' in all_errors else list()
        self.assertEqual(len(logs), total, 'Test all error - log entry is not equal to total value')
        first_logged_at = logs[0]['logged_at_unix']
        for log in logs: 
            logged_at = log['logged_at_unix']
            error_name = log['error_name']
            self.assertGreaterEqual(first_logged_at, logged_at, 'Test all error - descending is not working right for {}'.format(error_name))
            first_logged_at = logged_at
        # ----------------------------------------------------------------

        # ----------------------------------------------------------------
        # Test 3
        all_errors = zathura.get_all_error_log(show_all=True, desc= True)
        total = all_errors['total'] if 'total' in all_errors else -1
        self.assertNotEqual(total, -1, 'Test all error - Total is not -1')
        self.assertLessEqual(total, 150, 'Test all error - Total is less than or equal to 150 now')
        logs = all_errors['log'] if 'log' in all_errors else list()
        self.assertEqual(len(logs), total, 'Test all error - log entry is not equal to total value')
        first_logged_at = logs[0]['logged_at_unix']
        for log in logs: 
            logged_at = log['logged_at_unix']
            error_name = log['error_name']
            self.assertGreaterEqual(first_logged_at, logged_at, 'Test all error - descending is not working right for {}'.format(error_name))
            first_logged_at = logged_at
            resolved_at = log['resolved_at']
            if resolved_at is not None:
                self.assertTrue(log['is_resolved'], "Resolved is not True")
        # ----------------------------------------------------------------

        # ----------------------------------------------------------------
        # Test 4
        all_errors = zathura.get_all_error_log(show_all=False)
        total = all_errors['total'] if 'total' in all_errors else -1
        self.assertNotEqual(total, -1, 'Test all error - Total is not -1')
        self.assertLessEqual(total, 150, 'Test all error - Total is less than or equal to 150 now')
        logs = all_errors['log'] if 'log' in all_errors else list()
        self.assertEqual(len(logs), total, 'Test all error - log entry is not equal to total value')
        first_logged_at = logs[0]['logged_at_unix']
        for log in logs: 
            resolved_at = log['resolved_at']
            self.assertIsNone(resolved_at, "Is resolved should be None here!")
        # ----------------------------------------------------------------
        
        

    def test_all_debug(self):
        pass

    def test_debug_by_user(self):
        pass

    def test_debug_by_origin(self):
        pass


if __name__ == '__main__':
    unittest.main()
