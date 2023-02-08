import telebot
from datetime import datetime
from time import sleep

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

# while True:
# 	if datetime.now().strftime('%M')[-1] == "5" or datetime.now().strftime('%M')[-1] == "0":
# 		bot.send_message(662482931, f"Time to analyze, its {datetime.now().strftime('%H:%M')} now")
# 		sleep(60)
# 	else:
# 		sleep(60)

# nowis = datetime.now().strftime('%M')
# timeinterval = 30
# timenoww = datetime.now().strftime('%H:') + str(int(datetime.now().strftime('%M'))//timeinterval*timeinterval)
# print(nowis[-2])
# print(nowis[-1])

# bot.send_message(662482931, f"{datetime.now().strftime('%H:%M'))
# while True:
# 	print(timenoww)
# 	sleep(60)

# symbol="AAVEUSDT"
# timeinterval = 60
# print('https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + str(
# 		timeinterval) + 'm' + '&limit=51')

mytime = "12"
tf = 15
print(int(mytime) // tf)