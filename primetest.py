from random import randint as rint
def modexp(base, exp, mod):
    if mod == 1:
        return 0
    r = 1
    while exp > 0:
        if exp % 2 == 1:
            r = (r * base) % mod
        exp = exp >> 1
        base = base * base % mod
    return r

def primetest(p, k = 10):
    if p == 2:
        return True
    t = 0
    s = p - 1
    while s % 2 == 0:
        t += 1
        s = s // 2
    for i in range(k):
        a = rint(2, p - 1)
        if modexp(a, p-1, p) != 1:
            return False
        term = modexp(a, int(s), p)
        if term == p-1 or term == 1:
            continue
        for i in range(1, t):
            term2 = (term * term) % p
            if term2 == 1 and term == p-1:
                break
            if term2 == 1 and term != p-1:
                return False
            term = term2
    return True

def generatePrimes(size, amount = 1, safety = -1):
    """
    Generates 'amount' primes on the interval
    2^size, 2^(size + 1)
    """
    if safety < 0:
        safety = size
    primes = []
    while len(primes) < amount:
        p = 0
        for i in range(size - 1):
            p += rint(0, 1)
            p *= 2
        p += 2 ** size + 1
        if primetest(p, safety + 10):
            primes.append(p)
    return primes
        
def extended_gcd(a, b):
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while r1 != 0:
        q, r = r0 // r1, r0 % r1
        s = s0 - s1 * q
        t = t0 - t1 * q
        s0, t0 = s1, t1
        s1, t1 = s, t
        r0 = r1
        r1 = r
    return r0, s0, t0

def modinv(a, mod):
    d, inv, _ = extended_gcd(a, mod)
    if d != 1:
        return 0
    while inv < 0:
        inv += mod
    return inv % mod
