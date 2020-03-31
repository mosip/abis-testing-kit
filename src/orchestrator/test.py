import unittest


class MyTestCase(unittest.TestCase):

    def test_parser(self):
        from typing import List, Dict
        import errno
        import json
        import os
        from orchestrator import parse_test_cases, save_file
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

    def test_consume(self):
        from orchestrator import consume
        status, body = consume()
        print("status: " + str(status))
        print("body: " + str(body))


if __name__ == '__main__':
    unittest.main()
