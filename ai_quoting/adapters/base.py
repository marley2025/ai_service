from typing import List
from ai_quoting.schemas import ProviderOffer

class Adapter:
    name = "base"
    def fetch_offers(self, product_name: str, qty: float, uom: str) -> List[ProviderOffer]:
        raise NotImplementedError
