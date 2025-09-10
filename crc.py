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

def encodeData(data, key):
    # Appends CRC remainder to the original data.
    n = len(key)
    
    # Append n-1 zeros
    padded_data = data + '0' * (n - 1)  
    remainder = mod2div(padded_data, key)
    
    # Return data + CRC
    return data + remainder  

def receiver(code, key):
    # Checks if received data has errors (remainder = 0).
    remainder = mod2div(code, key)
    return 1 if '1' not in remainder else 0

if __name__ == "__main__":
    data = "100100"
    key = "1101"
    
    print("Sender Side")
    print("Data:", data)
    print("Key:", key)
    code = encodeData(data, key)
    print("Encoded Data:", code, "\n")

    print("Receiver Side")
    if receiver(code, key):
        print("Data is correct (No errors detected)")
    else:
        print("Data is incorrect (Error detected)")
