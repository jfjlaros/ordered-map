Library
=======

The API library provides the ``read`` and ``write`` functions.

.. code::

    >>> from ordered_map import read, write

The ``read`` function reads an ordered map file and returns a nested
dictionary.

.. code::

    >>> data = read(open('boards.txt'))
    >>> data['FTDI_PID_6001']['vid'][0]
    '0x0403'

The ``write`` function writes a nested dictionary to an ordered map file.

.. code::

    >>> write(open('boards.txt', 'w'), data)
