from users.database_helpers import UsersKeeper
from telebot.apihelper import ApiException
from config import bot


def mailing(markdown_text):
    conn = UsersKeeper()
    chats = conn.get_user_ids()

    for chat_id in chats:
        try:
            chat = bot.get_chat(chat_id)
        except ApiException:
            continue

        try:
            bot.send_message(chat_id, markdown_text, parse_mode='Markdown')
        except ApiException:
            continue
