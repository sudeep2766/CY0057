def encrypt(text, key):
    text = text.replace(" ", "").upper()
    columns = len(key)
    rows = (len(text) + columns - 1) // columns

    # Pad the text if necessary
    text += "X" * (rows * columns - len(text))

    # Create the grid
    grid = [text[i:i + columns] for i in range(0, len(text), columns)]

    # Read columns according to sorted key
    order = sorted(range(columns), key=lambda i: key[i])

    encrypted = ""
    for col in order:
        for row in grid:
            encrypted += row[col]

    return encrypted


def decrypt(ciphertext, key):
    columns = len(key)
    rows = len(ciphertext) // columns

    order = sorted(range(columns), key=lambda i: key[i])

    # Create empty grid
    grid = [[""] * columns for _ in range(rows)]

    index = 0
    for col in order:
        for row in range(rows):
            grid[row][col] = ciphertext[index]
            index += 1

    decrypted = "".join("".join(row) for row in grid)

    # Remove padding X's
    return decrypted.rstrip("X")


# Example
# message = "HELLO WORLD"
# key = "431256"

# encrypted = encrypt(message, key)
# print("Encrypted:", encrypted)

# decrypted = decrypt(encrypted, key)
# print("Decrypted:", decrypted)

a = input("Enc or dec? ")
if a  == 'e':
    message = input("Enter message: ")
    key = (input("Enter key: "))
    encrypted = encrypt(message, key)
    print("Encrypted:", encrypted)
elif a == 'd':
    encrypted = input("Enter cipher: ")
    key = (input("Enter key: "))
    decrypted = decrypt(encrypted, key)
    print("Decrypted:", decrypted)

