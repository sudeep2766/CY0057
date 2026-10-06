from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

key = b'1234567890abcdef'

plaintext = input("Enter Plain Text: ")

# Encryption
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(
    pad(plaintext.encode(), AES.block_size)
)

print("\nECB Encrypted Text:")
print(base64.b64encode(ciphertext).decode())

# Decryption
decipher = AES.new(key, AES.MODE_ECB)
decrypted = unpad(
    decipher.decrypt(ciphertext),
    AES.block_size
)

print("\nECB Decrypted Text:")
print(decrypted.decode())
