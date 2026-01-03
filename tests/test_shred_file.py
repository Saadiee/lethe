import os
from pathlib import Path
import pytest

from cryptoshred.files.shredder import shred_file


def test_shred_file_success(tmp_path: Path):
    """
    Happy path:
    - plaintext file is encrypted
    - encrypted file exists
    - plaintext file is deleted
    """
    plaintext_path = tmp_path / "secret.txt"
    plaintext_data = b"top secret data"

    plaintext_path.write_bytes(plaintext_data)

    encrypted_path = shred_file(plaintext_path)

    assert not plaintext_path.exists()
    assert encrypted_path.exists()
    assert encrypted_path.name == "secret.txt.lethe"

    encrypted_bytes = encrypted_path.read_bytes()
    assert len(encrypted_bytes) > 12  # nonce + ciphertext


def test_shred_file_nonexistent_path():
    """
    Non-existent input file must fail cleanly.
    """
    with pytest.raises(FileNotFoundError):
        shred_file(Path("does_not_exist.txt"))


def test_shred_file_directory_rejected(tmp_path: Path):
    """
    Directories must not be accepted.
    """
    with pytest.raises(IsADirectoryError):
        shred_file(tmp_path)


def test_shred_file_existing_encrypted_file(tmp_path: Path):
    """
    Must not overwrite an existing .lethe file.
    """
    plaintext_path = tmp_path / "data.bin"
    plaintext_path.write_bytes(b"data")

    encrypted_path = tmp_path / "data.bin.lethe"
    encrypted_path.write_bytes(b"existing ciphertext")

    with pytest.raises(FileExistsError):
        shred_file(plaintext_path)


def test_plaintext_not_deleted_if_encryption_fails(monkeypatch, tmp_path: Path):
    """
    If encryption fails, plaintext must remain untouched.
    """

    plaintext_path = tmp_path / "fail.txt"
    plaintext_path.write_bytes(b"important")

    def broken_encrypt(*args, **kwargs):
        raise RuntimeError("encryption failed")

    monkeypatch.setattr(
        "cryptoshred.files.shredder.encrypt",
        broken_encrypt,
    )

    with pytest.raises(RuntimeError):
        shred_file(plaintext_path)

    assert plaintext_path.exists()
