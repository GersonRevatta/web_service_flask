from pymodbus import pymodbus_apply_logging_config
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusDeviceContext,
    ModbusServerContext,
)
from pymodbus.server import StartTcpServer

HOST = "127.0.0.1"
PORT = 5020
DEVICE_ID = 1


def run_server():
    pymodbus_apply_logging_config("DEBUG")

    store = ModbusDeviceContext(
        hr=ModbusSequentialDataBlock(0, [0] * 200)
    )

    context = ModbusServerContext(
        devices={DEVICE_ID: store},
        single=False
    )

    print(f"[SERVER] Modbus TCP escuchando en {HOST}:{PORT}")
    print(f"[SERVER] device_id={DEVICE_ID}")
    print("[SERVER] Holding registers inicializados en 0")

    StartTcpServer(
        context=context,
        address=(HOST, PORT)
    )


if __name__ == "__main__":
    run_server()