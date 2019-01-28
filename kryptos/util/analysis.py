import pandas as pd
from collections import Counter

def __init__(self):
    pass

def frequencies(string, ignore_case=False):
    if (ignore_case):
        string = string.lower()
    return Counter(string)