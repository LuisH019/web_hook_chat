from utils.crypto.prime_number_generator import generatePrimeNumber
from utils.crypto.my_base64 import base64Encode, base64Decode

def modInverse (r1, r2, t1, t2, phi):
    q = r1 // r2
        
    r = r1 - q * r2
        
    t = t1 - q * t2
    
    if r == 1:
        if t < 0:
            t = phi + t
        return t
        
    return modInverse(r2, r, t2, t, phi)

def rsaKeyBase64Encode(key):
    return base64Encode(', '.join(map(str, key)))

def rsaGenerateKeys():
    p = generatePrimeNumber(1024)
    q = generatePrimeNumber(1024)

    n = p * q

    phi = (p - 1) * (q - 1)

    e = 65537

    d = modInverse(phi, e, 0, 1, phi)
    
    publicKey = (e, n)
    privateKey = (d, n)
    
    return rsaKeyBase64Encode(publicKey), rsaKeyBase64Encode(privateKey)

def rsaKeyBase64Decode(encodedKey):
    return tuple(map(int, base64Decode(encodedKey).split(', ')))

def rsaEncode(message, publicKey):
    try:
        e, n = rsaKeyBase64Decode(publicKey)
        
        return [pow(ord(m), e, n) for m in message]
    except Exception as e:
        return ("Erro ao codificar a mensagem:", str(e))

def rsaDecode(cypherText, privateKey):
    try:
        d, n = rsaKeyBase64Decode(privateKey)
        
        decoded = []

        decoded = [chr(pow(c, d, n)) for c in cypherText]
        decoded = ''.join(decoded)

        return decoded
    except Exception as e:
        return ("Erro ao decodificar a mensagem:", str(e))

