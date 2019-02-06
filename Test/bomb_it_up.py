from datetime import datetime, timedelta
from Test.run_test import RunTest
from ZathuraProject import Zathura
import unittest
import time
import random

class TestAll(unittest.TestCase):

    def setUp(self):
        zathura = Zathura()
        for i in range(0, 50):
            error_name = "No error - {}".format(i)
            rows = zathura.insert_error_log("test123", error_name, "no description", self.test_insertion_boom_boom.__name__, warning=3)
        for i in range(0, 50):
            error_name = "No error - {}".format(i)
            rows = zathura.insert_error_log("test123", error_name, "no description", self.test_insertion_boom_boom.__name__, warning=3)
        for i in range(0, 50):
            error_name = "No error - {}".format(i)
            rows = zathura.insert_error_log("test123", error_name, "no description", self.test_insertion_boom_boom.__name__, warning=3)

    def tearDown(self):
        RunTest().self_destruct()  # Delete the test db

    def test_insertion_boom_boom(self):
        zathura = Zathura()
        counter = 0
        for i in range(0, 50):
            error_name = "No error - {}".format(i)
            rows = zathura.insert_error_log("test123", error_name, "no description", self.test_insertion_boom_boom.__name__, warning=3)
            counter += rows
        self.assertEqual(counter, 50, "test insertion - inserted 50 data")

    def test_search_by_error_name(self):
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
        self.assertEqual(total, 2, 'Searchc by name, first date limit, last date limit, descending order and limit: Limit did not work.')
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
        pass

    def test_search_in_between_dates(self):
        pass

    def test_mark_resolve(self):
        zathura = Zathura()
        import random
        all_errors = zathura.get_all_error_log()
        total = all_errors['total'] if 'total' in all_errors else -1
        for _ in range(0, total):
            do_or_not_do = int(random.randint(100, 1000)) % 7
            if do_or_not_do == 0:
                # mark it resolved.
                result = zathura.mark_resolve("No error - {}".format(_), 'run_error_test')
                if isinstance(result, int):
                    status = True if result > 0 else False
                else:
                    status = False
                self.assertTrue(status, 'Mark Resolve: came False for {}'.format("No error - {}".format(_)))
        

    def test_all_error(self):
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
        # ----------------------------------------------------------------

        # ----------------------------------------------------------------
        # Test 4
        all_errors = zathura.get_all_error_log(show_all=False)
        # ----------------------------------------------------------------
        

    def test_all_debug(self):
        pass

    def test_debug_by_user(self):
        pass

    def test_debug_by_origin(self):
        pass


if __name__ == '__main__':
    unittest.main()
