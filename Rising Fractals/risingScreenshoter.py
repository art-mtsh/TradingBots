import datetime
import pandas
import telebot
import matplotlib.pyplot as plt
from requests import get
from os import remove

# --- TELEGRAM ---

TOKEN1 = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot1 = telebot.TeleBot(TOKEN1)
TOKEN2 = '5947685641:AAEofMStDGj0M0nGhVdlMEEEFP-dOAgOPaw'
bot2 = telebot.TeleBot(TOKEN2)
TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

# --- PENDING SEARCH ---

def sendScreen3(timeinterval:str, symbol:str, direction: str):

	# --- DATA CANDLES ---

	url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=100'
	data1 = get(url_klines).json()

	# --- K-LINE ---

	D1 = pandas.DataFrame(data1)
	D1.columns = ['open_time',
				  'cOpen',
				  'cHigh',
				  'cLow',
				  'cClose',
				  'cVolume',
				  'close_time',
				  'qav',
				  'num_trades',
				  'taker_base_vol',
				  'taker_quote_vol',
				  'is_best_match']
	df1 = D1
	df1['cOpen'] = df1['cOpen'].astype(float)
	df1['cHigh'] = df1['cHigh'].astype(float)
	df1['cLow'] = df1['cLow'].astype(float)
	df1['cClose'] = df1['cClose'].astype(float)
	df1['cVolume'] = df1['cVolume'].astype(float)
	df1['open_time'] = df1['open_time'].apply(
		lambda d: datetime.datetime.fromtimestamp(int(d) / 1000).strftime('%H:%M:%S'))

	# --- PLOTS ---
	plt.suptitle(symbol + ' at ' + datetime.datetime.now().strftime('%H:%M:%S') + f" ({timeinterval})" + ' is ' + direction)

	stock_prices = df1
	up = stock_prices[stock_prices.cClose >= stock_prices.cOpen]
	down = stock_prices[stock_prices.cClose < stock_prices.cOpen]

	# Up candles
	plt.bar(x=up.index, height=up.cClose - up.cOpen, width = 0.9, bottom=up.cOpen, color='green')
	plt.bar(x=up.index, height=up.cHigh - up.cClose, width = 0.05, bottom=up.cClose, color='green')
	plt.bar(x=up.index, height=up.cLow - up.cOpen, width = 0.05, bottom=up.cOpen, color='green')
	# Down candles
	plt.bar(x=down.index, height=down.cClose - down.cOpen, width = 0.9, bottom=down.cOpen, color='red')
	plt.bar(x=down.index, height=down.cHigh - down.cOpen, width = 0.05, bottom=down.cOpen, color='red')
	plt.bar(x=down.index, height=down.cLow - down.cClose, width = 0.05, bottom=down.cClose, color='red')
	# grid
	plt.grid(color='grey', linestyle='-', linewidth=0.1)

	# plt.show()

	# SAVE AND SEND
	plt.savefig(f'{symbol}.png', dpi=400, bbox_inches='tight', pad_inches=0.2)
	pic = open(f'{symbol}.png', 'rb')
	bot3.send_photo(662482931, pic)

	# CLEANING
	pic.close()
	remove(f'{symbol}.png')
	plt.cla()
	plt.clf()

# sendScreen3(timeinterval='1m', symbol='AAVEUSDT', direction='bullish')