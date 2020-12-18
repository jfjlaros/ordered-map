def _deserialise(string):
    """Deserialise an ordered map string.

    :arg str string: An ordered map string.

    :returns dict: An ordered map.
    """
    if '.' not in string.split('=')[0]:
        key, value = string.split('=', maxsplit=1)
        return {key.strip(): value.strip()}

    head, tail = string.split('.', maxsplit=1)
    return {head: _deserialise(tail)}


def _serialise(data, prefix=''):
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
            if key != '_':
                result += _serialise(data[key], '{}.{}'.format(prefix, key))
            else:
                result += _serialise(data[key], prefix)
        else:
            result += _serialise(data[key], key)
    return result


def _merge(d1, d2):
    """Merge two dictionaries.

    :arg dict d1: Dictionary 1.
    :arg dict d2: Dictionary 2.

    :returns dict: Merged dictionary.
    """
    if not isinstance(d1, dict) and not isinstance(d2, dict):
        return {d1, d2}

    _d1, _d2 = d1, d2
    if not isinstance(d1, dict):
        _d1 = {'_': d1}
    if not isinstance(d2, dict):
        _d2 = {'_': d2}

    result = {}
    for key in set(_d1.keys()) | set(_d2.keys()):
        if key in _d1:
            if key in _d2:
                result[key] = _merge(_d1[key], _d2[key])
            else:
                result[key] = _d1[key]
        else:
            result[key] = _d2[key]
    return result


def _to_list(data):
    """Convert indexed dictionaries to lists.

    :arg dict data: An ordered map.

    :returns dict: An ordered map.
    """
    if not isinstance(data, dict):
        return data

    if (
            all(map(lambda x: x.isdigit(), data)) and
            sorted(map(int, data)) == list(range(len(data)))):
        return [_to_list(data[i]) for i in sorted(data)]
    return dict([(key, _to_list(data[key])) for key in data])


def _from_list(data):
    """Convert lists to indexed dictionaries.

    :arg dict data: An ordered map.

    :returns dict: An ordered map.
    """
    if isinstance(data, list):
        return dict([(str(i), _from_list(v)) for i, v in enumerate(data)])
    if isinstance(data, dict):
        return dict([(key, _from_list(data[key])) for key in data])
    return data


def read(string):
    """Parse an ordered map file.

    :arg str string: Content of an ordered map file.

    :returns dict: An ordered map.
    """
    data = {}
    for line in string.split('\n'):
        if line and line[0] not in ('#', ' ', '\t', '\r'):
            data = _merge(data, _deserialise(line))
    return _to_list(data)


def write(data):
    """Write an odered map to a file.

    :arg dict data: An ordered map.

    :returns str: Content of an ordered map file.
    """
    _data = _from_list(data)

    string = ''
    for key in sorted(_data):
        string += '{}\n{}'.format(62 * '#', _serialise(_data[key], key))
    return string
