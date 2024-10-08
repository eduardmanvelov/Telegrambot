import telebot
from config import TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN)
from handlers import *
from handlers.movie_search_handler import *
from handlers.movie_rating_handler import *
from handlers.movie_budget_handler import *