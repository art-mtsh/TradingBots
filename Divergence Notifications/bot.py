import telebot

# --- TELEGRAM ---

TOKEN = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot = telebot.TeleBot(TOKEN)

# bot.send_message(662482931, f'''
# 					0000000000000
# 					Bearish divergence.
# 					CD fractals on volumes:
# 					00000000000000000
# 					https://www.binance.com/en/futures/AAVEUSDT/
# 					''', disable_web_page_preview=True)

pic = open('AAVEUSDT.png', 'rb')
bot.send_photo(662482931, pic)