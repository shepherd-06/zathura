from Test.run_test import RunTest
import unittest

class TestAll(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    test = RunTest()
    test.run_error_test()
    test.run_debug_test()
    unittest.main()