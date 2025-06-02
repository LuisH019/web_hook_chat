import math, random

def primeSieve (sieveSize):
    sieve = [True] * sieveSize
    sieve[0] = sieve[1] = False

    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i
    
    primes = []

    for i in range(sieveSize):
        if sieve[i]:
            primes.append(i)

    return primes

def rabinMiller (n):
    if n == 2 or n == 3:
        return True
    
    if n % 2 == 0 or n < 2:
        return False
    
    s = n - 1
    t = 0

    while s % 2 == 0:
        s //= 2
        t += 1

    for trials in range(5):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)

        if x != 1:
            i = 0
            while x != n - 1:
                if i == t - 1:
                    return False
                x = pow(x, 2, n)
                i += 1
    return True

def isPrime (n):
    if n < 2:
        return False
    for prime in primeSieve(100):
        if (n % prime == 0):
            return False
        if (n == prime):
            return True
        
    return rabinMiller(n)

def generatePrimeNumber (keySize):
    while True:
        n = random.randrange(pow(2, keySize - 1), pow(2, keySize))
        if isPrime(n):
            return n
        