import base64
import pprint
import unittest
from orchestrator.decryption import Decryption
from orchestrator.encryption import Encryption


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

    def test_aes_encrypt_decrypt(self):
        data = 'test12131'
        e = Encryption()
        print(data)
        iv, ciphertext, tag = e.encrypt_data_aes(data)
        print("iv: " + pprint.pformat(iv))
        print("Encrypted: "+pprint.pformat(ciphertext))
        print("tag: " + pprint.pformat(tag))
        print("B64 key: " + pprint.pformat(base64.urlsafe_b64encode(e.aes_key).decode('utf-8')))
        print("B64 iv: " + pprint.pformat(base64.urlsafe_b64encode(iv).decode('utf-8')))
        print("B64 data: " + pprint.pformat(base64.urlsafe_b64encode(ciphertext).decode('utf-8')))

    def test_read_public_key(self):
        data = 'test12131'
        e = Encryption()
        print(e.public_key)

    def test_rsa_encrypt(self):
        data = 'test12131'
        e = Encryption()
        print(data)
        encrypted, mod, expo = e.encrypt_data_rsa(data)
        print("Encrypted: "+pprint.pformat(encrypted))
        print("B64 key: " + pprint.pformat(e.public_key.decode('utf-8')))
        print("B64 data: " + pprint.pformat(base64.b64encode(encrypted).decode('utf-8')))
        print("Mod: " + pprint.pformat(mod))
        print("Exp: " + pprint.pformat(expo))
        decrypted = e.decrypt_data_rsa(encrypted, mod)
        print("Decrypted: " + pprint.pformat(decrypted))
        print("B64 private key: " + pprint.pformat(e.private_key.decode('utf-8')))
        print("B64 data: " + pprint.pformat(decrypted.decode('utf-8')))

    def test_rsa_decrypt(self):
        data = 'Bgwz/Cn4xPz20Bf0eeecJN9vLuuY4CsdRGyTB6RyYiLBDe3+actUdjarOcICb0xqxfJmV0ExqZlSgkBerHy1V8cK1JdpVN9hp9cLhBcKzvwiAMBwE1ENLA3masSHGN63xWDAlRaKFspb5Rre3bVFsC84VnUJjMt5nJdH17QyJG7GXarxsDE9uSvfUHktnPJ71OAeOwIjNIuGwvCPLMy61VpvlxEbyGECGSuFadghDNjSu4xBYwlp4ExpMxx1Qm7mntvPkimX5cyH6G6Jv/UtXj7IsmZiqvjFJC5wW+/8NQPg24kCvdohmLKEdzmBfj0TnA9nRyCELLbPU09E+cr6dA=='
        e = Encryption()
        print(data)
        decrypted = e.decrypt_data_rsa(base64.b64decode(data))
        print("Decrypted: " + pprint.pformat(decrypted))
        print("B64 private key: " + pprint.pformat(e.private_key.decode('utf-8')))
        print("B64 data: " + pprint.pformat(decrypted.decode('utf-8')))

    def test_encrypt_data_abis_with_specs(self):
        data = 'test12131'
        e = Encryption()
        data, mod = e.encrypt_data_abis_with_0_9_specs(data)
        d = Decryption()
        d.decrypt_data_abis_with_0_9_specs(data, mod)

    def test_match_mods(self):
        e = Encryption()
        pub_mod = e.getPublicKeyMod()
        pri_mod = e.getPrivateKeyMod()
        if pub_mod == pri_mod:
            print("Mod are matching")
        else:
            print("Mod does not matching")


if __name__ == '__main__':
    unittest.main()
