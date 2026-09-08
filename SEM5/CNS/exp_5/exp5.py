def modular_exponentiation(a, b, m):
    return pow(a, b, m)


def modular_inverse(a, m):
    try:
        return pow(a, -1, m)
    except ValueError:
        return None


# Modular exponentiation



# Modular exponentiation
while True:
    opt = input("Modular exp(E) or Modular inverse(I)?: ")
    if opt == "e":

        print("For a^b mod(m)")
        a, b, m = map(int, input("Enter a, b and m: ").split())
        print(f"{a}^{b} mod {m} =", modular_exponentiation(a, b, m))

    elif opt == "i":
        a, m = map(int, input("Enter a mod m: ").split())
        inverse = modular_inverse(a, m)
        print(inverse)

        if inverse is not None:
            print("Modular inverse =", inverse)
        else:
            print("Modular inverse does not exist")
    else:
        break
