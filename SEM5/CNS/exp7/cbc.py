from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

key = b'1234567890abcdef'
iv = get_random_bytes(16)

plaintext = input("Enter Plain Text: ")

# Encryption
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(
    pad(plaintext.encode(), AES.block_size)
)

print("\nCBC Encrypted Text:")
print(base64.b64encode(ciphertext).decode())

# Decryption
decrypt_cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = unpad(
    decrypt_cipher.decrypt(ciphertext),
    AES.block_size
)

print("\nCBC Decrypted Text:")
print(decrypted.decode())
