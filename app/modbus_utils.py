import struct
from decimal import Decimal, ROUND_HALF_UP

FLOAT_FORMAT = "CDAB"
# Prueba en este orden si no sale bien:
# "ABCD", "BADC", "CDAB", "DCBA"


def normalize_value(value: float | str) -> float:
    dec_value = Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    if dec_value < 0:
        raise ValueError("No se permiten valores negativos")

    if dec_value > Decimal("999.99"):
        raise ValueError("Valor fuera del rango permitido (999.99)")

    return float(dec_value)


def format_display_value(value: float | str) -> str:
    normalized = normalize_value(value)
    return f"{normalized:06.2f}"


def reorder_bytes(raw: bytes, fmt: str) -> bytes:
    """
    raw siempre entra como ABCD
    """
    a, b, c, d = raw[0:1], raw[1:2], raw[2:3], raw[3:4]

    mapping = {
        "ABCD": a + b + c + d,
        "BADC": b + a + d + c,
        "CDAB": c + d + a + b,
        "DCBA": d + c + b + a,
    }

    if fmt not in mapping:
        raise ValueError("Formato inválido. Usa ABCD, BADC, CDAB o DCBA")

    return mapping[fmt]


def inverse_reorder_bytes(raw: bytes, fmt: str) -> bytes:
    """
    Convierte desde fmt de vuelta a ABCD
    """
    if fmt == "ABCD":
        return raw
    if fmt == "BADC":
        return bytes([raw[1], raw[0], raw[3], raw[2]])
    if fmt == "CDAB":
        return bytes([raw[2], raw[3], raw[0], raw[1]])
    if fmt == "DCBA":
        return raw[::-1]

    raise ValueError("Formato inválido. Usa ABCD, BADC, CDAB o DCBA")


def float_to_registers(value: float | str) -> list[int]:
    normalized = normalize_value(value)

    raw = struct.pack(">f", normalized)
    ordered = reorder_bytes(raw, FLOAT_FORMAT)

    reg1 = int.from_bytes(ordered[0:2], byteorder="big")
    reg2 = int.from_bytes(ordered[2:4], byteorder="big")

    return [reg1, reg2]


def registers_to_float(registers: list[int]) -> float:
    if len(registers) != 2:
        raise ValueError("Se requieren exactamente 2 registers")

    raw = (
        registers[0].to_bytes(2, byteorder="big") +
        registers[1].to_bytes(2, byteorder="big")
    )

    abcd = inverse_reorder_bytes(raw, FLOAT_FORMAT)
    value = struct.unpack(">f", abcd)[0]

    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    )