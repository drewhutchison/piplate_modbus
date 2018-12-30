import logging
import struct
import sys

# this is the stupidest shit... in test context, we don't want to blow up
# importing piplates because we don't have spidev, but there's not a
# reasonable way to mock side-effectful imports that works in python 2, and
# checking python 2 compatibility is the entire point of the tests.
# So do this instead and may God have mercy on our souls.
try:
    # noinspection PyPep8Naming
    import piplates.DAQCplate as dp
except Exception as e:
    if 'unittest' not in sys.modules:
        raise e

from pymodbus.datastore.store import BaseModbusDataBlock

_LOG = logging.getLogger(__name__)


class _BaseDataBlock(BaseModbusDataBlock):

    @property
    def _address_offset(self):
        raise NotImplementedError()

    @property
    def default_value(self):
        raise NotImplementedError()

    @property
    def values(self):
        return None

    @property
    def _pincount(self):
        raise NotImplementedError()

    def __init__(self, board_address):
        self._board_address = board_address

    def validate(self, address, count=1):
        self.log('validating {}, {} for {}'.format(
            address, count, self.__class__.__name__
        ))
        caddress = self.corrected_address(address)
        return caddress >= 0 and caddress + count <= self._pincount

    def setValues(self, address, values):
        raise ValueError('{} is read-only'.format(self.__class__.__name__))

    def getValues(self, address, count=1):
        pass

    @classmethod
    def corrected_address(cls, address):
        return address - cls._address_offset

    def log(self, msg):
        _LOG.debug('Board {}: {}'.format(self._board_address, msg))


class DAQCPlateDIDataBlock(_BaseDataBlock):

    _pincount = 8
    _address_offset = 10001
    default_value = False

    @property
    def values(self):
        inport = dp.getDINall(self._board_address)
        return [bool((inport >> i) & 1) for i in range(self._pincount)]

    def getValues(self, address, count=1):
        caddress = self.corrected_address(address)
        values = self.values[caddress: caddress+count]
        self.log('read {} from {}..{}'.format(
            values, caddress, caddress+count
        ))
        return values


class DACQPlateCODataBlock(_BaseDataBlock):

    _pincount = 7
    _address_offset = 1
    default_value = False

    @property
    def values(self):
        # getDOUTbyte returns a list with one int in it for some dumbass reason
        outport = dp.getDOUTbyte(self._board_address)[0]
        return [bool((outport >> i) & 1) for i in range(self._pincount)]

    def getValues(self, address, count=1):
        caddress = self.corrected_address(address)
        values = self.values[caddress: caddress+count]
        self.log('Read {} from {}..{}'.format(
            values, caddress, caddress+count))
        return values

    def setValues(self, address, values):
        caddress = self.corrected_address(address)
        for i, value in enumerate(values):
            bit_addr = caddress + i
            self.log('writing {} to {}'.format(value, bit_addr))
            if value:
                dp.setDOUTbit(self._board_address, bit_addr)
            else:
                dp.clrDOUTbit(self._board_address, bit_addr)


class _DACQPlateRegisterDataBlock(_BaseDataBlock):

    @property
    def _pincount(self):
        raise NotImplementedError()

    @property
    def _address_offset(self):
        raise NotImplementedError()

    default_value = [0, 0]

    def validate(self, address, count=1):
        self.log('validating {}, {} for {}'.format(
            address, count, self.__class__.__name__
        ))
        # the count should be 2 for a float32
        return (0 <= self.corrected_address(address) < self._pincount
                and count == 2)

    @staticmethod
    def _pack_float(f):
        return struct.unpack('<HH', struct.pack('<f', f))

    @staticmethod
    def _unpack_float(l):
        return struct.unpack('<f', struct.pack('<HH', *l))[0]


class DACQPlateHRDataBlock(_DACQPlateRegisterDataBlock):

    _pincount = 2
    _address_offset = 40001

    def getValues(self, address, count=1):
        caddress = self.corrected_address(address)
        value = dp.getDAC(self._board_address, caddress)
        self.log('read {} from board {} output {}'.format(
            value, self._board_address, caddress))
        return self._pack_float(value)

    def setValues(self, address, values):
        caddress = self.corrected_address(address)
        value = self._unpack_float(values)
        self.log('writing {} to board {} output {}'.format(
            value, self._board_address, caddress))
        dp.setDAC(self._board_address, caddress, value)


class DACQPlateIRDataBlock(_DACQPlateRegisterDataBlock):

    _pincount = 8
    _address_offset = 30001

    def getValues(self, address, count=1):
        caddress = self.corrected_address(address)
        value = dp.getADC(self._board_address, caddress)
        self.log('read {} from board {} input {}'.format(
            value, self._board_address, caddress))
        return self._pack_float(value)
