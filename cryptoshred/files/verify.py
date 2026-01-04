from pathlib import Path


NONCE_SIZE = 12
MIN_FILE_SIZE = NONCE_SIZE + 1

def verify_file(path: Path) -> None:
    """
    Verify that a file is a structurally valid Lethe-encrypted artifact.
    Success: returns None
    Failure: raises an exception
    """
    if not isinstance(path, Path):
        raise TypeError(f"path must be a pathlib.Path, not {type(path).__name__}")
    if not path.exists():
        raise FileNotFoundError(f"file does not exist: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"path is not a regular file: {path}")
    if path.suffix != ".lethe":
        raise ValueError(f"invalid file extension (expected .lethe): {path}")

    file_size = path.stat().st_size
    if file_size < MIN_FILE_SIZE:
        raise ValueError(
            f"file too small to be a valid Lethe artifact: {file_size} bytes"
        )
    with path.open("rb") as f:
        nonce = f.read(NONCE_SIZE)
    if len(nonce) != NONCE_SIZE:
        raise ValueError("failed to read full nonce")
    return None
