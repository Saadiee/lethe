from pathlib import Path
import os
import pytest

from cryptoshred.files.verify import verify_file


def test_verify_valid_lethe_file(tmp_path: Path):
    # create a valid-looking .lethe file: 12-byte nonce + ciphertext
    p = tmp_path / "data.lethe"
    p.write_bytes(os.urandom(12) + b"x")

    # should not raise
    verify_file(p)


def test_verify_rejects_wrong_extension(tmp_path: Path):
    p = tmp_path / "data.bin"
    p.write_bytes(os.urandom(12) + b"x")

    with pytest.raises(ValueError):
        verify_file(p)


def test_verify_rejects_too_small_file(tmp_path: Path):
    p = tmp_path / "data.lethe"
    p.write_bytes(b"short")  # < 13 bytes

    with pytest.raises(ValueError):
        verify_file(p)


def test_verify_rejects_directory(tmp_path: Path):
    with pytest.raises(IsADirectoryError):
        verify_file(tmp_path)


def test_verify_rejects_nonexistent_path():
    p = Path("does_not_exist.lethe")

    with pytest.raises(FileNotFoundError):
        verify_file(p)
