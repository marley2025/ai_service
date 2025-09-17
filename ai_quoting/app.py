from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from ai_quoting.schemas import QuoteRequest, QuoteResponse, OptionOut
from ai_quoting.settings import settings
from ai_quoting.adapters.chadwicks import Chadwicks
from ai_quoting.adapters.screwfix import Screwfix
from ai_quoting.adapters.brooks import Brooks
from ai_quoting.core.normalize import normalize_offer
from ai_quoting.core.scoring import score
from ai_quoting.utils.cache import TTLCache

app = FastAPI(title=settings.app_name, default_response_class=ORJSONResponse)

ADAPTERS = [Chadwicks(), Screwfix(), Brooks()]
CACHE = TTLCache(max_items=settings.cache_max_items, ttl=settings.cache_ttl_seconds)

@app.get("/health")
def health():
    return {"ok": True, "env": settings.environment}

@app.get("/adapters")
def adapters():
    return {"adapters": [a.name for a in ADAPTERS]}

@app.post("/quote", response_model=QuoteResponse)
def quote(req: QuoteRequest):
    key = f"{req.product_name}|{req.qty}|{req.uom}|{req.country}"
    cached = CACHE.get(key)
    if cached:
        return cached

    offers = []
    for a in ADAPTERS:
        try:
            for off in a.fetch_offers(req.product_name, req.qty, req.uom):
                no = normalize_offer(req.product_name, off)
                offers.append(no.__dict__)
        except Exception as e:
            print(f"Adapter {a.name} error: {e}")

    if not offers:
        offers = [{
            "supplier": "Default",
            "unit_price_incl_vat": 10.0,
            "per_base_unit_price": 1.0,
            "base_unit": req.uom,
            "pack_size_qty": 1.0,
            "pack_size_uom": req.uom,
            "availability": "limited",
            "lead_time_days": 3,
            "delivery_fee": 12.0,
            "option": "delivery"
        }]

    ranked = score(offers)

    def to_option(o, qty):
        packs_needed = max(qty / o["pack_size_qty"], 1.0)
        total = round(packs_needed * o["unit_price_incl_vat"] + o.get("delivery_fee", 0.0), 2)
        return OptionOut(
            supplier=o["supplier"],
            unit_price_incl_vat=round(o["unit_price_incl_vat"], 2),
            per_base_unit=round(o["per_base_unit_price"], 4),
            lead_time_days=o["lead_time_days"],
            total=total,
            option=o["option"],
            url=o.get("url"),
            title=o.get("title")
        )

    best = to_option(ranked[0], req.qty)
    alts = [to_option(o, req.qty) for o in ranked[1:3]]

    resp = QuoteResponse(recommendation=best, alternatives=alts)
    CACHE.set(key, resp)
    return resp
