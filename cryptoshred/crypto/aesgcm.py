import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt(plaintext: bytes, key_bytes: bytes) -> tuple[bytes, bytes]:

    if not isinstance(plaintext, bytes):
        raise TypeError(f"Plaintext type must be bytes, not {type(plaintext).__name__}")
    if not isinstance(key_bytes, bytes):
        raise TypeError(f"Key type must be bytes, not {type(key_bytes).__name__}")
    if not len(key_bytes) == 32:
        raise ValueError("Key length is not 32")

    aesgcm = AESGCM(key_bytes)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce, ciphertext

def decrypt(nonce: bytes, ciphertext: bytes, key_bytes: bytes) -> bytes:
    if not isinstance(nonce, bytes):
        raise TypeError(f"nonce type must be bytes, not {type(nonce).__name__}")
    if not isinstance(ciphertext, bytes):
        raise TypeError(f"Ciphertext type must be bytes, not {type(ciphertext).__name__}")
    if not isinstance(key_bytes, bytes):
        raise TypeError(f"Key type must be bytes, not {type(key_bytes).__name__}")
    if not len(key_bytes) == 32:
        raise ValueError("Key length is not 32")
    if not len(nonce) == 12:
        raise ValueError("Nonce length is not 12")

    aesgcm = AESGCM(key_bytes)
    return aesgcm.decrypt(nonce,ciphertext, None)
