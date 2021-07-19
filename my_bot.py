from config import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from users import UserConfigsKeeper


def get_start_markup():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('SPCE', callback_data='start:spce'))

    return markup


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    markup = get_start_markup()
    bot.send_message(message.chat.id, 'Привет! Выбери что ты хочешь отслеживать', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('start'))
def start_callback(call):
    data = call.data.split(':')[1]
    bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text='Окей, мы будем отправлять тебе уведомления!')
    if data == 'spce':
        conn = UserConfigsKeeper()
        conn.update(call.from_user.id, spce=True)
