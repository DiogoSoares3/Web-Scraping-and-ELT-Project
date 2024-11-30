from typing import List
import sys
import os

from fastapi import APIRouter, Depends
from sqlalchemy import select
import fireducks.pandas as pd

from core.configs import settings
from core.database import engine
from core.deps import get_session
from schemas.puma_shoes_schema import *


router = APIRouter()


@router.get("/metrics/", description='')
def metrics(session = Depends(get_session)):
    from models.metrics_model import MetricsPumaPrices
    
    result = session.execute(select(MetricsPumaPrices)).scalars().all()
    print(result)
    return result


@router.get("/top10-best-puma/", description='')
def get_top10(session = Depends(get_session)):
    from models.top10_puma_model import Top10BestPumaShoesPrice
    
    result = session.execute(select(Top10BestPumaShoesPrice)).scalars().all()
    print(result)
    return result