import asyncio
import os

from telegram import Bot
from dotenv import load_dotenv
import requests
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
DB_URL = os.getenv("DB_URL")

bot = Bot(token=TOKEN)
app = FastAPI()

## DEIXAR ESSE CODIGO NO DIRETORIO /api DEPOIS. Organizar todos os endpoints pra la

async def send_telegram_message(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)
      

# Rota raiz
@app.get("/telegram-bot")
async def telegram_bot():
    try:
        engine = create_engine(DB_URL, echo=False, future=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        schema = "data"
        table_name = "price_over_time_infusion"
        
        query = text(f"SELECT * FROM {schema}.{table_name}")
        result = session.execute(query).fetchall()
        
        await send_telegram_message(str(result))

    except Exception as e:
        raise e
    finally:
        session.close()

    return {"message": "success"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("telegram_connection:app", host="0.0.0.0",
                port=8000, log_level='info',
                reload=True)