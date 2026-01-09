import re
from langchain.tools import tool


LENGTH_UNITS = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "mi": 1609.34,
    "ft": 0.3048,
    "in": 0.0254,
}

WEIGHT_UNITS = {
    "kg": 1.0,
    "g": 0.001,
    "lb": 0.45359237,
    "oz": 0.0283495,
}

CUBIC_UNITS = {
    "l": 1.0,
    "litro": 1.0,
    "litros": 1.0,
    "ml": 0.001,
    "cl": 0.01,
    "dl": 0.1,
    "hl": 100.0,
}

TEMP_UNITS = {"c", "f", "k"}


def _parse_amount(expr: str):
    match = re.match(r"\s*([+-]?[0-9]*\.?[0-9]+)\s*([a-zA-Z]+)\s*(?:to|em|para)\s*([a-zA-Z]+)\s*$", expr)
    if not match:
        raise ValueError("Use o formato: '10 km para mi' ou '32 F to C'.")
    value = float(match.group(1))
    src = match.group(2).lower()
    dst = match.group(3).lower()
    return value, src, dst


def _convert_temperature(value, src, dst):
    if src == dst:
        return value
    if src == "c":
        if dst == "f":
            return value * 9 / 5 + 32
        if dst == "k":
            return value + 273.15
    if src == "f":
        c = (value - 32) * 5 / 9
        if dst == "c":
            return c
        if dst == "k":
            return c + 273.15
    if src == "k":
        if dst == "c":
            return value - 273.15
        if dst == "f":
            return (value - 273.15) * 9 / 5 + 32
    raise ValueError("Unidades de temperatura suportadas: C, F, K.")


def _convert_generic(value, src, dst, table, label):
    if src not in table or dst not in table:
        raise ValueError(f"Unidades de {label} suportadas: {', '.join(sorted(table.keys()))}")
    base = value * table[src]
    return base / table[dst]


@tool
def unit_converter(expression: str) -> str:
    """
    Converte unidades de comprimento, peso, temperatura ou moeda.
    Formato: "<valor> <origem> para <destino>". Ex: "10 km para mi".
    """
    value, src, dst = _parse_amount(expression)

    if src in TEMP_UNITS or dst in TEMP_UNITS:
        if not (src in TEMP_UNITS and dst in TEMP_UNITS):
            raise ValueError("Para temperaturas use apenas C, F ou K.")
        result = _convert_temperature(value, src, dst)
        return f"{value} {src} = {result:.6g} {dst}"

    if src in LENGTH_UNITS or dst in LENGTH_UNITS:
        result = _convert_generic(value, src, dst, LENGTH_UNITS, "comprimento")
        return f"{value} {src} = {result:.6g} {dst}"

    if src in WEIGHT_UNITS or dst in WEIGHT_UNITS:
        result = _convert_generic(value, src, dst, WEIGHT_UNITS, "peso")
        return f"{value} {src} = {result:.6g} {dst}"

    if src in CUBIC_UNITS or dst in CUBIC_UNITS:
        result = _convert_generic(value, src, dst, CUBIC_UNITS, "volume")
        return f"{value} {src} = {result:.6g} {dst}"

    raise ValueError("Unidades não suportadas. Exemplos: '10 km para mi', '32 F para C'.")

