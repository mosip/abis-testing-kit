import json
import os
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.response_path = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'store'))

    # noinspection PyMethodMayBeStatic
    def test_validate_test_case(self):
        from orchestrator.orchestrator_methods import validate_test_cases
        with open(os.path.join(self.response_path, 'test_cases.json'), 'r') as file:
            response = json.loads(file.read())
            status, msg = validate_test_cases(response)
            print(msg)
            self.assertTrue(status)

    # noinspection PyMethodMayBeStatic
    def test_validate_test_data(self):
        from orchestrator.orchestrator_methods import validate_test_data
        with open(os.path.join(self.response_path, 'test_data.json'), 'r') as file:
            response = json.loads(file.read())
            status, msg = validate_test_data(response)
            print(msg)
            self.assertTrue(status)


if __name__ == '__main__':
    unittest.main()
