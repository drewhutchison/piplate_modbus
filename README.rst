##############
piplate_modbus
##############

This is a shim layer that allows for remote control and sensing of the
`pi-plates <https://pi-plates.com/>`_
`DAQCplate <https://pi-plates.com/daqcr1/>`_
by MODBUS via the
`PyModbus <https://github.com/riptideio/pymodbus>`_
library.

**********************
Installation and usage
**********************

With setuptools installed, run

  python setup.py install

to install, after which you'll have access to the piplate_modbus module.

Example usage is provided in ``main.py`` in the project root directory, which
can be run with optional ``host`` and ``port`` arguments to set up a modbus
TCP server.

After that, ``pymodbus.console tcp --host <host>`` should connect you to the
server, as verified by its ``client.connect`` returning true.

Advanced usage
==============

This module defines the interface within a pymodbus ``ModbusSlaveContext``,
which could theoretically be used to implement a serial RTU or any of the other
server types provided by PyModbus.
I haven't tested this but, honestly, if you're to the point of trying stuff
like that you probably don't need this module anyway.

Note that board communications are (probably at least supposed to be) blocking
on the GPIO and SPI bus, so implementing an async server is a futile if not
an actively bad idea.

**********
MODBUS map
**********

DAQC plates will be assigned to the unit id corresponding to the settings of
their address jumpers.
Multiple devices should work, though this is untested.
Out of the box, a DAQCplate will correspond to unit id 0.

Each board will implement the following table for its unit id:

+----------+--------+--------+---------+---------------------+
| Address  | Access | Length | Format  |        PHY          |
+==========+========+========+=========+=====================+
| 00000..6 |    R/W |      - | bit     | Digital out 0..6    |
+----------+--------+--------+---------+---------------------+
| 10000..7 |     RO |      - | bit     | Digital in 0..7     |
+----------+--------+--------+---------+---------------------+
| 30000..7 |     RO |      2 | Float32 | Analog in 0..7      |
+----------+--------+--------+---------+---------------------+
| 40000..1 |    R/W |      2 | Float32 | Analog/PWM out 0..1 |
+----------+--------+--------+---------+---------------------+

Analog values are passed in IEEE-754 single-precision format in (1-0-3-2)
byteorder.
Behavior is undefined when reading/writing a count other than 2 on these
registers.
These values represent the actual voltage present on the terminal as determined
by the piplate driver.

A note on addressing
====================

Since modbus addressing is the land of OBOEs and since pymodbus seems to
implement some internal magic whereby there's 1 added to the address upon
packet encoding and subtracted on decoding, I've picked a numbering scheme that
seemed minimally stupid.
Careful readers will note that this munges the tests for the ``validate``
method, which seem to be called at a point where the above-noted magic 1 is
in effect.

If you're at any point of confusion as to why addressing isn't working the way
you expect, please enable logging at the DEBUG level, which will show the raw
pin number being called with all read/writes.

****
Test
****

There are a few unit tests included to validate the address fuckery noted
above, as well as to make sure the small amounts of bitwrangling work as
intended in both 2 and 3.
``python setup.py test`` to run them.

***********
Future work
***********

The piplate driver is pretty garbage by modern python standards, but, barring
a ground-up reimplementation of that, here's a list of potential future
enhancements.

- Byteorder is hardcoded to (1-0-3-2) right now, since that's the default on
  `Pyscada <https://github.com/trombastic/PyScada>`_,
  which is my application.
  However, it wouldn't be difficult to implement other byteorders, and I might
  do so if this is useful for someone.
- The PWM functions take an int in [0..1023], but right now this is munged by
  calls to ``setDAC``.
  Implementing native registers for the raw PWM values might be worthwhile.
- We're not doing anything with the LED... this could be brought in as a
  register, or at least blinked to indicate active and fault conditions.
- I've only played with the DAQCplate, but something like this is presumably
  possible for the other piplates products.