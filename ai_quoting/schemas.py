from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Unit = Literal["kg", "m", "m2", "m3", "piece", "pack"]

class QuoteRequest(BaseModel):
    product_name: str
    qty: float = Field(..., gt=0)
    uom: Unit
    eircode: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    country: Optional[str] = "IE"

class ProviderOffer(BaseModel):
    supplier: str
    currency: str = "EUR"
    unit_price: float
    pack_size_qty: float
    pack_size_uom: Unit
    includes_vat: bool = True
    vat_rate: Optional[float] = None
    availability: str = "in_stock"
    lead_time_days: int = 2
    delivery_fee: float = 0.0
    option: str = "delivery"
    title: Optional[str] = None
    url: Optional[str] = None

class NormalizedOffer(BaseModel):
    supplier: str
    currency: str
    unit_price_incl_vat: float
    per_base_unit_price: float
    base_unit: Unit
    pack_size_qty: float
    pack_size_uom: Unit
    availability: str
    lead_time_days: int
    delivery_fee: float
    option: str
    title: Optional[str] = None
    url: Optional[str] = None

class OptionOut(BaseModel):
    supplier: str
    unit_price_incl_vat: float
    per_base_unit: float
    lead_time_days: int
    total: float
    option: str
    title: Optional[str] = None
    url: Optional[str] = None

class QuoteResponse(BaseModel):
    recommendation: OptionOut
    alternatives: List[OptionOut]
