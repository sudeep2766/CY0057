# Euclidean Algorithm
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)


# Extended Euclidean Algorithm
# Returns (g, x, y) such that:
# ax + by = gcd(a, b)
def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)

    g, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return (g, x, y)


# Modular Inverse
def modular_inverse(a, m):
    g, x, y = extended_gcd(a, m)

    if g != 1:
        return None

    return x % m


# Main program
while True:

    choice = input("GCD(G) or Modular Inv(M)? ").lower()

    if choice == 'g':

        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))

        print("GCD:", gcd(a, b))

    elif choice == 'm':

        a = int(input("Enter number: "))
        m = int(input("Enter modulus: "))

        inverse = modular_inverse(a, m)

        if inverse is not None:
            print(f"Modular inverse of {a} modulo {m} = {inverse}")
        else:
            print(f"Modular inverse does not exist because gcd({a}, {m}) != 1")

    else:
        print("Invalid choice. Enter G or M.")
