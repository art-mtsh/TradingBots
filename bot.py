import telebot
import datetime
import pandas
import telebot
import matplotlib.pyplot as plt
from requests import get
# --- TELEGRAM ---

TOKEN1 = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot1 = telebot.TeleBot(TOKEN1)
TOKEN2 = '5947685641:AAEofMStDGj0M0nGhVdlMEEEFP-dOAgOPaw'
bot2 = telebot.TeleBot(TOKEN2)
TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)


bot3.send_message(662482931, "1")

#
# def cumdelta(symbol: str, timeinterval: int, risk: float):
#
# 	# --- DATA CANDLES ---
#
# 	url_bs = 'https://fapi.binance.com/futures/data/takerlongshortRatio?symbol=' + symbol + '&period=' + str(timeinterval) + 'm' + '&limit=51'
#
# 	data2 = get(url_bs).json()
#
# 	# --- BUY SELL RATIO ---
#
# 	D2 = pandas.DataFrame(data2)
# 	df2 = D2
# 	df2['buySellRatio'] = df2['buySellRatio'].astype(float)
# 	df2['buyVol'] = df2['buyVol'].astype(float)
# 	df2['sellVol'] = df2['sellVol'].astype(float)
# 	df2['timestamp'] = df2['timestamp'].apply(
# 		lambda d: datetime.datetime.fromtimestamp(int(d) / 1000).strftime('%H:%M:%S'))
#
# 	print(df2)
#
# 	# cBSR = df2['buySellRatio'].to_numpy()
# 	# cBuyVol = df2['buyVol'].to_numpy()
# 	# cSellVol = df2['sellVol'].to_numpy()
# 	# cTimestamp = df2['timestamp'].to_numpy()
#
#
# # cumdelta('AAVEUSDT', 5, 10)
#
# li = []
# li.append(1)
# print(li)
#
# print(26 % 5)