from random import randint as rint
from primetest import modinv, modexp, generatePrimes

def findGenerator(p : int):
    """
    Encuentra un generador del grupo multiplicativo
    de Zp.
    """
    g = rint(2, p - 2)
    while modexp(g, (p - 1) // 2, p) == 1 or modexp(g, 2, p) == 1:
        g = rint(2, p - 2)
    return g

def genkeyElGamal(p : int, g = 0):
    """
    Genera una pareja de clave privada / clave publica en ElGamal
    usando de grupo base el grupo multiplicativo de Zp.
    """
    if g == 0:
        g = findGenerator(p)
    a = rint(2, p - 2)
    A = modexp(g, a, p)
    return (g, a, A)

def signatureElGamal(m : int, p : int, g = 0):
    """
    Dado el mensaje m (entero) y el primo p,
    calcula la firma digital del mensaje m
    en el sistema ElGamal.
    Retorna:
        El generador usado g.
        La clave publica principal A
        La clave para generar la firma B
        El mensaje m
        La firma digital Sabm.
    """
    if g == 0:
        g = findGenerator(p)
    _, a, A = genkeyElGamal(p, g)
    _, b, B = genkeyElGamal(p, g)
    while modinv(b, p - 1) == 0:
        _, b, B = genkeyElGamal(p, g)
    B_ = B % (p - 1)
    sub = a * B_
    q = sub // (p - 1)
    sub = - sub
    sub = q * (p - 1) + sub
    while sub < 0:
        sub += p - 1
    Sabm = modinv(b, p - 1) * (m + sub)
    Sabm = Sabm % (p - 1)
    return (g, A, B, m, Sabm)

def verifySignatureElGamal(g, A, B, m, S, p : int):
    """
    Dados los outputs de "signatureElGamal" y el primo p,
    verifica si la firma dada es correcta.
    Retorna
        True si la firma dada es valida
        False de lo contrario
    """
    g1 = modexp(g, m, p)
    B_ = B % (p - 1)
    g2 = (modexp(A, B_, p) * modexp(B, S, p)) % p
    return (g1 == g2)
