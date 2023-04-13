from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification

# 모드버스 TCP/IP 서버 생성
StartTcpServer(
    # 서버 IP 주소와 포트 설정
    address=("localhost", 502),
    # 데이터를 저장할 SlaveContext 생성
    context=modbus_context,
    # 디바이스 정보 설정
    identity=ModbusDeviceIdentification(),
    # 쓰기 권한 설정 (True: 쓰기 가능, False: 쓰기 불가능)
    single=True,
)
