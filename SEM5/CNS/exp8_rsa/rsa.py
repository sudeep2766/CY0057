from math import gcd

# Function to calculate modular inverse
def modular_inverse(e, phi):
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None


# Step 1: Choose two prime numbers
p = int(input("Enter p(prime): "))
q = int(input("Enter q(prime): "))
e = int(input("Enter e: "))

# Step 2: Compute n
n = p * q

# Step 3: Compute Euler's Totient
phi = (p - 1) * (q - 1)



if gcd(e, phi) != 1:
    print("Choose another value of e")
    exit()

# Step 5: Compute d
d = modular_inverse(e, phi)

# Display keys
print("Public Key :", (e, n))
print("Private Key:", (d, n))

# Input plaintext
plaintext = input("\nEnter Plain Text: ")

# Step 6: Encryption
cipher = []

for ch in plaintext:
    cipher.append(pow(ord(ch), e, n))

print("\nEncrypted Message:")
print(cipher)

# Step 7: Decryption
decrypted = ""

for c in cipher:
    decrypted += chr(pow(c, d, n))

print("\nDecrypted Message:")
print(decrypted)
