from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Generate RSA Key Pair
key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

# Input Message
message = input("Enter Message: ").encode()

# Hash the Message
hash_value = SHA256.new(message)

# Generate Digital Signature
signature = pkcs1_15.new(private_key).sign(hash_value)

print("\nDigital Signature Generated Successfully.")

# Print Digital Signature
print("\nDigital Signature:")
print(signature.hex())

# Verification
try:
    pkcs1_15.new(public_key).verify(hash_value, signature)
    print("\nDigital Signature Verified Successfully.")

except (ValueError, TypeError):
    print("\nDigital Signature Verification Failed.")

