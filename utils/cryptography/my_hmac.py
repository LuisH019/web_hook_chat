import random

# utils.cryptography.

from utils.cryptography.my_sha256 import sha256Encode
from utils.cryptography.to_list_converter import readInt, readString

def hmacGenerateKey(keySize):
    return random.randrange(pow(2, keySize - 1), pow(2, keySize))

def hmacEncodeSha256(message, key):
    blockSize = 32
    opad = 92
    ipad = 54

    keyByteSize = (key.bit_length() + 7) // 8 or 1

    if (keyByteSize > blockSize):
        key = int(sha256Encode(key, "int"), 16)
    elif (keyByteSize < blockSize):
        while (keyByteSize < blockSize):
            key = key << 8
            keyByteSize += 1

    key = readInt(key)

    iKeyPad = [x ^ ipad for x in key]
    oKeyPad = [x ^ opad for x in key]

    iHashInput = iKeyPad + readString(message)
    iHash = sha256Encode(iHashInput, "lin")

    oHashInput = oKeyPad + readInt(int(iHash, 16))
    result = sha256Encode(oHashInput, "lin")

    return result

