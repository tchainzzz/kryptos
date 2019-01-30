import string
import re

def __init__(self):
    pass

def encodeVigenere(msg, key, tabula=string.ascii_lowercase, ignore_whitespace=True):
    if ignore_whitespace:
        msg = msg.replace(" ", "")
    encoded = list(msg)
    meaningfulIndex = 0
    for i in range(len(msg)):
        try:
            indexOfChar = tabula.index(msg[i])
            indexOfKeyChar = tabula.index(key[meaningfulIndex % len(key)])
            targetIndex = (indexOfChar + indexOfKeyChar) % len(tabula)
            encoded[i] = tabula[targetIndex]
            meaningfulIndex += 1
        except ValueError:
            encoded[i] = msg[i]
    return ''.join(encoded)

def decodeVigenere(msg, key, tabula=string.ascii_lowercase):
    decoded = list(msg)
    meaningfulIndex = 0
    for i in range(len(msg)):
        try:
            indexOfChar = tabula.index(msg[i])
            indexOfKeyChar = tabula.index(key[meaningfulIndex % len(key)])
            targetIndex = (indexOfChar - indexOfKeyChar + len(tabula)) % len(tabula)
            decoded[i] = tabula[targetIndex] 
            meaningfulIndex += 1
        except ValueError:
            decoded[i] = msg[i]
    return ''.join(decoded)

def tabulaOf(key, prepend=True, basis=string.ascii_lowercase):
    # used for encoding Kryptos!
    alphabetSubstring = tableauFilter(key, basis)
    if prepend:
        return key + alphabetSubstring
    else:
        return alphabetSubstring + key

def tableauFilter(key, alphabet):
    regex = re.compile('[' + key + ']')
    return regex.sub('', alphabet)

def rotateKey(key, rotation):
    return key[rotation:] + key[:rotation]

def decodeAndRotate(msg, key, tabula=string.ascii_lowercase):
    plaintexts = {}
    for i in range(len(key)):
        plaintexts[rotateKey(key, i)] = decodeVigenere(msg, rotateKey(key, i), tabula)
    return plaintexts