from pkg_resources import get_distribution

from .ordered_map import read, write


def _get_metadata(name: str) -> str:
    pkg = get_distribution(__package__)

    for line in pkg.get_metadata_lines(pkg.PKG_INFO):
        if line.startswith('{}: '.format(name)):
            return line.split(': ')[1]

    return ''


_copyright_notice = 'Copyright (c) {} <{}>'.format(
    _get_metadata('Author'), _get_metadata('Author-email'))

usage = [_get_metadata('Summary'), _copyright_notice]


def doc_split(func: callable) -> str:
    return func.__doc__.split('\n\n')[0]


def version(name: str) -> str:
    return '{} version {}\n\n{}\nHomepage: {}'.format(
        _get_metadata('Name'), _get_metadata('Version'), _copyright_notice,
        _get_metadata('Home-page'))
