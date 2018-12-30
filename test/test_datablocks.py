"""
Standalone code tests for checking basic boundaries and constraints and making
sure the bit-fiddly stuff works in 2 and 3
"""

from unittest import TestCase, main

import piplate_modbus.datablocks


# noinspection PyPep8Naming
class Test_DAQCPlateDIDataBlock(TestCase):
    def test_validate(self):
        d = piplate_modbus.datablocks.DAQCPlateDIDataBlock(0)

        self.assertTrue(d.validate(10001, 1))
        self.assertTrue(d.validate(10001, 7))
        self.assertTrue(d.validate(10008, 1))

        self.assertFalse(d.validate(10008, 2))
        self.assertFalse(d.validate(10000, 1))
        self.assertFalse(d.validate(10009, 1))


# noinspection PyPep8Naming
class Test_DAQCPlateCODataBlock(TestCase):
    def test_validate(self):
        d = piplate_modbus.datablocks.DACQPlateCODataBlock(0)

        self.assertTrue(d.validate(1, 1))
        self.assertTrue(d.validate(1, 7))
        self.assertTrue(d.validate(7, 1))

        self.assertFalse(d.validate(7, 2))
        self.assertFalse(d.validate(0, 1))
        self.assertFalse(d.validate(-1, 1))
        self.assertFalse(d.validate(8, 1))


# noinspection PyPep8Naming
class Test_DAQCPlateIRDataBlock(TestCase):
    def test_validate(self):
        d = piplate_modbus.datablocks.DACQPlateIRDataBlock(0)

        self.assertTrue(d.validate(30001, 2))
        self.assertTrue(d.validate(30008, 2))

        self.assertFalse(d.validate(30000, 2))
        self.assertFalse(d.validate(30009, 2))
        self.assertFalse(d.validate(30001, 4))
        self.assertFalse(d.validate(30001, 1))


# noinspection PyPep8Naming
class Test_DAQCPlateHRDataBlock(TestCase):
    def test_validate(self):
        d = piplate_modbus.datablocks.DACQPlateHRDataBlock(0)

        self.assertTrue(d.validate(40001, 2))
        self.assertTrue(d.validate(40002, 2))

        self.assertFalse(d.validate(40000, 2))
        self.assertFalse(d.validate(40003, 2))
        self.assertFalse(d.validate(40001, 4))
        self.assertFalse(d.validate(40001, 1))


# noinspection PyPep8Naming
class Test_DACQPlateRegisterDataBlock(TestCase):

    pack_float = staticmethod(
        piplate_modbus.datablocks._DACQPlateRegisterDataBlock._pack_float)
    unpack_float = staticmethod(
        piplate_modbus.datablocks._DACQPlateRegisterDataBlock._unpack_float)

    cases = [
        (69, (0, 0x428a)),
        (-69, (0, 0xc28a))
    ]

    def test__pack_float(self):
        for i, o in self.cases:
            self.assertEqual(self.pack_float(i), o)

    def test__unpack_float(self):
        for o, i in self.cases:
            self.assertEqual(self.unpack_float(i), o)


if __name__ == '__main__':
    main()


