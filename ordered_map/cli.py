from argparse import ArgumentParser, FileType, RawDescriptionHelpFormatter
from yaml import safe_dump, safe_load

from . import doc_split, usage, version, read as om_read, write as om_write


def read(input_handle: object, output_handle: object) -> None:
    """Convert an ordered map file to a YAML file.

    :args stream input_handle: Input file in ordered map format.
    :args stream output_handle: Output file in YAML format.
    """
    safe_dump(
        om_read(input_handle.read()), output_handle, width=76,
        default_flow_style=False)


def write(input_handle: object, output_handle: object) -> None:
    """Convert a YAML file to an ordered map file.

    :args stream input_handle: Intput file in YAML format.
    :args stream output_handle: Output file in ordered map format.
    """
    output_handle.write(om_write(safe_load(input_handle)))


def _arg_parser() -> object:
    """Command line argument parsing."""
    files_parser = ArgumentParser(add_help=False)
    files_parser.add_argument(
        'input_handle', metavar='INPUT', type=FileType('r'),
        help='input file')
    files_parser.add_argument(
        'output_handle', metavar='OUTPUT', type=FileType('w'),
        help='output file')

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument('-v', action='version', version=version(parser.prog))
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    read_parser = subparsers.add_parser(
        'read', parents=[files_parser], description=doc_split(read))
    read_parser.set_defaults(func=read)

    write_parser = subparsers.add_parser(
        'write', parents=[files_parser], description=doc_split(write))
    write_parser.set_defaults(func=write)

    return parser


def main() -> None:
    """Main entry point."""
    parser = _arg_parser()

    try:
        args = parser.parse_args()
    except IOError as error:
        parser.error(error)

    try:
        args.func(
            **{k: v for k, v in vars(args).items()
               if k not in ('func', 'subcommand')})
    except (ValueError, IOError) as error:
        parser.error(error)
