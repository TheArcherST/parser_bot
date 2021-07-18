from config import bot
from .database_helpers import accept_message
from telebot.types import Message


@bot.middleware_handler(update_types=['message'])
def all_messages_indexer(_bot_instance, message: Message):
    if message.text is None:
        return None

    accept_message(message)
