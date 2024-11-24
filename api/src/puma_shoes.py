from typing import List
import sys
import os

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import fireducks.pandas as pd

from core.configs import settings
from core.database import engine
from core.deps import get_session
from schemas.puma_shoes_schema import *

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
router = APIRouter()


@router.get("/metrics/", description='')
def metrics(session = Depends(get_session)):
    pass
