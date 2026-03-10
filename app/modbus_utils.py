from decimal import Decimal, ROUND_HALF_UP

SCALE = 100


def scale_value(value: float | str) -> int:
    """
    Convierte un número con 2 decimales a entero escalado x100.
    Ejemplo: 123.45 -> 12345
    """
    dec_value = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    scaled = int(dec_value * SCALE)

    if scaled < 0:
        raise ValueError("No se permiten valores negativos en esta implementación.")

    if scaled > 99999:
        raise ValueError("El valor excede el máximo esperado de 999.99")

    return scaled


def uint32_to_registers(value: int) -> list[int]:
    """
    Convierte un uint32 a 2 registers de 16 bits.
    Orden usado: [high_word, low_word]
    """
    if value < 0 or value > 0xFFFFFFFF:
        raise ValueError("Valor fuera de rango para uint32")

    high_word = (value >> 16) & 0xFFFF
    low_word = value & 0xFFFF
    return [high_word, low_word]


def registers_to_uint32(registers: list[int]) -> int:
    """
    Reconstruye un uint32 desde 2 registers.
    Espera [high_word, low_word]
    """
    if len(registers) != 2:
        raise ValueError("Se requieren exactamente 2 registers")

    high_word, low_word = registers
    return (high_word << 16) | low_word

def registers_to_real(registers: list[int]) -> float:
    scaled = registers_to_uint32(registers)
    return scaled / SCALE



def normalize_value(value: float | str) -> float:
    """
    Fuerza formato 3 enteros y 2 decimales.
    Ejemplo:
    93.31 -> 093.31
    5 -> 005.00
    """
    dec_value = Decimal(str(value)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    if dec_value < 0:
        raise ValueError("No se permiten valores negativos")

    if dec_value > Decimal("999.99"):
        raise ValueError("Valor fuera del rango permitido (999.99)")

    return float(dec_value)


def real_to_registers(value: float | str) -> list[int]:

    normalized = normalize_value(value)

    scaled = int(round(normalized * SCALE))

    high_word = (scaled >> 16) & 0xFFFF
    low_word = scaled & 0xFFFF

    return [high_word, low_word]