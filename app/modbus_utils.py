import struct
from decimal import Decimal, ROUND_HALF_UP


def float_to_registers(value) -> list[int]:
    """
    Convierte un valor a float32 (IEEE754) en 2 registers Modbus,
    aplicando un pequeño ajuste para evitar valores tipo 12.129999.
    """

    # forzar 2 decimales exactos
    value = Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    # pequeño ajuste para evitar representación binaria inferior
    adjusted = float(value) + 1e-6

    packed = struct.pack(">f", adjusted)

    high_word = int.from_bytes(packed[0:2], byteorder="big")
    low_word = int.from_bytes(packed[2:4], byteorder="big")

    return [high_word, low_word]


def registers_to_float(registers: list[int]) -> float:
    """
    Reconstruye un float IEEE754 desde 2 registers Modbus.
    """

    if len(registers) != 2:
        raise ValueError("Se requieren exactamente 2 registers")

    high_word, low_word = registers

    packed = (
        high_word.to_bytes(2, byteorder="big") +
        low_word.to_bytes(2, byteorder="big")
    )

    return struct.unpack(">f", packed)[0]