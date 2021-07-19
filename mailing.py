from users.database_helpers import UsersKeeper, UserConfigsKeeper
from telebot.apihelper import ApiException
from config import bot


def mailing(markdown_text, mailing_tag: str = None):
    conn = UsersKeeper()
    chats = conn.get_user_ids()

    for chat_id in chats:
        if mailing_tag is not None:
            conn = UserConfigsKeeper()
            config = conn.get_config(chat_id)
            if mailing_tag == 'spce' and not config.spce:
                continue

        try:
            chat = bot.get_chat(chat_id)
        except ApiException:
            continue

        try:
            bot.send_message(chat_id, markdown_text, parse_mode='Markdown')
        except ApiException:
            continue
