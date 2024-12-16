from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select

from core.deps import get_session
from schemas.puma_shoes_schema import MetricsPumaShoesSchema, Top10BestPumaShoesSchema


router = APIRouter()


@router.get("/metrics/", description='', response_model=List[MetricsPumaShoesSchema], status_code=200)
def metrics(session = Depends(get_session)):
    from models.metrics_model import MetricsPumaPrices
    
    result = session.execute(select(MetricsPumaPrices)).scalars().all()
    return result


@router.get("/top10-best-puma/", description='', response_model=List[Top10BestPumaShoesSchema], status_code=200)
def get_top10(session = Depends(get_session)):
    from models.top10_puma_model import Top10BestPumaShoesPrice
    
    result = session.execute(select(Top10BestPumaShoesPrice)).scalars().all()
    return result
