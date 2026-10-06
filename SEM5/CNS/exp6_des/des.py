from Crypto.Cipher import DES

key = b"12345678"

cipher = DES.new(key, DES.MODE_ECB)

text = input("Enter text to encrypt: ")

# DES requires data in blocks of 8 bytes
data = text.encode()
padding = 8 - (len(data) % 8)
data += bytes([padding]) * padding

encrypted = cipher.encrypt(data)

print("Encrypted text:", encrypted.hex())
