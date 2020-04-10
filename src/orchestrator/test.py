import unittest


class MyTestCase(unittest.TestCase):

    # noinspection PyMethodMayBeStatic
    def test_parser(self):
        from typing import List, Dict
        import errno
        import json
        import os
        from orchestrator.orchestrator_methods import parse_test_cases, save_file
        result_abs_path = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), './', 'temp_data'))
        store_abs_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'store'))
        test_case_file_path = os.path.join(store_abs_path, 'test_cases.json')
        test_data_file_path = os.path.join(store_abs_path, 'test_data.json')
        parsed_test_case_file_path = os.path.join(result_abs_path, 'parsed_test_cases.json')

        if not os.path.isfile(test_case_file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), test_case_file_path)
        if not os.path.isfile(test_data_file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), test_data_file_path)

        with open(test_case_file_path, 'r') as file:
            test_cases: List = json.loads(file.read())

        with open(test_data_file_path, 'r') as file:
            test_data: Dict = json.loads(file.read())

        ptcs: List = parse_test_cases(test_cases)
        save_file(parsed_test_case_file_path, ptcs)

    # noinspection PyMethodMayBeStatic
    def test_consume(self):
        from orchestrator.queue_methods import consume
        status, body = consume()
        print("status: " + str(status))
        print("body: " + str(body))

    # noinspection PyMethodMayBeStatic
    def test_request_creator(self):
        from orchestrator.request_creator import create_identify_request
        data = create_identify_request("123", "zxs123", "adada", ["sasasa", "adadadad"])
        print(data)

    # noinspection PyMethodMayBeStatic
    def test_schema_validator_insert(self):
        from orchestrator.schema_validator import validate_insert_response
        ins = {
            "id": "mosip.abis.insert",
            "requestId": "www",
            "timestamp": "3242424",
            "returnValue": 2
        }
        data = validate_insert_response(ins)
        print(data)


if __name__ == '__main__':
    unittest.main()
