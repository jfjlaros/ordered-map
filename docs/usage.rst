Usage
=====

The command line interface can be used for converting an ordered map to a YAML
file or vice versa. It currently has two subcommands: ``read`` and ``write``.
Use the ``-h`` option for more information.

::

    ordered_map -h


Reading ordered maps
--------------------

The ``read`` subcommand is used for reading an ordered map and converting it to
YAML.

::

    ordered_map read boards.txt boards.yml


Writing ordered maps
--------------------

The ``write`` subcommand is used for reading a YAML file and converting it to
an ordered map.

::

    ordered_map write boards.yml boards.txt
