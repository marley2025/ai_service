def infer_base_unit(product_name: str, fallback: str) -> str:
    p = product_name.lower()
    if "cement" in p: return "kg"
    if "rebar" in p: return "m"
    if "gypsum" in p or "board" in p: return "m2"
    return fallback
