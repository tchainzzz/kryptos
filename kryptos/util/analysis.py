import pandas as pd
from collections import Counter
import string
import re

def __init__(self):
    pass

def frequencies(string, ignore_case=True, alphabet=string.ascii_lowercase):
    if (ignore_case):
        string = string.lower()
    counter = Counter()
    for c in string:
        if c in alphabet:
            counter[c] += 1
    return counter

def calculateIC(string, ignore_case=True, alphabet=string.ascii_lowercase):
    if (ignore_case):
        string = string.lower()
    counter = frequencies(string, ignore_case, alphabet)
    ic = 0
    n_chars = 0
    for k in counter:
        ic += counter[k] * (counter[k] - 1)
        n_chars += counter[k]
    return ic / (n_chars * (n_chars-1))

def sliceIC(string, sliceSize, ignore_case=True, alphabet=string.ascii_lowercase):
    if (ignore_case):
        string = string.lower()
    string = filter(string, alphabet)
    return calculateIC(string[::sliceSize], ignore_case, alphabet)


def icForSliceSizes(string, max=10, ignore_case=True, alphabet=string.ascii_lowercase):
    if (ignore_case):
        string = string.lower()
    string = filter(string, alphabet)
    ics = {}
    for sliceSize in range(max + 1):
        if sliceSize == 0:
            continue
        ics[sliceSize] = sliceIC(string, sliceSize, ignore_case, alphabet)
    return ics

def filter(string, alphabet):
    regex = re.compile('[^' + alphabet + ']')
    return regex.sub('', string)


