def xor(a, b):
    """Perform bitwise XOR between two equal-length binary strings."""
    result = ""
    for i in range(len(a)):
        result += '0' if a[i] == b[i] else '1'
    return result


def mod2div(dividend, divisor):
    """Perform modulo-2 division and return the remainder."""
    pick = len(divisor)
    tmp = dividend[:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * len(divisor), tmp) + dividend[pick]
        pick += 1

    # Final step
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * len(divisor), tmp)

    # Return remainder (drop the first bit)
    return tmp[1:]


def encode_data(data, key):
    """Encode data using CRC."""
    # Append zeros (degree = len(key)-1)
    padded = data + '0' * (len(key) - 1)

    # Compute remainder
    remainder = mod2div(padded, key)

    # Encoded output = original data + CRC remainder
    return data + remainder


# -----------------------------
# Example: Encode Data Using CRC
# -----------------------------
data = "100100"
key = "1101"   # CRC-3 polynomial

encoded = encode_data(data, key)


print("Data       :", data)
print("Generator  :", key)
print("Encoded Data:", encoded)


