from pathlib import Path
from cryptoshred.keys.key_manager import generate_key
from cryptoshred.crypto.aesgcm import encrypt

def shred_file(path: Path) -> Path:
    """
    Encrypt a file and cryptographically shred the original.
    Returns the path to the encrypted (.lethe) file.
    """
    if not isinstance(path, Path):
        raise TypeError(f"path must be a pathlib.Path, not {type(path).__name__}")

    if not path.exists():
        raise FileNotFoundError(f"file does not exist: {path}")

    if not path.is_file():
        raise IsADirectoryError(f"path is not a regular file: {path}")

    encrypted_path = path.with_name(path.name + ".lethe")
    if encrypted_path.exists():
        raise FileExistsError(f"encrypted file already exists: {encrypted_path}")

    with path.open("rb") as f:
        plaintext = f.read()

    key_handle = generate_key()
    key_bytes = key_handle.getKeyBytes()
    nonce, ciphertext = encrypt(plaintext, key_bytes)

    with encrypted_path.open("xb") as f:
        f.write(nonce)
        f.write(ciphertext)

    key_handle.destroy_key()
    path.unlink()

    return encrypted_path
