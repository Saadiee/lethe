import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# -------------------------------------------------------------------
# 1. Read plaintext from disk as raw bytes
# -------------------------------------------------------------------
# Crypto always operates on bytes, never on strings.
# Binary mode ("rb") prevents any encoding or newline conversion.
with open("input.txt", "rb") as f:
    plaintext = f.read()

# At this point:
# - plaintext is of type `bytes`
# - its contents are exactly what exists on disk


# -------------------------------------------------------------------
# 2. Generate cryptographic material
# -------------------------------------------------------------------

# AES-256 key: 32 cryptographically secure random bytes
key = os.urandom(32)

# A different random key to simulate key loss / wrong key
bad_key = os.urandom(32)

# AES-GCM nonce: 12 bytes (96 bits)
# Must be UNIQUE per encryption for the same key
# It is NOT secret and can be stored alongside ciphertext
nonce = os.urandom(12)


# -------------------------------------------------------------------
# 3. Encrypt using AES-GCM
# -------------------------------------------------------------------

# Bind the algorithm to the secret key
aesgcm = AESGCM(key)

# Encrypt the plaintext
# Parameters:
# - nonce: unique value (required)
# - plaintext: bytes to encrypt
# - None: no Additional Authenticated Data (AAD) for now
#
# Output:
# - ciphertext (bytes)
# - authentication tag is INCLUDED inside this value
ciphertext = aesgcm.encrypt(
    nonce,
    plaintext,
    None
)

# IMPORTANT:
# ciphertext is opaque binary data.
# Printing it is fine for learning, but NEVER do this in real tools.
# print(ciphertext)


# -------------------------------------------------------------------
# 4. Attempt decryption with the WRONG key (intentional failure)
# -------------------------------------------------------------------

try:
    # This MUST fail because bad_key != key
    AESGCM(bad_key).decrypt(
        nonce,
        ciphertext,
        None
    )

    # If this ever prints, something is catastrophically wrong
    print("UNEXPECTED SUCCESS: decryption should have failed")

except Exception as e:
    # Expected path:
    # AES-GCM detects authentication failure and refuses to decrypt
    print("PASS: Decryption failed as expected")
    print("Exception type:", type(e).__name__)


# -------------------------------------------------------------------
# 5. (Optional) Correct decryption path (for sanity)
# -------------------------------------------------------------------

# Uncomment this to confirm correctness when using the right key
#
# recovered_plaintext = AESGCM(key).decrypt(
#     nonce,
#     ciphertext,
#     None
# )
#
# assert recovered_plaintext == plaintext
# print("PASS: Correct key successfully recovered plaintext")

# -------------------------------------------------------------------
# 6. Write out encrypted file
# -------------------------------------------------------------------
# Q1: Can I use my custom extension after the file name?

with open("cipher.txt", "wb") as f:
    f.write(nonce+ciphertext)

with open("cipher.txt", "rb") as f:
    nonce_plus_cipher = f.read()


sliced_nonce = nonce_plus_cipher[:12]
sliced_ciphertext = nonce_plus_cipher[12:]
print("Nonce length:", len(sliced_nonce))
print("Ciphertext length:", len(sliced_ciphertext))

recovered_text = AESGCM(key).decrypt(sliced_nonce, sliced_ciphertext, None)
print("recovered text:", recovered_text)
assert recovered_text == plaintext
