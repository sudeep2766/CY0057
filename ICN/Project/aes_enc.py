from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, struct

MAGIC = b"AESEncv1"
SALT_LEN = 16
NONCE_LEN = 12
KEY_LEN = 32  # AES-256

# --- KEY DERIVATION ---
def derive_key(password: str, salt: bytes):
    kdf = Scrypt(
        salt=salt,
        length=KEY_LEN,
        n=2**14,
        r=8,
        p=1
    )
    return kdf.derive(password.encode())

# --- ENCRYPTION ---
def encrypt_file(in_path, out_path, password):
    salt = os.urandom(SALT_LEN)
    nonce = os.urandom(NONCE_LEN)
    key = derive_key(password, salt)

    aesgcm = AESGCM(key)
    data = open(in_path, "rb").read()
    ciphertext = aesgcm.encrypt(nonce, data, None)

    with open(out_path, "wb") as f:
        f.write(MAGIC)
        f.write(struct.pack("B", SALT_LEN))
        f.write(salt)
        f.write(struct.pack("B", NONCE_LEN))
        f.write(nonce)
        f.write(struct.pack(">Q", len(ciphertext)))
        f.write(ciphertext)

# --- DECRYPTION ---
def decrypt_file(enc_path, out_path, password):
    data = open(enc_path, "rb").read()
    i = 0

    if data[:len(MAGIC)] != MAGIC:
        raise ValueError("Bad file header!")

    i += len(MAGIC)

    salt_len = data[i]; i += 1
    salt = data[i:i+salt_len]; i += salt_len

    nonce_len = data[i]; i += 1
    nonce = data[i:i+nonce_len]; i += nonce_len

    (ct_len,) = struct.unpack(">Q", data[i:i+8])
    i += 8

    ciphertext = data[i:i+ct_len]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    open(out_path, "wb").write(plaintext)
