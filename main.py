#!/bin/python
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
 
# Create an instance of Modbus Client
client_001 = ModbusClient(host="192.168.0.3", port=502, unit_id=1, debug=False)
 
# Create an instance of Modbus Server
server = ModbusServer(host="192.168.0.3", port=503, no_block=True, ipv6=False)
 
set_list_001 = [0]
get_list_001 = [0]
 
try:
    # Modbus TCP Server DataBack init.
    client_001.open()

    if client_001.is_open():
        read_list_001 = client_001.read_holding_registers(reg_addr=0, reg_nb=1)
        set_list_001 = read_list_001
 
        DataBank.set_words(address=0, word_list=read_list_001)
        get_list_001 = DataBank.get_words(address=0, number=1)
 
        client_001.close()
 
        print("Start server . . . ")
        server.start()
        print("Server is online")  
    else:
        print("Error with Client Port Open")
 
    while True:
        client_001.open()
        if client_001.is_open():
            read_list_001 = client_001.read_holding_registers(reg_addr=0, reg_nb=1)
 
            if set_list_001 != read_list_001:
                set_list_001 = read_list_001
                DataBank.set_words(address=0, word_list=read_list_001)
                client_001.close()
            elif DataBank.get_words(address=0, number=1) != get_list_001:
                get_list_001 = DataBank.get_words(address=0, number=1)
                client_001.write_single_register(reg_addr=0, reg_value=int(get_list_001[0]))
                client_001.close()
            else:
                client_001.close()
        else:
                print("port open error")
        sleep(1)
except ValueError:
    print("Shutdown server . . .")
    server.stop()
    print("Server is offline")