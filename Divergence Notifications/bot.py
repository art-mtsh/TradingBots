import telebot
from datetime import datetime
from time import sleep
from screenshoter import sendScreen

# --- TELEGRAM ---

TOKEN = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot = telebot.TeleBot(TOKEN)

# bot.send_message(662482931, f"0000000000000 "
# 							f"\nBearish divergence."
# 							f"\nCD fractals on volumes:"
# 							f"\n00000000000000000\nhttps://www.binance.com/en/futures/AAVEUSDT/",
# 				 disable_web_page_preview=True)
#
# pic = open('AAVEUSDT.png', 'rb')
# bot.send_photo(662482931, pic)

# bot.send_message(662482931, f"{datetime.now().strftime('%H:%M')[0:4]}0")

(bot.send_message(662482931, f"Bigger")) if 4 - 2 == 2 else None