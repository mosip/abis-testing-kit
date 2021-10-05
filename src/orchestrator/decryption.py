import base64
import errno
import logging
import os

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


class Decryption:
    conf = AppConfig()

    def __init__(self, key_splitter=None):
        self.private_key = None
        self.key_splitter = key_splitter or '#KEY_SPLITTER#'
        self.read_private_key()

    def decrypt_data_abis_with_0_9_specs(self, data: str, rsa_mod: int = None):
        if rsa_mod is None or rsa_mod == self.getPrivateKeyMod():
            data_bytes = base64.urlsafe_b64decode(data)

            # Part 1
            enc_version = str(data_bytes[:6])
            myPrint("decrypt data enc_version: " + enc_version)
            thumbprint = data_bytes[6:38].hex()
            myPrint("decrypt data thumbprint length: " + str(len(data_bytes[6:38])))
            myPrint("decrypt data thumbprint: " + thumbprint)
            encrypted_aes_key = data_bytes[38:294]
            myPrint("decrypt encrypted_aes_key length: " + str(len(data_bytes[38:294])))
            myPrint("decrypt data encrypted_aes_key: " + str(encrypted_aes_key))
            myPrint("decrypt data encrypted_aes_key: " + base64.urlsafe_b64encode(encrypted_aes_key).decode('utf-8'))

            # Part 2
            key_splitter_aad_iv_text = data_bytes[294:]
            myPrint("decrypt key_splitter_aad_iv_text length: " + str(len(key_splitter_aad_iv_text)))
            key_splitter_bytes = bytes(self.key_splitter, 'utf-8')
            aad_iv_text = key_splitter_aad_iv_text.replace(key_splitter_bytes, b'')
            myPrint("decrypt aad_iv_text length: " + str(len(aad_iv_text)))
            aad = aad_iv_text[:32]
            myPrint("decrypt AAD: " + base64.urlsafe_b64encode(aad).decode('utf-8'))
            iv_bytes = aad_iv_text[32:44]
            myPrint("decrypt iv_bytes: " + base64.urlsafe_b64encode(iv_bytes).decode('utf-8'))
            encrypted_data = aad_iv_text[44:]
            myPrint("decrypt encrypted_data: " + base64.urlsafe_b64encode(encrypted_data).decode('utf-8'))

            aes_key = self.decrypt_data_rsa(encrypted_aes_key)
            myPrint("decrypt aes_key: " + base64.b64encode(aes_key).decode('utf-8'))

            data = self.decrypt_data_aes(encrypted_data, aes_key, iv_bytes, aad)
            myPrint("decrypt data: " + str(data))
        else:
            raise RuntimeError("Mod are not matching")
        return

    def decrypt_data_aes(self, data: bytes, aes_key: bytes, iv: bytes, aad: bytes):
        data = AESGCM(aes_key).decrypt(iv, data, aad)
        return data.decode('utf-8')

    def read_private_key(self):
        key_file_path = os.path.join(certificate_folder_path, "root.key")
        if os.path.exists(key_file_path):
            with open(key_file_path, "rb") as key_file:
                self.private_key = RSA.importKey(key_file.read()).exportKey(format='PEM', passphrase=None, pkcs=1)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), key_file_path)

    def decrypt_data_rsa(self, data: bytes, mod: int = None):
        key = RSA.importKey(self.private_key)
        if mod is None or mod == key.n:
            cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
            message = cipher.decrypt(data)
            return message
        else:
            raise RuntimeError("Private key mod: "+str(key.n)+"\nPublic key mod: "+str(mod))

    def getPrivateKeyMod(self):
        key = RSA.importKey(self.private_key)
        return key.n
