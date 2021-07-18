from config import bot


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    bot.send_message(message.chat.id, 'Hello, Mazafaker!') 
