import os
import pytest

from cryptoshred.crypto.aesgcm import encrypt, decrypt


def test_encrypt_decrypt_roundtrip():
    """
    Encrypting and then decrypting with the same key
    should return the original plaintext.
    """
    plaintext = b"hello world"
    key = os.urandom(32)

    nonce, ciphertext = encrypt(plaintext, key)
    recovered = decrypt(nonce, ciphertext, key)

    assert recovered == plaintext


def test_wrong_key_fails():
    """
    Decryption with the wrong key must fail.
    """
    plaintext = b"secret data"
    key = os.urandom(32)
    wrong_key = os.urandom(32)

    nonce, ciphertext = encrypt(plaintext, key)

    with pytest.raises(Exception):
        decrypt(nonce, ciphertext, wrong_key)


def test_tampered_ciphertext_fails():
    """
    Any modification to ciphertext must cause failure.
    """
    plaintext = b"important"
    key = os.urandom(32)

    nonce, ciphertext = encrypt(plaintext, key)

    tampered = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0x01])

    with pytest.raises(Exception):
        decrypt(nonce, tampered, key)


def test_tampered_nonce_fails():
    """
    Using a different nonce must cause failure.
    """
    plaintext = b"data"
    key = os.urandom(32)

    nonce, ciphertext = encrypt(plaintext, key)
    bad_nonce = os.urandom(12)

    with pytest.raises(Exception):
        decrypt(bad_nonce, ciphertext, key)


def test_invalid_key_length_rejected():
    """
    Keys that are not 32 bytes must be rejected.
    """
    with pytest.raises(ValueError):
        encrypt(b"data", os.urandom(16))


def test_invalid_input_types_rejected():
    """
    Non-bytes inputs must be rejected immediately.
    """
    key = os.urandom(32)

    with pytest.raises(TypeError):
        encrypt("not-bytes", key)

    with pytest.raises(TypeError):
        decrypt(b"nonce", b"ciphertext", "not-bytes")
