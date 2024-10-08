import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MOVIE_API_KEY = os.getenv("MOVIE_API_KEY")