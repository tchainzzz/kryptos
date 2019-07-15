import string
import re
import argparse

def __init__(self):
    pass

def encodeVigenere(msg, key, tabula=string.ascii_uppercase, ignore_whitespace=True):
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

def decodeVigenere(msg, key, tabula=string.ascii_uppercase):
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

def tabulaOf(key, prepend=True, basis=string.ascii_uppercase):
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

def decodeAndRotate(msg, key, tabula=string.ascii_uppercase):
    plaintexts = {}
    for i in range(len(key)):
        plaintexts[rotateKey(key, i)] = decodeVigenere(msg, rotateKey(key, i), tabula)
    return plaintexts

if __name__ == '__main__':
    psr = argparse.ArgumentParser()
    psr.add_argument('mode', metavar='mode', type=str, choices=['encode', 'decode'])
    psr.add_argument('text', metavar='text', type=str, action='store')
    psr.add_argument('key', metavar='key' , type=str, action='store')
    psr.add_argument('--tabula-of', type=str, action='store', default=None)
    psr.add_argument('--prepend-tabula-key', '--prepend',  action='store_true', default=True)
    psr.add_argument('--basis', type=str, action='store', default=string.ascii_uppercase)
    psr.add_argument('--ignore_ws', action='store_true', default=True)
    psr.add_argument('--iterative', '-i', action='store_true', default=False)
    args = psr.parse_args()
    args.text = args.text.upper()
    args.key = args.key.upper()
    if args.tabula_of is not None:
        args.tabula_of = args.tabula_of.upper()
        tbl = tabulaOf(args.tabula_of, prepend=args.prepend_tabula_key, basis=args.basis) 
    else:
        tbl = args.basis
    print("Pipeline: [TEXT={}] + [TABULA_STATE=(basis={}, tabula_seed={} ({}))] >> [TABULA={}] >> [({}) key={}]".format(
        args.text[:15] + '...' if len(args.text) > 10 else args.text,
        args.basis[:10] + '...' if len(args.basis) > 5 else args.basis,
        "DEFAULT" if args.tabula_of is None else (args.tabula_of[:8] + '...' if len(args.tabula_of) > 8 else args.tabula_of),
        "PRE" if args.prepend_tabula_key else "POST",
        tbl[:10] + '...' if len(tbl) > 10 else tbl,
        args.mode.upper(),
        args.key[:15] + '...' if len(args.key) > 10 else args.key 
        ))
    if args.mode is 'encode':
        print(encodeVigenere(args.text, args.key, tabula=tbl, ignore_whitespace=args.ignore_ws))
    else:
        if args.iterative:
            decodings = decodeAndRotate(args.text, args.key, tabula=tbl)
            for decoding_key, plaintext in decodings.items():
                print("KEY={}: PLAINTEXT={}".format(decoding_key, plaintext))
        else:
            print(decodeVigenere(args.text, args.key, tabula=tbl)) 
