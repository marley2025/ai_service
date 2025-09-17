from typing import List
from ai_quoting.schemas import ProviderOffer
from ai_quoting.adapters.base import Adapter

class Chadwicks(Adapter):
    name = "chadwicks"
    def fetch_offers(self, product_name: str, qty: float, uom: str) -> List[ProviderOffer]:
        if "cement" in product_name.lower():
            return [
                ProviderOffer(supplier="Chadwicks", unit_price=7.95, pack_size_qty=25, pack_size_uom="kg", title="Cement 25kg", url="https://www.chadwicks.ie/", option="delivery"),
                ProviderOffer(supplier="Chadwicks", unit_price=7.50, pack_size_qty=25, pack_size_uom="kg", title="Cement 25kg Click&Collect", url="https://www.chadwicks.ie/", option="click_collect")
            ]
        return []
