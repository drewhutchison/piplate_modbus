#!/usr/bin/env python

from setuptools import setup

from piplate_modbus.__version__ import VERSION

setup(
    name='piplate_modbus',
    version=VERSION,
    author='andrew james hutchison',
    description='modbus server for piplates DAQCplate',
    packages=['piplate_modbus'],
    install_requires=[
        'pi-plates==4.1',
        'pymodbus>=2.0.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering ::'
        'Interface Engine/Protocol Translator'
    ],
    long_description=open('README.rst').read(),
    test_suite='test'
)
