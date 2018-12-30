from piplates import DAQCplate as dp
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.device import ModbusDeviceIdentification

from piplate_modbus import VERSION
from piplate_modbus.datablocks import (
    DAQCPlateDIDataBlock, DACQPlateCODataBlock, DACQPlateHRDataBlock,
    DACQPlateIRDataBlock)


class DAQCPlateIdentification(ModbusDeviceIdentification):
    def __init__(self):
        super(DAQCPlateIdentification, self).__init__({
            'VendorName': 'piplate_modbus',
            'VendorURL': 'https://github.com/drewhutchison/piplate_modbus',
            'ProductCode': 'ppDAQC-R1.0',
            'ProductName': 'DAQCplate',
            'ModelName': 'DAQCplate',
            'MajorMinorRevision': VERSION
        })


def get_server_context():
    slaves = {board_address: get_slave_context(board_address)
              if dp.daqcsPresent[board_address]
              else None
              for board_address
              in range(8)}

    return ModbusServerContext(slaves=slaves, single=False)


def get_slave_context(board_address):
    return ModbusSlaveContext(
        di=DAQCPlateDIDataBlock(board_address),
        co=DACQPlateCODataBlock(board_address),
        hr=DACQPlateHRDataBlock(board_address),
        ir=DACQPlateIRDataBlock(board_address)
    )
