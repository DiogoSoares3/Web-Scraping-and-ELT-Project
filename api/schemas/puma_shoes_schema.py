from typing import Optional
from pydantic import BaseModel, ConfigDict


class MetricsPumaShoesSchema(BaseModel):
    site: str
    min_price: float
    max_price: float
    mean_price: float
    stddev_price: float
    percentile_25: float
    median_price: float
    percentile_75: float
    qtd_shoes: int

    model_config = ConfigDict(from_attributes=True)


class Top10BestPumaShoesSchema(BaseModel):
    name: str
    brand: Optional[str]
    price: float
    site: str

    model_config = ConfigDict(from_attributes=True)
