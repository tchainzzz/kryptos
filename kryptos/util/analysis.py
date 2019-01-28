import pandas as pd
from collections import Counter
from . import constants

def __init__(self):
    pass

def frequencies(string, ignore_case=False, alphabet=constants.ALPHABET_ENGLISH):
    if (ignore_case):
        string = string.lower()
    counter = Counter()
    for c in string:
        if c in alphabet:
            counter[c] += 1
    return counter