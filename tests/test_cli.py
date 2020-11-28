"""Tests for the ordered-map CLI."""
from io import StringIO

from ordered_map import ordered_map

from shared import md5_check


class TestCLI(object):
    def setup(self):
        self._output = StringIO()

    def _md5_check(self, md5sum):
        return md5_check(self._output.getvalue(), md5sum)

    def test_1(self):
        pass
