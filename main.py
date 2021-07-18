from colorama import Fore, Style, Back

print('Initialization...', end=' ')

from threading import Thread
from users import setup_users
from spce_parser_backend import Server as SPCEServer
from config import bot
import my_bot

setup_users()

spce_server = SPCEServer(1, 1)
spce_server.start()


def pooling():
    bot.polling(none_stop=True)

thread = Thread(target=pooling)
thread.start()

print(f'{Fore.GREEN}done{Style.RESET_ALL}')
print(f'\n\nScript inited!')

# while True:
#     text = input("main >>> ")
#
#     if text == 'quit':
#         spce_server.stop()
#         print('\nServer thread stop requested, wait...')
#         exit()
