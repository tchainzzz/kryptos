import pandas as pd
from collections import Counter, OrderedDict, defaultdict
import string
import re
import math
import operator
import scipy.stats

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

#########################
#
#    ADVANCED STATS
#
#########################

def chi2_test(sample_text, true_pmf, keep=string.ascii_uppercase, freq_order=True, laplace=1):
    # accepts two dictionaries in the form of (letter, frequency).
    # for english frequencies, load english_monograms.txt into a dict and run it through dictToPMF to get a valid pmf.
    sample_text = re.sub('[^'+keep+']','',sample_text.upper())
    freqs = Counter(sample_text)
    for key in true_pmf.keys():
        freqs[key] += laplace
    if freq_order:
        text_pmf = dict(sorted(dictToPMF(freqs).items(), key=operator.itemgetter(1), reverse=True))
    else:
        text_pmf = dict(sorted(dictToPMF(freqs).items(), key=lambda kv: list(true_pmf.keys()).index(kv[0]), reverse=False))
    # print("observations:", text_pmf, "sum =", sum(text_pmf.values()))
    # print("expected:", true_pmf, "sum =", sum(true_pmf.values()))
    text_copy = dict()
    true_copy = dict()
    # pseudo smoothing - multiply all the relative counts by 50
    for key in text_pmf.keys(): text_copy[key] = text_pmf[key] * len(sample_text)
    for key in true_pmf.keys(): true_copy[key] = true_pmf[key] * len(sample_text)
    under_five = len([_ for val in text_pmf.values() if val < 5])
    if under_five != 0:
        print("WARNING: {} observations with frequency < 5. This test may not be reliable.".format(under_five))
    chisq, p = scipy.stats.chisquare([val for _, val in text_copy.items()],  
            [val for _, val in true_copy.items()]
            , ddof=0)
    print("Chi-statistic:", chisq)
    print("p-value:", p)

#########################
#
#    DATA PROCESSING
#
#########################

def loadDict(filepath):
    d = {}
    with open(filepath) as f:
        for line in f:
            key, val = line.split()
            d[key] = int(val)
    return OrderedDict(sorted(d.items(), key=operator.itemgetter(1)))

def dictToPMF(d):
    factor=1.0/math.fsum(d.values())
    for k in d:
        d[k] = d[k]*factor
    # for extra safety, ENSURE that everything sums up to 1
    key_for_max = max(d.items(), key=operator.itemgetter(1))[0]
    diff = 1.0 - math.fsum(d.values())
    d[key_for_max] += diff
    return OrderedDict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))

def dictToCMF(d):
    assert(abs( 1 - sum(d.values())) < 0.00001)
    d = OrderedDict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))
    cum_sum = 0
    for k in d.keys():
        temp = d[k]
        d[k] += cum_sum
        cum_sum += temp
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
