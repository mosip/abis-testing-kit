import base64
import errno
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from config.settings import AppConfig

certificate_folder_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), './../', 'config', 'certificates'))


class Encryption:
    conf = AppConfig()

    def __init__(self, key_splitter=None):
        self.public_key = None
        self.key_splitter = key_splitter or '#KEY_SPLITTER#'
        self.read_public_key()
        self.aes_key = os.urandom(32)
        self.iv = os.urandom(32)
        self.private_key = None
        print(self.aes_key)

    def encrypt_data_aes(self, data: str):
        # because AES encryption requires the length of the msg to be a multiple of 16
        padded_private_msg = data + (self.key_splitter * ((16 - len(data)) % 16))

        # Construct an AES-GCM Cipher object with the given key and a
        # randomly generated IV.
        encryptor = Cipher(
            algorithms.AES(self.aes_key),
            modes.GCM(self.iv),
        ).encryptor()

        # associated_data will be authenticated but not encrypted,
        # it must also be passed in on decryption.
        encryptor.authenticate_additional_data(bytes('', 'utf-8'))

        # Encrypt the plaintext and get the associated ciphertext.
        # GCM does not require padding.
        ciphertext = encryptor.update(bytes(padded_private_msg, 'utf-8')) + encryptor.finalize()
        return self.iv, ciphertext, encryptor.tag

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
                    self.public_key = serialization.load_pem_public_key(
                        key_file.read(),
                        backend=default_backend()
                    )
                elif file_extension == ".pub":
                    self.public_key = serialization.load_ssh_public_key(
                        key_file.read(),
                        backend=default_backend()
                    )
                else:
                    raise RuntimeError("Public key file extension "+file_extension+" not supported")
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), key_file_path)

    def read_private_key(self):
        key_file_path = os.path.join(certificate_folder_path, "id_rsa")
        if os.path.exists(key_file_path):
            with open(key_file_path, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
            return private_key
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), key_file_path)

    def encrypt_data_rsa(self, data: str):
        encrypted = self.public_key.encrypt(
            bytes(data, 'utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    def decrypt_data_rsa(self, data: bytes, private_key):
        decrypted = private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))
        return decrypted.decode('utf-8')

    def encrypt_symmetric_asymmetric(self, data):
        encrypted = self.encrypt_data_aes(data)
