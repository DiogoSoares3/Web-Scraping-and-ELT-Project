import math

from fastapi import APIRouter, Depends
from telegram import Bot
from sqlalchemy import select

from core.configs import settings
from core.deps import get_session


bot = Bot(token=settings.TOKEN)
router = APIRouter()


async def send_telegram_message(result) -> None:
    best_price = math.inf

    if result:
        for element in result:
            if element.price < best_price:
                best_price = element.price

                text = f'''
                The cheaper Puma Infusion Running was collected on {element.datetime.strftime('%d/%m/%Y %H:%M:%S')} from {element.site} website with a price of R${element.price}
                '''

        await bot.send_message(chat_id=settings.CHAT_ID, text=text)


@router.get("/telegram-bot", description='')
async def telegram_bot(session = Depends(get_session)):
    from models.infusion_model import PriceOverTimeInfusion
 
    result = session.execute(select(PriceOverTimeInfusion)).scalars().all()

    await send_telegram_message(result)
    return {'response': 'success'}
