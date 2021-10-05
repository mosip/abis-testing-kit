import base64
import errno
import logging
import os
import re

from Crypto.Cipher import PKCS1_OAEP
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
        self.key_splitter = key_splitter or '#KEY_SPLITTER#'
        self.read_public_key()
        self.aes_key = os.urandom(32)
        self.random = os.urandom(32)

    def encrypt_data_abis_with_0_9_specs(self, data: str):
        iv = self.random[:12]
        myPrint("length of iv: " + str(len(iv)))
        ciphertext = self.encrypt_data_aes(bytes(data, 'utf-8'), iv, self.random)
        encrypted_aes_key, mod, exp = self.encrypt_data_rsa_bytes(self.aes_key)
        key_splitter_bytes = bytes(self.key_splitter, 'utf-8')
        thumbprint = self.getPublicCertificateThumbprint()
        final_response = b''.join([bytes("VER_R2", 'utf-8'), bytes.fromhex(thumbprint), encrypted_aes_key, key_splitter_bytes, self.random, iv, ciphertext])
        myPrint("encrypt AAD: " + base64.urlsafe_b64encode(self.random).decode('utf-8'))
        myPrint("encrypt iv: " + base64.urlsafe_b64encode(iv).decode('utf-8'))
        # myPrint("encrypt ciphertext: " + base64.urlsafe_b64encode(ciphertext).decode('utf-8'))
        myPrint("encrypt aes_key: " + base64.urlsafe_b64encode(self.aes_key).decode('utf-8'))
        myPrint("encrypt hex aes_key: " + self.aes_key.hex())
        myPrint("encrypt encrypted_aes_key length: " + str(len(encrypted_aes_key)))
        myPrint("encrypt encrypted_aes_key: " + str(encrypted_aes_key))
        myPrint("encrypt encrypted_aes_key: " + base64.urlsafe_b64encode(encrypted_aes_key).decode('utf-8'))
        myPrint("encrypt rsa_public_key: " + self.public_key.decode('utf-8'))
        myPrint("encrypt thumbprint length: " + str(len(bytes.fromhex(thumbprint))))
        myPrint("encrypt thumbprint: " + thumbprint)
        myPrint("encrypt rsa_mod: " + str(mod))
        myPrint("encrypt rsa_exp: " + str(exp))
        return base64.b64encode(final_response), mod

    def encrypt_data_aes(self, data: bytes, iv: bytes, aad: bytes):
        # Construct an AES-GCM Cipher object with the given key and a
        ciphertext = AESGCM(self.aes_key).encrypt(iv, data, aad)
        return ciphertext

    def read_public_key(self):
        key_file_path = os.path.join(certificate_folder_path, self.conf.public_key_file)
        if os.path.exists(key_file_path):
            filename, file_extension = os.path.splitext(key_file_path)
            with open(key_file_path, "rb") as key_file:
                self.public_key = RSA.importKey(key_file.read()).exportKey(format='PEM', passphrase=None, pkcs=1)
                # if file_extension == ".crt":
                #     self.public_key = RSA.importKey(key_file.read()).exportKey(format='PEM', passphrase=None, pkcs=1)
                # elif file_extension == ".pub":
                #     self.public_key = RSA.importKey(key_file.read()).exportKey(format='PEM', passphrase=None, pkcs=1)
                # else:
                #     raise RuntimeError("Public key file extension "+file_extension+" not supported")
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

    def getPublicKeyMod(self):
        key = RSA.importKey(self.public_key)
        return key.n

    def getPublicCertificateThumbprint(self):
        key = RSA.importKey(self.public_key)
        stripped = re.sub(r'-----(BEGIN|END) PUBLIC KEY-----', '', key.exportKey().decode('utf-8'))
        myPrint("getPublicCertificateThumbprint: " + stripped)
        h = SHA256.new()
        h.update(base64.urlsafe_b64decode(stripped))
        return h.hexdigest()
