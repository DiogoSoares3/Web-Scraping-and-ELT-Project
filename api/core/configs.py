from typing import ClassVar
import os

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

class Settings(BaseSettings):

    """
    General configs used for the the aplication
    """

    DBBaseModel: ClassVar = declarative_base()

    load_dotenv()
    DB_URL: ClassVar = os.getenv("DB_URL")
    TOKEN: ClassVar = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID: ClassVar = os.getenv('TELEGRAM_CHAT_ID')

    class Config:
        case_sensitive = True


settings: Settings = Settings()
