from typing import List
from ai_quoting.schemas import ProviderOffer
from ai_quoting.adapters.base import Adapter

class Brooks(Adapter):
    name = "brooks"
    def fetch_offers(self, product_name: str, qty: float, uom: str) -> List[ProviderOffer]:
        if "cement" in product_name.lower():
            return [
                ProviderOffer(supplier="Brooks", unit_price=8.00, pack_size_qty=25, pack_size_uom="kg", title="Cement 25kg", url="https://www.brooks.ie/", option="click_collect")
            ]
        return []
