import requests
from langchain.tools import tool


FX_ENDPOINT = "https://api.exchangerate.host/convert"

FALLBACK_RATES = {
    "usd": 1.0,
    "eur": 0.93,
    "brl": 5.6,
    "gbp": 0.79,
    "jpy": 150.0,
}


@tool
def fx_converter(query: str) -> str:
    """
    Converte valores entre moedas. Formato sugerido: "100 USD para BRL".
    Usa exchangerate.host; se falhar, usa taxas estáticas de fallback.
    """
    parts = query.replace(",", ".").split()
    if len(parts) < 3:
        raise ValueError("Use o formato: '<valor> <moeda_origem> para <moeda_destino>'. Ex: '100 USD para BRL'.")

    try:
        amount = float(parts[0])
    except ValueError:
        raise ValueError("Valor inválido. Exemplo: '100 USD para BRL'.")

    if "para" in parts:
        para_idx = parts.index("para")
    elif "to" in parts:
        para_idx = parts.index("to")
    else:
        raise ValueError("Use 'para' ou 'to' entre as moedas. Ex: '100 USD para BRL'.")

    try:
        src = parts[1].lower()
        dst = parts[para_idx + 1].lower()
    except Exception:
        raise ValueError("Formato inválido. Exemplo: '100 USD para BRL'.")

    # Tenta API
    try:
        resp = requests.get(FX_ENDPOINT, params={"from": src.upper(), "to": dst.upper(), "amount": amount}, timeout=8)
        data = resp.json()
        if resp.status_code == 200 and data.get("result") is not None:
            result = data["result"]
            rate = data.get("info", {}).get("rate")
            rate_info = f" (taxa {rate:.6g})" if rate else ""
            return f"{amount} {src.upper()} = {result:.6g} {dst.upper()}{rate_info}"
    except Exception:
        pass

    # Fallback
    if src not in FALLBACK_RATES or dst not in FALLBACK_RATES:
        raise ValueError("Moedas não suportadas no fallback. Use USD, EUR, BRL, GBP ou JPY.")
    base = amount / FALLBACK_RATES[src]
    result = base * FALLBACK_RATES[dst]
    return f"{amount} {src.upper()} = {result:.6g} {dst.upper()} (taxas estáticas de fallback)"

