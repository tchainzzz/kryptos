import pytest
from .context import kryptos
import string

import kryptos.util.analysis as analysis

class TestSanity:
    def test_frequencySanity(self):
        c = analysis.frequencies("Hello world!")
        assert c["h"] == 1
        assert c["e"] == 1
        assert c["l"] == 3
        assert c["o"] == 2
        assert c["w"] == 1
        assert c["r"] == 1
        assert c["d"] == 1
        assert c["!"] == 0
        assert len(c) == 7

    def test_frequencyIgnoreCase(self):
        c = analysis.frequencies("HhHh", False, string.ascii_letters)
        assert c["H"] == 2
        assert c["h"] == 2
        assert len(c) == 2

    def test_nonsenseString(self):
        c = analysis.frequencies("12351p-~~! p")
        assert c["p"] == 2
        assert len(c) == 1
        assert len(list(c)) == 1




