import pytest
from keys.key_manager import generate_key


def test_key_is_usable_after_generation():
    """
    A newly generated key should be usable and not destroyed.
    """
    handle = generate_key()

    key_bytes = handle.getKeyBytes()

    assert isinstance(key_bytes, bytes)
    assert len(key_bytes) == 32
    assert handle.isDestroyed() is False


def test_access_after_destroy_raises():
    """
    Accessing key material after destruction must fail loudly.
    """
    handle = generate_key()
    handle.destroy_key()

    assert handle.isDestroyed() is True

    with pytest.raises(RuntimeError):
        handle.getKeyBytes()


def test_double_destroy_is_safe():
    """
    Destroying a key twice should be safe and idempotent.
    """
    handle = generate_key()

    handle.destroy_key()
    handle.destroy_key()  # should not raise

    assert handle.isDestroyed() is True

    with pytest.raises(RuntimeError):
        handle.getKeyBytes()


def test_full_lifecycle():
    """
    Full lifecycle:
    generate -> use -> destroy -> permanent failure
    """
    handle = generate_key()

    # Key usable initially
    _ = handle.getKeyBytes()

    # Destroy key
    handle.destroy_key()

    # Key unusable forever
    with pytest.raises(RuntimeError):
        handle.getKeyBytes()
