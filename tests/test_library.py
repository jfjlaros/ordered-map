"""Tests for the ordered-map library."""
from ordered_map.ordered_map import (
    _deserialise, _from_list, _merge, _serialise, _to_list)
from ordered_map import read, write


def test_deserialise() -> None:
    assert _deserialise('a.b=c\n') == {'a': {'b': 'c'}}
    assert _deserialise('a.b=c') == {'a': {'b': 'c'}}
    assert _deserialise('a.b = c') == {'a': {'b': 'c'}}
    assert _deserialise('a.b.c=d') == {'a': {'b': {'c': 'd'}}}


def test_serialise() -> None:
    assert _serialise({'a': {'b': 'c'}}) == 'a.b=c\n'
    assert _serialise({'a': {'b': {'c': 'd'}}}) == 'a.b.c=d\n'


def test_merge() -> None:
    assert _merge({'a': 'b'}, {'x': 'y'}) == {'a': 'b', 'x': 'y'}
    assert _merge({'a': 'b'}, {'a': 'y'}) == {'a': {'b', 'y'}}
    assert _merge({'a': {'b': 'c'}}, {'a': {'y': 'z'}}) == {
        'a': {'b': 'c', 'y': 'z'}}
    assert _merge({'a': {'b': 'c'}}, {'a': {'b': 'z'}}) == {
        'a': {'b': {'c', 'z'}}}


def test_to_list() -> None:
    assert _to_list({'0': 'a'}) == ['a']
    assert _to_list({'1': 'a'}) == {'1': 'a'}
    assert _to_list({'0': 'a', '1': 'b'}) == ['a', 'b']
    assert _to_list({'1': 'a', '0': 'b'}) == ['b', 'a']
    assert _to_list({'0': 'a', '2': 'b'}) == {'0': 'a', '2': 'b'}
    assert _to_list({'a': {'0', '1'}}) == {'a': {'0', '1'}}
    assert _to_list({'a': {'0': 'x', '1': 'y'}}) == {'a': ['x', 'y']}
    assert _to_list({'0': {'a': 'b'}, '1': {'x': 'y'}}) == [
        {'a': 'b'}, {'x': 'y'}]


def test_from_list() -> None:
    assert _from_list(['a']) == {'0': 'a'}
    assert _from_list({'1': 'a'}) == {'1': 'a'}
    assert _from_list(['a', 'b']) == {'0': 'a', '1': 'b'}
    assert _from_list(['b', 'a']) == {'1': 'a', '0': 'b'}
    assert _from_list({'0': 'a', '2': 'b'}) == {'0': 'a', '2': 'b'}
    assert _from_list({'a': {'0', '1'}}) == {'a': {'0', '1'}}
    assert _from_list({'a': ['x', 'y']}) == {'a': {'0': 'x', '1': 'y'}}
    assert _from_list([{'a': 'b'}, {'x': 'y'}]) == {
        '0': {'a': 'b'}, '1': {'x': 'y'}}


def test_read_skip() -> None:
    assert read('') == []
    assert read('\n') == []
    assert read('\r') == []
    assert read('# Comment.') == []
    assert read(' a=b') == []
    assert read('\ta=b') == []


def test_read_single() -> None:
    assert read('a=b') == {'a': 'b'}


def test_read_multi() -> None:
    assert read('a=b\nx=y') == {'a': 'b', 'x': 'y'}


def test_write_skip() -> None:
    assert write({}) == ''
    assert write([]) == ''


def test_write_single() -> None:
    assert write({'a': 'b'}) == '{}\na=b\n'.format(62 * '#')


def test_write_multi() -> None:
    assert write({'a': 'b', 'x': 'y'}) == '{}\na=b\n{}\nx=y\n'.format(
        62 * '#', 62 * '#')
