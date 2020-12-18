"""Tests for the ordered-map CLI."""
from io import StringIO

from ordered_map.cli import read, write


def test_read() -> None:
    s = StringIO()
    read(StringIO('a=b'), s)
    assert s.getvalue() == 'a: b\n'


def test_write() -> None:
    s = StringIO()
    write(StringIO('a: b'), s)
    assert s.getvalue() == '{}\na=b\n'.format(62 * '#')
