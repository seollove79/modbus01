from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from pymodbus.server.sync import StartTcpServer
from threading import Thread

# define the Modbus server context
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [1] * 100),
    co=ModbusSequentialDataBlock(0, [2] * 100),
    hr=ModbusSequentialDataBlock(0, [3] * 100),
    ir=ModbusSequentialDataBlock(0, [4] * 100)
)

context = ModbusServerContext(slaves=store, single=True)

# define a function to handle the Modbus function code 3 request
def read_registers(context, address, count):
    builder = BinaryPayloadBuilder(byteorder=Endian.Big)
    for i in range(address, address+count):
        builder.add_16bit_uint(store.get_values(3, i, count=1)[0])
    return builder.to_registers()

# define a function to handle the client connection
def handle_client(server, client, address):
    while True:
        request = client.receive()
        if request:
            if request.function_code == 3:
                start_address = request.address
                register_count = request.count
                values = read_registers(context, start_address, register_count)
                response = client.build_response(request, values)
                server.send(response, address)

# create a new thread to handle the client connection
def start_server():
    server = StartTcpServer(context, address=("localhost", 502))
    while True:
        client, address = server.accept()
        client_thread = Thread(target=handle_client, args=(server, client, address))
        client_thread.daemon = True
        client_thread.start()

# start the server
start_server()