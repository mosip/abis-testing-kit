import unittest
import os
import json


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.response_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'config/responses'))

    # noinspection PyMethodMayBeStatic
    def test_schema_validator_insert(self):
        from orchestrator.schema_validator import validate_insert_response
        with open(os.path.join(self.response_path, 'insert.json'), 'r') as file:
            response = json.loads(file.read())
            status, msg = validate_insert_response(response)
            print(msg)
            self.assertTrue(status)

    # noinspection PyMethodMayBeStatic
    def test_schema_validator_identify(self):
        from orchestrator.schema_validator import validate_identify_response
        with open(os.path.join(self.response_path, 'identify.json'), 'r') as file:
            response = json.loads(file.read())
            status, msg = validate_identify_response(response)
            print(msg)
            self.assertTrue(status)

    # noinspection PyMethodMayBeStatic
    def test_schema_validator_delete(self):
        from orchestrator.schema_validator import validate_delete_response
        with open(os.path.join(self.response_path, 'delete.json'), 'r') as file:
            response = json.loads(file.read())
            status, msg = validate_delete_response(response)
            print(msg)
            self.assertTrue(status)

    # noinspection PyMethodMayBeStatic
    def test_schema_validator_ping(self):
        from orchestrator.schema_validator import validate_ping_response
        with open(os.path.join(self.response_path, 'ping.json'), 'r') as file:
            response = json.loads(file.read())
            status, msg = validate_ping_response(response)
            print(msg)
            self.assertTrue(status)

    # noinspection PyMethodMayBeStatic
    def test_schema_validator_reference_count(self):
        from orchestrator.schema_validator import validate_reference_count_response
        with open(os.path.join(self.response_path, 'reference_count.json'), 'r') as file:
            response = json.loads(file.read())
            status, msg = validate_reference_count_response(response)
            print(msg)
            self.assertTrue(status)


if __name__ == '__main__':
    unittest.main()
