import unittest


class MyTestCase(unittest.TestCase):

    def test_something(self):
        from abis_apis.lib import identify
        data = identify("123", "zxs123", ["sasasa", "adadadad"])
        print(data)


if __name__ == '__main__':
    unittest.main()
