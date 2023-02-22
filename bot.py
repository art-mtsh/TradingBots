import datetime
import pandas
import numpy as np
import telebot
from requests import get

# --- TELEGRAM ---

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

def search_FrTr(symbol: str, timeinterval: str, risk: float, filter: float):
	# --- DATA ---

	url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=800'
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

	# Lists:
	cOpen = df1['cOpen'].to_numpy()
	cHigh = df1['cHigh'].to_numpy()
	cLow = df1['cLow'].to_numpy()
	cClose = df1['cClose'].to_numpy()
	cVolume = df1['cVolume'].to_numpy()

	# --- SMA ---
	sma = sum(cClose) / len(cClose)

	# --- VOLATILITY CALC ---
	atr = (sum(sum([cHigh - cLow])) / len(cClose))
	atrpercent = atr / (cClose[-1] / 100)
	atrpercent = float('{:.2f}'.format(atrpercent))
	# timeintimeframe = datetime.now().strftime('%H:') + str(int(datetime.now().strftime('%M')) // timeinterval * timeinterval)

	# --- HIGH RANGE BAR ---

	threeUps = 0
	threeDns = 0

	for i in range(2, 550):
		point = -i-120
		if max(cHigh[-i:-i-360:-1]) == cHigh[point]:
			threeUps += cHigh[point]
			break

	for i in range(2, 550):
		point = -i-9
		if min(cLow[-i:-i-360:-1]) == cLow[point]:
			threeDns += cLow[point]
			break

	print(threeUps)
	print(threeDns)

	# print(cHigh[-122])
	# print(len(cHigh[-2:-122:-1]))
	# print(len(cHigh[-2:-362:-1]))


search_FrTr(symbol='AAVEUSDT', timeinterval='1m', risk=10, filter=0.2)