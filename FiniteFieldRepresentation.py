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

def polynomialPrimeProduct(a, b, p : int):
    """
    Returns result of the product of the polynomial a(x)
    by the polynomial b(x) in the prime field Zp.
    """

    c = []
    for k in range(len(a) + len(b) - 1):
        c.append(0)
        for i in range(k + 1):
            if i < len(a) and (k - i) < len(b):
                c[k] += a[i] * b[k - i]
        c[k] = c[k] % p
    return c


def polynomialPrimeDivision(a, b, p : int):
    """
    Returns result of the division of the polynomial a(x)
    by the polynomial b(x) in the prime field Zp.
    """

    if len(a) < len(b):
        return ([0], a)

    mainInverse = modinv(b[-1], p)

    k = len(a) - len(b)
    rem = a.copy()
    div = [0 for _ in range(k + 1)]
    while k >= 0:
        div[k] = (rem[k + len(b) - 1] * mainInverse) % p
        for i in range(len(b)):
            rem[k + i] = rem[k + i] - div[k] * b[i]
            while rem[k + i] < 0:
                rem[k + i] += p
            rem[k + i] = rem[k + i] % p
        k -= 1
    
    return (div, rem[:len(b)])

def irreduciblePolynomialFinder(p : int, n : int):
    """
    Finds an irreducible polynomial in Zp of degree n
    by brute force (not really elegant, I know).
    """
    # 1. Creating the polynomial X^{p^n} - X
    bigBoy = [0 for _ in range(p ** n + 1)]
    bigBoy[1] = p - 1
    bigBoy[p ** n] = 1

    # 2. Getting rid of the monomials:

    smallBoy = [0 for _ in range(p + 1)]
    smallBoy[1] = p - 1
    smallBoy[p] = 1
    
    bigBoy, _ = polynomialPrimeDivision(bigBoy, smallBoy, p)
    
    # 3. Iterating over polynomials of degree n
    # until one of them divides the bigBoy
    
    candidate = [0 for _ in range(n + 1)]
    candidate[n] = 1

    _, r = polynomialPrimeDivision(bigBoy, candidate, p)
    
    while max(r) != 0: # while the remainder isn't 0
        candidate[0] += 1
        for i in range(n):
            if candidate[i] == p:
                candidate[i] = 0
                candidate[i+1] += 1
        _, r = polynomialPrimeDivision(bigBoy, candidate, p)
    return candidate

class fieldInt:
    def __init__(self, value : int, p : int, n : int, irreduciblePol = None):
        self.value = value % (p ** n)
        self.primeBase = p
        self.primePower = n
        self.fieldSize = p ** n
        polinomialValue = [value % p]
        for i in range(1, n):
            value -= polinomialValue[i-1]
            value = value // p
            polinomialValue.append(value % p)
        self.polValue = polinomialValue
        if irreduciblePol is not None:
            self.prodPol = irreduciblePol
        else:
            if n == 1:
                self.prodPol = [0, 1]
            else:
                self.prodPol = irreduciblePolynomialFinder(p, n)

    def __str__(self):
        t = str(self.value) + " del campo F" + str(self.fieldSize) + '\n'
        t += ' + '.join([str(v) + "x^" + str(i) for i, v in enumerate(self.polValue)])
        t += '\n'
        return t

    def __bool__(self):
        return bool(self.value)
    
    def __int__(self):
        return self.value
    
    def __add__(self, other):
        if not self.fieldSize == other.fieldSize:
            return "Error, no se pueden sumar enteros de campos diferentes"
        sumPolynomial = [(self.polValue[i] + other.polValue[i]) % self.primeBase for i in range(self.primePower)]
        sumValue = 0
        for i in range(self.primePower):
            sumValue += sumPolynomial[i] * self.primeBase ** i
        return fieldInt(sumValue, self.primeBase, self.primePower, self.prodPol)

    def __mul__(self, other):
        if not self.fieldSize == other.fieldSize:
            return "Error, no se pueden multiplicar enteros de campos diferentes"
        prodPolynomial = polynomialPrimeProduct(self.polValue, other.polValue, self.primeBase)
        _, prodPolynomial = polynomialPrimeDivision(prodPolynomial, self.prodPol, self.primeBase)
        prodValue = 0
        for i in range(self.primePower):
            prodValue += prodPolynomial[i] * self.primeBase ** i
        return fieldInt(prodValue, self.primeBase, self.primePower, self.prodPol)

    def __neg__(self):
        negSelfPolynomial = list(map(lambda x: (self.primeBase - x) % self.primeBase, self.polValue))
        negSelfValue = 0
        for i in range(self.primePower):
            negSelfValue += negSelfPolynomial[i] * self.primeBase ** i
        return fieldInt(negSelfValue, self.primeBase, self.primePower, self.prodPol)

    def __sub__(self, other):
        if not self.fieldSize == other.fieldSize:
            return "Error, no se pueden restar enteros de campos diferentes"
        return self + (- other)

    def __floordiv__(self, other):
        if not self.fieldSize == other.fieldSize:
            return "Error, no se pueden restar enteros de campos diferentes"
        inverseOther = fieldInt(1, other.primeBase, other.primePower)
        while (inverseOther * other).value != 1:
            inverseOther = inverseOther * other
        return self * inverseOther
        

def main():
    a = fieldInt(4, 3, 3)
    b = fieldInt(5, 3, 3)
    c = fieldInt(13, 3, 3)
    x = (a * b) + c
    y = (x - c) * a # (((a * b) + c) - c) * a = a * b * a
    z = y // (b * a) # a * b * a // (b * a) = a
    # print(a, b, c, x, y, z)

    """
    prime = 11
    power = 2

    for i in range(prime ** power):
        v = fieldInt(i, prime, power)
        prod = fieldInt(1, prime, power)
        for j in range(prime):
            prod = prod * v
        print(v, prod)
    """

    i = fieldInt(74, 2, 8)
    print(i)
    

if __name__ == "__main__":
    main()
