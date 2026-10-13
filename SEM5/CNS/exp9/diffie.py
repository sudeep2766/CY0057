p = int(input("Enter Prime Number (p): "))
g = int(input("Enter Primitive Root (g): "))

a = int(input("Enter Alice's Private Key: "))

b = int(input("Enter Bob's Private Key: "))

A = pow(g, a, p)

B = pow(g, b, p)

print("\nAlice's Public Key:", A)
print("Bob's Public Key :", B)

Alice_secret = pow(B, a, p)
Bob_secret = pow(A, b, p)

print("\nAlice's Shared Secret Key:", Alice_secret)
print("Bob's Shared Secret Key :", Bob_secret)

if Alice_secret == Bob_secret:
    print("\nSecure Key Exchange Successful!")
else:
    print("\nKey Exchange Failed!")
