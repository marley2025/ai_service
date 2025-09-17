from ai_quoting.schemas import ProviderOffer, NormalizedOffer
from ai_quoting.settings import settings

def normalize_offer(product_name: str, o: ProviderOffer):
    vat = o.vat_rate if o.vat_rate else settings.ie_default_vat
    price_incl = o.unit_price if o.includes_vat else o.unit_price * (1 + vat)
    per_base = price_incl / o.pack_size_qty
    return NormalizedOffer(
        supplier=o.supplier,
        currency="EUR",
        unit_price_incl_vat=round(price_incl, 2),
        per_base_unit_price=round(per_base, 4),
        base_unit=o.pack_size_uom,
        pack_size_qty=o.pack_size_qty,
        pack_size_uom=o.pack_size_uom,
        availability=o.availability,
        lead_time_days=o.lead_time_days,
        delivery_fee=o.delivery_fee,
        option=o.option,
        title=o.title,
        url=o.url
    )
