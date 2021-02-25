import base64
import errno
import logging
import os

import Crypto
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from config.settings import AppConfig
from logger_utils import initLogger, myPrint

logger = logging.getLogger("server.custom")
certificate_folder_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'config', 'certificates'))

initLogger()


class Encryption:
    conf = AppConfig()

    def __init__(self, key_splitter=None):
        self.public_key = None
        self.private_key = None
        self.key_splitter = key_splitter or '#KEY_SPLITTER#'
        self.read_public_key()
        self.read_private_key()
        self.aes_key = os.urandom(32)
        # self.aes_key = b'\xef"1\x97\xbd\x95a\x87\xcb2\x99V\x13\xdb\x82\xb3\xbd\xdd\xfb:o\xc3D\xfd\xd7G\xea\xdd\xe2
        # \xc6\xbe\x9d'
        self.iv = os.urandom(32)
        # self.iv = Random.new().read(AES.block_size)
        # self.iv = b'\x1d\xc7\xb4\x95\'b\xcd\x12\x0fI\xcf\rG\xc3E\xc0\x13ch`\xe2\xb9\xb7\x9d\xc4\x11.\xc8\x19\xa8\x8b}'

    def encrypt_data_abis_with_specs(self, data: str):
        iv, ciphertext, _xx = self.encrypt_data_aes(data)
        encrypted_aes_key, mod, exp = self.encrypt_data_rsa_bytes(self.aes_key)
        key_splitter_bytes = bytes(self.key_splitter, 'utf-8')
        final_response = b''.join([encrypted_aes_key, key_splitter_bytes, iv, ciphertext])
        myPrint("encrypt iv: " + base64.b64encode(iv).decode('utf-8'))
        myPrint("encrypt ciphertext: " + base64.b64encode(ciphertext).decode('utf-8'))
        myPrint("encrypt aes_key: " + base64.b64encode(self.aes_key).decode('utf-8'))
        myPrint("encrypt encrypted_aes_key: " + base64.b64encode(encrypted_aes_key).decode('utf-8'))
        myPrint("encrypt rsa_public_key: " + self.public_key.decode('utf-8'))
        myPrint("encrypt rsa_mod: " + str(mod))
        myPrint("encrypt rsa_exp: " + str(exp))
        return base64.b64encode(final_response), mod

    def decrypt_data_abis_with_specs(self, data: str, rsa_mod: int = None):
        if rsa_mod is None or rsa_mod == self.getPrivateKeyMod():
            data_bytes = base64.b64decode(data)
            encrypted_aes_key = data_bytes[:256]
            key_splitter_bytes = bytes(self.key_splitter, 'utf-8')
            key_splitter_iv_data = data_bytes[256:]
            iv_data = key_splitter_iv_data.replace(key_splitter_bytes, b'')
            iv_bytes = iv_data[:32]
            encrypted_data = iv_data[32:]

            aes_key = self.decrypt_data_rsa(encrypted_aes_key, rsa_mod)

            data = self.decrypt_data_aes(encrypted_data, aes_key, iv_bytes)
            myPrint("decrypt iv: " + base64.b64encode(iv_bytes).decode('utf-8'))
            myPrint("decrypt ciphertext: " + base64.b64encode(encrypted_data).decode('utf-8'))
            myPrint("decrypt encrypted_aes_key: " + base64.b64encode(encrypted_aes_key).decode('utf-8'))
            myPrint("decrypt aes_key: " + base64.b64encode(aes_key).decode('utf-8'))
            myPrint("decrypt data: " + data)
        else:
            raise RuntimeError("Mod are not matching")
        return

    def encrypt_data_aes(self, data: str):
        # Construct an AES-GCM Cipher object with the given key and a
        ciphertext = AESGCM(self.aes_key).encrypt(self.iv, bytes(data, 'utf-8'), b"")
        return self.iv, ciphertext, ""

    def decrypt_data_aes(self, data: bytes, aes_key: bytes, iv: bytes):
        data = AESGCM(aes_key).decrypt(iv, data, b"")
        return data.decode('utf-8')

    def read_public_key(self):
        key_file_path = os.path.join(certificate_folder_path, self.conf.public_key_file)
        if os.path.exists(key_file_path):
            filename, file_extension = os.path.splitext(key_file_path)
            with open(key_file_path, "rb") as key_file:
                if file_extension == ".pem":
                    self.public_key = RSA.importKey(key_file.read()).exportKey(format='PEM', passphrase=None, pkcs=1)
                elif file_extension == ".pub":
                    self.public_key = RSA.importKey(key_file.read()).exportKey(format='PEM', passphrase=None, pkcs=1)
                else:
                    raise RuntimeError("Public key file extension "+file_extension+" not supported")
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), key_file_path)

    def read_private_key(self):
        key_file_path = os.path.join(certificate_folder_path, "server.key")
        if os.path.exists(key_file_path):
            with open(key_file_path, "rb") as key_file:
                self.private_key = RSA.importKey(key_file.read()).exportKey(format='PEM', passphrase=None, pkcs=1)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), key_file_path)

    def encrypt_data_rsa(self, data: str):
        key = RSA.importKey(self.public_key)
        cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        ciphertext = cipher.encrypt(bytes(data, 'utf-8'))
        return ciphertext, key.n, key.e

    def encrypt_data_rsa_bytes(self, data: bytes):
        key = RSA.importKey(self.public_key)
        cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        ciphertext = cipher.encrypt(data)
        return ciphertext, key.n, key.e

    def decrypt_data_rsa(self, data: bytes, mod: int = None):
        key = RSA.importKey(self.private_key)
        if mod is None or mod == key.n:
            cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
            message = cipher.decrypt(data)
            return message
        else:
            raise RuntimeError("Private key mod: "+str(key.n)+"\nPublic key mod: "+str(mod))

    def getPublicKeyMod(self):
        key = RSA.importKey(self.public_key)
        return key.n

    def getPrivateKeyMod(self):
        key = RSA.importKey(self.private_key)
        return key.n
