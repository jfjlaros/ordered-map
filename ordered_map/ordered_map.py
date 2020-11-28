from collections import defaultdict


def deserialise(string):
    """Deserialise an ordered map string.

    :arg str string: An ordered map string.

    :returns dict: An ordered map.
    """
    if '.' not in string:
        key, value = string.split('=')

        return {key.strip(): value.strip()}

    head, tail = string.split('.', maxsplit=1)

    return {head: deserialise(tail)}


def serialise(data, prefix=''):
    """Serialise an ordered map.

    :arg dict data: An ordered map.
    :arg str prefix: Partially serialised result.

    :returns str: An ordered map string.
    """
    if not isinstance(data, dict):
        return '{}={}\n'.format(prefix, data)

    result = ''
    for key in sorted(data):
        if prefix:
            result += serialise(data[key], '{}.{}'.format(prefix, key))
        else:
            result += serialise(data[key], key)

    return result


def merge(d1, d2):
    """Merge two dictionaries.

    :arg dict d1: Dictionary 1.
    :arg dict d2: Dictionary 2.

    :returns dict: Merged dictionary.
    """
    result = {}
    for key in set(d1.keys()) | set(d2.keys()):
        if key in d1:
            if key in d2:
                result[key] = merge(d1[key], d2[key])
            else:
                result[key] = d1[key]
        else:
            result[key] = d2[key]

    return result


def parse(handle):
    """Parse an ordered map file.

    :arg stream handle: Open readable handle to an ordered map file.

    :returns dict: An ordered map.
    """
    data = {}
    for line in handle.readlines():
        if line[0] not in ('#', ' ', '\t', '\n', '\r'):
            data = merge(data, deserialise(line))

    return data


def write(handle, data):
    """Write an odered map to a file.

    :arg stream handle: Open writeable handle to an ordered map file.
    :arg dict data: An ordered map.
    """
    for key in sorted(data):
        handle.write('{}\n'.format(62 * '#'))
        handle.write(serialise(data[key], key))
