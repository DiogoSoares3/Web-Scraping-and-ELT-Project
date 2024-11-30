from typing import List
import sys
import os

from fastapi import APIRouter, Depends, Body, Request
from pydantic import BaseModel

from core.database import engine
from core.deps import get_session
# sys.path.append('/datawarehouse')
from sources.utils import insert_data_to_postgres


router = APIRouter()


@router.post("/insert-data/", description='Insert data to Postgres database given a source directory containing JSON or CSV files.')
async def insert_data(request: Request, session = Depends(get_session)):
    content = await request.json()
    response = insert_data_to_postgres(engine, session, content['schema'], content['source_dir'])
    return {'response': response}
