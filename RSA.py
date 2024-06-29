from primetest import modexp, generatePrimes, inv_mod
def encode(msg):
    """
    Encodes a text message msg including spaces.
    """
    text = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    msg = msg.upper()
    block = []
    for char in msg:
        block.append(text.index(char))
    return block

def decode(block):
    """
    Encodes a text message msg including spaces.
    """
    text = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    msg = ''
    for number in block:
        msg += text[number]
    return msg

def RSAencode(block, blocksize = 420):
    numbers = [0]
    index = 0
    for i in range(len(block)):
        numbers[index] += block[i] * 27 ** (i % blocksize)
        if i % blocksize == 0 and i != 0:
            index += 1
            numbers.append(0)
    return numbers

def RSAdecode(block, blocksize = 420):
    numbers = []
    for i in block:
        for j in range(blocksize):
            numbers.append(i % 27)
            i = i // 27
    return numbers

def RSAencrypt(msg, N, e, blocksize = 420):
    encodedblock = RSAencode(encode(msg), blocksize)
    encrypt = []
    for number in encodedblock:
        encrypt.append(modexp(number, e, N))
    return encrypt

def RSAdecrypt(encodedblock, N, e, p, q, blocksize=420):
    d = inv_mod(e, (p - 1) * (q - 1))
    decrypt = []
    for number in encodedblock:
        decrypt.append(modexp(number, d, N))
    return decode(RSAdecode(decrypt, blocksize))
