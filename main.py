#!/usr/bin/env python

import logging
import argparse

from pymodbus.server.sync import StartTcpServer

parser = argparse.ArgumentParser()

parser.add_argument(
    '--log',
    dest='loglevel',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help='Set the logging level (default: %(default)s)',
    default='INFO')

parser.add_argument(
    '--host',
    dest='host',
    default='localhost',
    help='Host to serve on (default: %(default)s)'
)

parser.add_argument(
    '--port',
    dest='port',
    type=int,
    default=5020,
    help='Port to serve on (default: %(default)i)'
)

args = parser.parse_args()

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')

logging.basicConfig(level=logging.getLevelName(args.loglevel),
                    format=FORMAT)

from piplate_modbus.contexts import DAQCPlateIdentification, get_server_context

logging.getLogger(__name__).info('Starting server on {}:{}'.format(
    args.host, args.port
))

StartTcpServer(
    context=get_server_context(),
    identity=DAQCPlateIdentification,
    address=(args.host, args.port)
)
