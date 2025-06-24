def readInt (n, encoding=None):
    nByteList = []

    nBitLength = n.bit_length()

    for i in range(0, nBitLength, 8):
        nByte = (n >> i) % pow(2, 8)

        if encoding == 'utf-8':
            byteUtf8 = []

            for byte in chr(nByte).encode('utf-8'):
                byteUtf8.append(byte)
            
            byteUtf8.reverse()

            nByteList.extend(byteUtf8)
        else:
            nByteList.append(nByte)

    nByteList.reverse()
    
    return nByteList

def readListOfInt(message):
    return [byte for i in message for byte in chr(i).encode('utf-8')]

def readString(message):
    return [byte for char in message for byte in char.encode('utf-8')]

def readFile(path):
    f = open(path, 'rb')
    bin = f.read()

    fileByteList = [b for b in bin]

    f.close()
    
    return fileByteList