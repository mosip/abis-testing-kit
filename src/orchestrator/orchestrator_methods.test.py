import json
import os
import unittest

abs_tmp_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../../', 'tmp'))


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.response_path = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'store'))

    # noinspection PyMethodMayBeStatic
    def test_validate_test_case(self):
        from orchestrator.orchestrator_methods import validate_test_cases
        with open(os.path.join(self.response_path, 'test_cases.json'), 'r') as file:
            response = json.loads(file.read())
            status = validate_test_cases(response)
            self.assertTrue(status)

    # noinspection PyMethodMayBeStatic
    def test_parse_test_cases(self):
        from orchestrator.orchestrator_methods import parse_test_cases
        with open(os.path.join(self.response_path, 'test_cases.json'), 'r') as file:
            response = json.loads(file.read())
            tcs = parse_test_cases(response)
            print(json.dumps(tcs))

    # noinspection PyMethodMayBeStatic
    def test_validate_test_data(self):
        from orchestrator.orchestrator_methods import validate_test_data
        with open(os.path.join(self.response_path, 'persona_data.json'), 'r') as file:
            response = json.loads(file.read())
            status = validate_test_data(response)
            self.assertTrue(status)

    # noinspection PyMethodMayBeStatic
    def test_extract_testdata(self):
        from orchestrator.orchestrator_methods import extract_testdata
        extract_testdata(os.path.join(abs_tmp_path, 'testdata.zip'))

    # noinspection PyMethodMayBeStatic
    def test_parse_step(self):
        from orchestrator.orchestrator_methods import parse_step
        step = 'insert(person1, person2).assert(returnValue, 1)'
        parsed_step = parse_step(step)
        print(parsed_step)


if __name__ == '__main__':
    unittest.main()
