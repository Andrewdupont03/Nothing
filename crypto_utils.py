import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_message(message: str, password: str) -> str:
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    token = Fernet(key).encrypt(message.encode())
    return base64.urlsafe_b64encode(salt + token).decode()

def decrypt_message(token: str, password: str) -> str:
    data = base64.urlsafe_b64decode(token.encode())
    salt, ciphertext = data[:16], data[16:]
    key = _derive_key(password, salt)
    return Fernet(key).decrypt(ciphertext).decode()
