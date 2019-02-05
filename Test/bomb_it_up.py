from Test.run_test import RunTest
from ZathuraProject import Zathura
import unittest
import sys


class TestAll(unittest.TestCase):

    def setUp(self):
        test = RunTest()
        test.run_error_test()
        test.run_debug_test()

    # @unittest.skipIf(sys.version_info < (3, 0, 0))
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO', "Checking AssetEqual")

    def test_count_error(self):
        # this will check the insertion as well.
        zathura = Zathura()
        all_errors = zathura.get_all_error_log()
        self.assertGreaterEqual(len(all_errors), 1000, 'Logger DB is not populated')

    def test_search_by_error_name(self):
        pass

    def test_search_by_error_origin(self):
        pass

    def test_search_in_between_dates(self):
        pass

    def test_all_error(self):
        pass

    def test_all_debug(self):
        pass

    def test_debug_by_user(self):
        pass

    def test_debug_by_origin(self):
        pass

    def test_mark_resolve(self):
        pass

    def doCleanups(self):
        import os
        print(os.getcwd())
        RunTest().self_destruct()


if __name__ == '__main__':
    unittest.main()
