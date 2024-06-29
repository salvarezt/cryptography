from FiniteFieldRepresentation import fieldInt
from random import randint
from random import random

def encodingText(text : str):
    """
    Encodes an english text (including spaces) into an array of
    integers from the field F27
    """
    text = text.upper()
    code = []
    for symbol in text:
        if symbol == ' ':
            code.append(fieldInt(0, 3, 3))
            continue
        code.append(fieldInt(ord(symbol) - ord('A') + 1, 3, 3))  
    return code

def decodingText(fieldIntList) -> str:
    """
    Decides an array of integers from the field F27
    into an english text
    """

    text = ''
    for i in fieldIntList:
        if i.value == 0:
            text += " "
            continue
        text += chr(ord('A') + i.value - 1)

    return text

def noisyChannel(fieldIntList, noError = 2/3):
    """
    Simulates a noisy channel where the
    probability of not changing a particular
    symbol is given by noError
    """

    newFieldIntList = []
    for i in fieldIntList:
        if random() <= noError:
            newFieldIntList.append(i)
            continue
        noise = fieldInt(randint(1, 26), 3, 3)
        newFieldIntList.append(i + noise)

    return newFieldIntList
    

def main():
    t = "Este es un mensaje que quise enviar hace mucho tiempo"
    code = encodingText(t)
    noisyCode = noisyChannel(code, 0.9)
    print("Mensaje a enviar:", decodingText(code))
    print("Mensaje recibido:", decodingText(noisyCode))

if __name__ == "__main__":
    main()
