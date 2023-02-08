import telebot
import matplotlib.pyplot as plt
from datetime import datetime
import os
import calendar
import requests
import pandas

TOKEN = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot = telebot.TeleBot(TOKEN)


def sendScreen(timeinterval:int, symbol:str, cumDeltaValues:list, dcoordinate:int, direction:str):

	# --- DATA ---
	slicer = slice(0, -7)
	now = datetime.utcnow()
	unixtime = calendar.timegm(now.utctimetuple())
	since = unixtime
	start = str(since - 60 * 60 * 10)

	url = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + str(symbol) + '&interval=' + str(timeinterval) + 'm' + '&limit=51'
	data = requests.get(url).json()

	D = pandas.DataFrame(data)
	D.columns = ['open_time', 'cOpen', 'cHigh', 'cLow', 'cClose', 'cVolume', 'close_time', 'qav', 'num_trades',
				 'taker_base_vol', 'taker_quote_vol', 'is_best_match']

	df = D

	df['cOpen'] = df['cOpen'].astype(float)
	df['cHigh'] = df['cHigh'].astype(float)
	df['cLow'] = df['cLow'].astype(float)
	df['cClose'] = df['cClose'].astype(float)

	# MAIN CHART
	plt.subplot(2, 1, 1)
	plt.suptitle(symbol + direction)
	stock_prices = df
	up = stock_prices[stock_prices.cClose >= stock_prices.cOpen]
	down = stock_prices[stock_prices.cClose < stock_prices.cOpen]
	col1 = 'green'
	col2 = 'red'
	# Candlestick elements width
	width = .8
	width2 = .07
	# Up candles
	plt.bar(up.index, up.cClose - up.cOpen, width, bottom=up.cOpen, color=col1)
	plt.bar(up.index, up.cHigh - up.cClose, width2, bottom=up.cClose, color=col1)
	plt.bar(up.index, up.cLow - up.cOpen, width2, bottom=up.cOpen, color=col1)
	# Down candles
	plt.bar(down.index, down.cClose - down.cOpen, width, bottom=down.cOpen, color=col2)
	plt.bar(down.index, down.cHigh - down.cOpen, width2, bottom=down.cOpen, color=col2)
	plt.bar(down.index, down.cLow - down.cClose, width2, bottom=down.cClose, color=col2)
	# Grid
	plt.grid(color='grey', linestyle='-', linewidth=0.1)

	# CUMULATIVE DELTA CHART
	plt.subplot(2, 1, 2)
	y1 = cumDeltaValues
	x1 = list(range(0, len(cumDeltaValues)))
	plt.plot(x1, y1, color='red', linewidth=0.7)
	ly = [cumDeltaValues[-1], cumDeltaValues[dcoordinate]]
	lx = [50, 51 + dcoordinate]
	plt.plot(lx, ly, color='green', linewidth=0.5)
	# Grid
	plt.grid(color='grey', linestyle='-', linewidth=0.1)

	# SAVE AND SEND
	plt.savefig(f'{symbol}.png', dpi=600, bbox_inches='tight', pad_inches=0.2)
	pic = open(f'{symbol}.png', 'rb')
	bot.send_photo(662482931, pic)

	# CLEANING
	pic.close()
	os.remove(f'{symbol}.png')
	plt.cla()
	plt.clf()

