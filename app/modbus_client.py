from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from app.modbus_utils import float_to_registers, format_display_value


class ModbusSender:
    def __init__(self, host: str, port: int = 502, device_id: int = 1, start_address: int = 0):
        self.host = host
        self.port = port
        self.device_id = device_id
        self.start_address = start_address

    def send_value(self, value: float) -> bool:
        client = ModbusTcpClient(self.host, port=self.port, timeout=21)
        print(f"[MODBUS] Cliente: {client}")

        try:
            if not client.connect():
                print(f"[MODBUS] No se pudo conectar a {self.host}:{self.port}")
                return False

            registers = float_to_registers(value)

            print(f"[MODBUS] Valor real: {format_display_value(value)}")
            print(f"[MODBUS] Registers a enviar: {registers}")
            print(f"[MODBUS] Dirección inicial: {self.start_address}")
            print("[MODBUS] Formato: Float Little-endian byte swap")

            write_response = client.write_registers(
                address=self.start_address,
                values=registers,
                device_id=self.device_id
            )

            if write_response.isError():
                print(f"[MODBUS] Error al escribir: {write_response}")
                return False

            print("[MODBUS] Escritura exitosa")

            read_response = client.read_holding_registers(
                address=self.start_address,
                count=2,
                device_id=self.device_id
            )

            if read_response.isError():
                print(f"[MODBUS] Error en lectura de validación: {read_response}")
                return False

            print(f"[MODBUS] Validación inmediata, registers leídos: {read_response.registers}")
            return True

        except ModbusException as e:
            print(f"[MODBUS] Excepción Modbus: {e}")
            return False
        except Exception as e:
            print(f"[MODBUS] Error general: {e}")
            return False
        finally:
            client.close()