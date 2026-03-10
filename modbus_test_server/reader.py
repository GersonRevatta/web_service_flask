import sys
from pymodbus.client import ModbusTcpClient

sys.path.append("..")

from app.modbus_utils import registers_to_uint32, registers_to_real

HOST = "127.0.0.1"
PORT = 5020
DEVICE_ID = 1
START_ADDRESS = 0
COUNT = 2


def read_value():
    client = ModbusTcpClient(HOST, port=PORT, timeout=3)

    try:
        if not client.connect():
            print(f"[READER] No se pudo conectar a {HOST}:{PORT}")
            return

        response = client.read_holding_registers(
            address=START_ADDRESS,
            count=COUNT,
            device_id=DEVICE_ID
        )

        if response.isError():
            print(f"[READER] Error al leer: {response}")
            return

        registers = response.registers
        raw_value = registers_to_uint32(registers)
        real_value = registers_to_real(registers)

        print(f"[READER] Registers leídos: {registers}")
        print(f"[READER] Entero escalado: {raw_value}")
        print(f"[READER] Valor real: {real_value:.2f}")

    finally:
        client.close()


if __name__ == "__main__":
    read_value()