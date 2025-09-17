from typing import List, Dict
from ai_quoting.settings import settings

def score(offers: List[Dict]):
    if not offers:
        return []
    prices = [o["per_base_unit_price"] for o in offers]
    pmin, pmax = min(prices), max(prices)
    def s_price(v): return 1.0 if pmax==pmin else 1 - (v-pmin)/(pmax-pmin)
    leads = [o["lead_time_days"] for o in offers]
    lmin, lmax = min(leads), max(leads)
    def s_lead(v): return 1.0 if lmax==lmin else 1 - (v-lmin)/(lmax-lmin)
    def s_stock(av): return {"in_stock":1,"limited":0.6,"out":0}.get(av,0.5)
    fees = [o["delivery_fee"] for o in offers]
    fmin, fmax = min(fees), max(fees)
    def s_fee(v): return 1.0 if fmax==fmin else 1 - (v-fmin)/(fmax-fmin)

    for o in offers:
        o["_score"] = (
            settings.weight_price*s_price(o["per_base_unit_price"])
            + settings.weight_leadtime*s_lead(o["lead_time_days"])
            + settings.weight_stock*s_stock(o["availability"])
            + settings.weight_fees*s_fee(o["delivery_fee"])
        )
    return sorted(offers, key=lambda x:(-x["_score"], x["per_base_unit_price"], x["lead_time_days"]))
