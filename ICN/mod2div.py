def findXor(a, b):
    #Performs bitwise XOR between two binary strings (a and b).
    n = len(b)
    result = ""
    for i in range(1, n):  # Skip first bit (CRC standard)
        result += '0' if a[i] == b[i] else '1'
    return result

def mod2div(dividend, divisor):
    # Performs Modulo-2 division (CRC division algorithm).
    n = len(dividend)
    pick = len(divisor)
    tmp = dividend[0:pick]  # Initial window

    while pick < n:
        if tmp[0] == '1':
            # XOR with divisor and bring down next bit
            tmp = findXor(divisor, tmp) + dividend[pick]
        else:
            # XOR with zeros and bring down next bit
            tmp = findXor('0' * pick, tmp) + dividend[pick]
        pick += 1

    # Final XOR step
    if tmp[0] == '1':
        tmp = findXor(divisor, tmp)
    else:
        tmp = findXor('0' * pick, tmp)
    return tmp

def receiver(code, key):
    # Checks if received data has errors (remainder = 0).
    remainder = mod2div(code, key)
    return 1 if '1' not in remainder else 0

if __name__ == "__main__":

    code = '101101010'
    key = "1101"

    if receiver(code, key):
        print("Data is correct (No errors detected)")
    else:
        print("Data is incorrect (Error detected)")
