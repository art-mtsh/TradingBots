import telebot
import datetime

TOKEN1 = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot1 = telebot.TeleBot(TOKEN1)

TOKEN2 = '5947685641:AAEofMStDGj0M0nGhVdlMEEEFP-dOAgOPaw'
bot2 = telebot.TeleBot(TOKEN2)

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

# bot3.send_message(662482931, f'123')


now = datetime.datetime.now()

hours_now = int(now.strftime('%H'))

if hours_now in list(range(9, 18)):
	print(hours_now)
else:
	print(None)