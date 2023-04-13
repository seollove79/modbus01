#!/usr/bin/env python3

""" Read 10 holding registers and print result on stdout. """

from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import *

client = ModbusTcpClient("192.168.0.3", 502)
for n in range (0,3):
    #result = client.read_coils(n,1)
    result = client.read_holding_registers(0)
    print(result.registers)

#client.write_coil(0, True)
client.write_register(1,3456)