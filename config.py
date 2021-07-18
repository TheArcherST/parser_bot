import os
from dotenv import load_dotenv
import telebot
import datetime


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


telebot.apihelper.ENABLE_MIDDLEWARE = True

BOT_API_KEY = os.environ.get('BOT_API_KEY')

bot = telebot.TeleBot(BOT_API_KEY)
