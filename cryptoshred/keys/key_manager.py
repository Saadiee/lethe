import os

class KeyHandle:
    def __init__(self, key_material: bytearray):
        self._key_material = key_material

    def isDestroyed(self) -> bool:
        return self._key_material is None

    def getKeyBytes(self) -> bytes:
        if self._key_material is None:
            raise RuntimeError("Key has been destroyed")
        return bytes(self._key_material)

    def destroy_key(self):
        if self._key_material is None:
            return
        self._key_material[:] = b'\x00' * len(self._key_material)
        self._key_material = None


def generate_key():
    key = bytearray(os.urandom(32))
    return KeyHandle(key)

