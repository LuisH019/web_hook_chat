import random, sys

# from util.cryptography.my_sha256 import sha256Encode

from my_sha256 import sha256Encode

def hmacEncode(message, key):
    blockSize = 32
    opad = 92
    ipad = 54

    keyByteSize = (key.bit_length() + 7) // 8 or 1

    if (keyByteSize > blockSize):
        key = int (sha256Encode(key, 'i'), 16)
    elif (keyByteSize < blockSize):
        while (keyByteSize < blockSize):
            key = key << 8
            keyByteSize += 1
        

# # keyInt = random.randrange(pow(2, 255), pow(2, 256))
# # key = keyInt.to_bytes((keyInt.bit_length() + 7) // 8 or 1, byteorder='big')

# # print(key.decode('latin1'))

# # print(sha256Encode(key.decode('latin1'), 's'))

# test = int(sha256Encode("yyyy", 's'), 16)

# print(((test.bit_length() + 7) // 8 or 1))

# # print(sha256Encode("7", 's'))
key = 21342432151

key = key.to_bytes((key.bit_length() + 7) // 8 or 1, byteorder='big')

opad = 0x5c

oKey = bytes([x ^ opad for x in key])

print(oKey)

key2 = 21342432151

key2Bytes = []

print(key2>>0)

for i in range(8, ((key2.bit_length() + 7) // 8 or 1), 8):
    print(key2 >> i)
    key2Bytes.append(key2 >> i)

print(key2Bytes)

opad2 = 92

oKey2 = [x ^ opad2 for x in key2Bytes]


