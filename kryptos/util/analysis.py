import pandas as pd
from collections import Counter
import string
import re
import math
from constants import RES_PATH

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
    string = filterAlphabet(string, alphabet)
    return calculateIC(string[::sliceSize], ignore_case, alphabet)



def icForSliceSizes(string, max=10, ignore_case=True, alphabet=string.ascii_lowercase):
    if (ignore_case):
        string = string.lower()
    string = filterAlphabet(string, alphabet)
    ics = {}
    for sliceSize in range(max + 1):
        if sliceSize == 0:
            continue
        ics[sliceSize] = sliceIC(string, sliceSize, ignore_case, alphabet)
    return ics

def filterAlphabet(filterString, alphabet):
    regex = re.compile('[^' + alphabet + ']')
    return regex.sub('', filterString)

def loadDict(file):
    d = {}
    with open(RES_PATH + file) as f:
        for line in f:
            (key, val) = line.split()
            d[key] = int(val)
    return d

def nGramFit(string, size):
    score = 0
    freqDict = {}
    if size == 1:
        freqDict = loadDict("english_monograms.txt")
    elif size == 2:
        freqDict = loadDict("english_bigrams.txt")
    elif size == 3:
        freqDict = loadDict("english_trigrams.txt")
    elif size == 4:
        freqDict = loadDict("english_quadgrams.txt")
    elif size == 5:
        freqDict = loadDict("english_quintgrams.txt")
    else:
        raise ValueError
    nGrams = nGramAnalysis(string, size)
    for k, v in nGrams.items():
        if k in freqDict:
            score += math.log(freqDict[k])
    return score


def nGramAnalysis(string, size):
    ngramCounts = {}
    len_string = len(string)
    string = string + string # padding the string
    for i in range(len_string):
        segment = string[i:i+size]
        if segment in ngramCounts:
            ngramCounts[segment] += 1
        else:
            ngramCounts[segment] = 1
    return dict(sorted(ngramCounts.items(), key=lambda x: x[1], reverse=True))