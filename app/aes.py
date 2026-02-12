from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import os

AES_KEY = os.environ['AES_KEY']


def encrypt_aes(secret):
    salt = get_random_bytes(16)
    key = PBKDF2(AES_KEY.encode(), salt, dkLen=16, count=10000 )
    iv = get_random_bytes(16)
    aes = AES.new(key, AES.MODE_CFB, iv)
    aes_secret = aes.encrypt(secret.encode())
    return aes_secret, iv, salt


def decrypt_aes(aes_secret, iv, salt):
    key = PBKDF2(AES_KEY.encode(), salt, dkLen=16, count=10000)
    aes = AES.new(key, AES.MODE_CFB, iv)
    secret = aes.decrypt(aes_secret)
    return secret.decode()
