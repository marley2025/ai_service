def to_eur(amount: float, currency: str) -> float:
    c = (currency or "EUR").upper()
    if c == "EUR": return amount
    if c == "USD": return amount * 0.92
    if c == "GBP": return amount * 1.18
    if c == "MXN": return amount / 19.5
    return amount
