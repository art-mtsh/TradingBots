import datetime
import pandas
import telebot
import matplotlib.pyplot as plt
from requests import get
from os import remove

# --- TELEGRAM ---

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

# --- PENDING SEARCH ---

def screenshoter_FrTr(timeinterval:str, symbol:str, direction: str, atr1: float, atr2: float, atr3: float):

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

	cClose = df1['cClose'].to_numpy()

	# --- PLOTS ---
	plt.suptitle(symbol + ' look for ' + direction + ' at ' + datetime.datetime.now().strftime('%H:%M:%S') + f' ({timeinterval})')

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
	# ATRs
	ly1 = [cClose[-1] - atr1, cClose[-1] - atr1]
	ly2 = [cClose[-1] - atr2, cClose[-1] - atr2]
	ly3 = [cClose[-1] - atr3, cClose[-1] - atr3]
	ly4 = [cClose[-1] + atr1, cClose[-1] + atr1]
	ly5 = [cClose[-1] + atr2, cClose[-1] + atr2]
	ly6 = [cClose[-1] + atr3, cClose[-1] + atr3]
	lx = [101, 110]
	plt.plot(lx, ly1, color='green', linewidth=0.6)
	plt.plot(lx, ly2, color='green', linewidth=0.6)
	plt.plot(lx, ly3, color='green', linewidth=0.6)
	plt.plot(lx, ly4, color='red', linewidth=0.6)
	plt.plot(lx, ly5, color='red', linewidth=0.6)
	plt.plot(lx, ly6, color='red', linewidth=0.6)

	# plt.show()

	# SAVE AND SEND
	plt.savefig(f'FT{symbol}{timeinterval}.png', dpi=400, bbox_inches='tight', pad_inches=0.2)
	pic = open(f'FT{symbol}{timeinterval}.png', 'rb')
	bot3.send_photo(662482931, pic)

	# CLEANING
	pic.close()
	remove(f'FT{symbol}{timeinterval}.png')
	plt.cla()
	plt.clf()

# sendScreen3(timeinterval='30m', symbol='AAVEUSDT')