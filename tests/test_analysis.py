import pytest
from .context import kryptos

import kryptos.util.analysis as analysis

class TestSanity:
    def test_frequencySanity(self):
        c = analysis.frequencies("Hello world!")
        assert c["H"] == 1
        assert c["e"] == 1
        assert c["l"] == 3
        assert c["o"] == 2
        assert c["w"] == 1
        assert c["r"] == 1
        assert c["d"] == 1

