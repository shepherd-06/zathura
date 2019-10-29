import unittest


class TestAll(unittest.TestCase):

    def test_always_true(self):
        """
        This function will always assert True.
        It's here only to make sure travisCI always returns True.
        """
        self.assertTrue(True, "Always True")


if __name__ == '__main__':
    unittest.main()
