from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AIQ_", case_sensitive=False)
    app_name: str = "AI Quoting Service"
    environment: str = "dev"
    host: str = "0.0.0.0"
    port: int = 8080
    weight_price: float = 0.55
    weight_leadtime: float = 0.20
    weight_stock: float = 0.15
    weight_fees: float = 0.10
    ie_default_vat: float = 0.23
    mx_default_vat: float = 0.16
    cache_ttl_seconds: int = 300
    cache_max_items: int = 256

settings = Settings()
