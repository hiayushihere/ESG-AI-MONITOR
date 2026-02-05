import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///esg.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "pool_pre_ping": True
    }

    # 📰 News API Key
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
