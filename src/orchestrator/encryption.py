import base64
import errno
import os

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, padding, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from config.settings import AppConfig

certificate_folder_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'config', 'certificates'))


class Encryption:
    conf = AppConfig()

    def __init__(self, key_splitter=None):
        self.public_key = None
        self.private_key = None
        self.key_splitter = key_splitter or '#KEY_SPLITTER#'
        self.read_public_key()
        self.read_private_key()
        # self.aes_key = os.urandom(32)
        self.aes_key = b'\xef"1\x97\xbd\x95a\x87\xcb2\x99V\x13\xdb\x82\xb3\xbd\xdd\xfb:o\xc3D\xfd\xd7G\xea\xdd\xe2\xc6\xbe\x9d'
        # self.iv = os.urandom(16)
        # self.iv = Random.new().read(AES.block_size)
        self.iv = b'YG\xa8\x17\x83M\xba\x7f\xd3\x80\x95\xe5t\xc1\xc5U'

    def encrypt_data_aes(self, data: str):
        # because AES encryption requires the length of the msg to be a multiple of 16
        # padded_private_msg = data + (self.key_splitter * ((16 - len(data)) % 16))

        # Construct an AES-GCM Cipher object with the given key and a
        ciphertext = AESGCM(self.aes_key).encrypt(self.iv, bytes(data, 'utf-8'), b"")
        return self.iv, ciphertext, ""

    def decrypt_data_aes(self, data: bytes, iv: bytes):
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        pt = cipher.decrypt(data).decode('utf-8')
        return pt.rstrip(self.key_splitter)

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
        key_file_path = os.path.join(certificate_folder_path, "id_rsa")
        if os.path.exists(key_file_path):
            with open(key_file_path, "rb") as key_file:
                self.private_key = RSA.importKey(key_file.read()).exportKey(format='PEM', passphrase=None, pkcs=1)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), key_file_path)

    def encrypt_data_rsa(self, data: str):
        key = RSA.importKey(self.public_key)
        cipher = PKCS1_OAEP.new(key)
        ciphertext = cipher.encrypt(bytes(data, 'utf-8'))
        return ciphertext

    def decrypt_data_rsa(self, data: bytes):
        key = RSA.importKey(self.private_key)
        cipher = PKCS1_OAEP.new(key)
        message = cipher.decrypt(data)
        return message

    def encrypt_symmetric_asymmetric(self, data):
        encrypted = self.encrypt_data_aes(data)
