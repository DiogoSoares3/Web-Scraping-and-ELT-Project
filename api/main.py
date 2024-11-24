import os

import uvicorn
from fastapi import FastAPI

from src.puma_shoes import router as puma_shoes_router
from src.telegram_connections import router as telegram_bot_router
from src.database_operations import router as database_router


app = FastAPI(title='DataWarehouse API')

prefix = '/api'
app.include_router(puma_shoes_router, prefix=prefix)
app.include_router(telegram_bot_router, prefix=prefix)
app.include_router(database_router, prefix=prefix)


if __name__ == "__main__":
    print("Initializing API server...")
    uvicorn.run(
        "main:app",
        port=8200,
        host='0.0.0.0',
        reload=True,
        log_level="info"
        )
