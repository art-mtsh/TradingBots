import datetime
import pandas
import telebot
from multiprocessing import Process  # cpu_count
import time
from requests import get
from Screenshoer_DIV_cdabsolute import screenshoter_DIV
from Screenshoter_DIV_cdinpercent import screenshoter_DIV_d

# --- TELEGRAM ---

TOKEN1 = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot1 = telebot.TeleBot(TOKEN1)

def search_DIVtz(symbol: str, timeinterval: str, risk: float):

	url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=102'
	url_bs = 'https://fapi.binance.com/futures/data/takerlongshortRatio?symbol=' + symbol + '&period=' + timeinterval + '&limit=102'
	data1 = get(url_klines).json()
	data2 = get(url_bs).json()

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
	cHigh = df1['cHigh'].to_numpy()
	cLow = df1['cLow'].to_numpy()
	cClose = df1['cClose'].to_numpy()
	smaClose = df1['cClose'].to_numpy()

	# --- BUY SELL RATIO ---

	D2 = pandas.DataFrame(data2)
	df2 = D2
	df2['buySellRatio'] = df2['buySellRatio'].astype(float)
	df2['buyVol'] = df2['buyVol'].astype(float)
	df2['sellVol'] = df2['sellVol'].astype(float)
	df2['timestamp'] = df2['timestamp'].apply(
		lambda d: datetime.datetime.fromtimestamp(int(d) / 1000).strftime('%H:%M:%S'))

	# Lists:
	cBuyVol = df2['buyVol'].to_numpy()
	cSellVol = df2['sellVol'].to_numpy()

	# --- DELTA/ CUMULATIVE DELTA ---

	cumDeltaValues = [(cBuyVol[0] - cSellVol[0]) / ((cBuyVol[0] + cSellVol[0]) / 100)]

	for i in range(0, len(cSellVol)):
		one_perc_volume = (cBuyVol[i] + cSellVol[i]) / 100
		delta_per = cBuyVol[i] - cSellVol[i]
		delta_percent = delta_per / one_perc_volume
		cumDeltaValues.append(int(cumDeltaValues[-1] + delta_percent))
	cumDeltaValues = cumDeltaValues[1:]

	# cumDeltaValues = []
	# for i in range(1, len(cBuyVol)+1):
	# 	cumDeltaValues.append(int(sum(cBuyVol[0:i])-sum(cSellVol[0:i])))

	# --- SMA ---
	sma = sum(cClose) / len(cClose)

	# --- VOLATILITY ---

	atr = (sum(sum([cHigh - cLow])) / len(cClose))
	atrpercent = atr / (cClose[-1] / 100)
	atrpercent = float('{:.2f}'.format(atrpercent))

	# print(cumDeltaValues)
	# print(cumDeltaValues[-2:-12:-1])
	# print(cumDeltaValues[-11])
	# print(cumDeltaValues[-11:-21:-1])
	# print(cumDeltaValues[-11])

	'''
	# --- Transient zone fractal ---

	maxpoint = 0
	minpoint = 0

	for i in range(2, 78):
		point = -i-9
		# print(cumDeltaValues[-i:-i-10:-1])
		# print(cumDeltaValues[-i-9:-i-19:-1])
		# print(f'Equator: {cumDeltaValues[point]}')
		if max(cumDeltaValues[-i:-i-19:-1]) == cumDeltaValues[point]:
			maxpoint += point
			break

	for i in range(2, 78):
		point = -i - 9
		# print(cumDeltaValues[-i:-i-10:-1])
		# print(cumDeltaValues[-i-9:-i-19:-1])
		# print(f'Equator: {cumDeltaValues[point]}')
		if min(cumDeltaValues[-i:-i-19:-1]) == cumDeltaValues[point]:
			minpoint += point
			break

	print(f'Max point coord: {maxpoint}')
	print(f'Max point high: {cHigh[maxpoint]}')
	print(f'Min point coord: {minpoint}')
	print(f'Minpoint low: {cLow[minpoint]}')
	
	'''

	# --- CUMULATIVE DELTA FRACTAL ---

	for i in range(2, 78):
		point = -i-9
		if max(cumDeltaValues[-i:-i-19:-1]) == cumDeltaValues[point]:
			if cumDeltaValues[-1] >= cumDeltaValues[point] and cHigh[-2] < cHigh[point] and cHigh[-2] < sma and abs(cHigh[point] - cHigh[-2]) > 0.3 * atr and atrpercent > 0.8:
				clean = 0
				for b in range(2, -point):
					if cHigh[-b] >= cHigh[point] or cumDeltaValues[-b] >= cumDeltaValues[point]:
						clean += 1
				if clean == 0:
					bot1.send_message(662482931, f"🔴 SELL ... {symbol} ... {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
												f"\n1xATR: {float('{:.2f}'.format(atrpercent))}% ... "
												f"2xATR: {float('{:.2f}'.format(atrpercent * 2))}% ... "
												f"3xATR: {float('{:.2f}'.format(atrpercent * 3))}%\n"

												f"\nOpen parameters (risk: ${risk}):"
												f"\n    №    | ATR, % |  Price  | $ Size  | ₿ Size  | Stop | $ Fee"

												f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | {cLow[-2]}  $ {int(risk / (atrpercent / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100)) / cLow[-2]))}    "
												f"{float('{:.5f}'.format(cLow[-2] + atr))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) * 0.0008))}"

												f"\n2xATR |  {float('{:.2f}'.format(atrpercent * 2))}%  | {cLow[-2]}  $ {int(risk / (atrpercent * 2 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent * 2 / 100)) / cLow[-2]))}    "
												f"{float('{:.5f}'.format(cLow[-2] + atr * 2))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent * 2 / 100) * 0.0008))}"

												f"\n3xATR |  {float('{:.2f}'.format(atrpercent * 3))}%  | {cLow[-2]}  $ {int(risk / (atrpercent * 3 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent * 3 / 100)) / cLow[-2]))}    "
												f"{float('{:.5f}'.format(cLow[-2] + atr * 3))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent * 3 / 100) * 0.0008))}"

												f"\nhttps://www.binance.com/en/futures/{symbol}/",
									  disable_web_page_preview=True)
					screenshoter_DIV_d(timeinterval=timeinterval, symbol=symbol, direction=" -> SELL", atr1=atr, atr2=atr * 2, atr3=atr * 3)
					print(f"\nSELL ... {symbol} ... {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})\n")
			break

	for i in range(2, 78):
		point = -i-9
		if min(cumDeltaValues[-i:-i - 19:-1]) == cumDeltaValues[point]:
			if cumDeltaValues[-1] <= cumDeltaValues[point] and cLow[-2] > cLow[point] and cLow[-2] > sma and abs(cLow[-2] - cLow[point]) > 0.3 * atr and atrpercent > 0.8:
				clean = 0
				for b in range(2, -point):
					if cLow[-b] <= cLow[point] or cumDeltaValues[-b] <= cumDeltaValues[point]:
						clean += 1
				if clean == 0:
					bot1.send_message(662482931, f"🟢 BUY ... {symbol} ... {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
												f"\n1xATR: {float('{:.2f}'.format(atrpercent))}% ... "
												f"2xATR: {float('{:.2f}'.format(atrpercent * 2))}% ... "
												f"3xATR: {float('{:.2f}'.format(atrpercent * 3))}%\n"

												f"\nOpen parameters (risk: ${risk}):"
												f"\n    №    | ATR, % |  Price  | $ Size  | ₿ Size  | Stop | $ Fee"

												f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | {cHigh[-2]}  $ {int(risk / (atrpercent / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100)) / cHigh[-2]))}    "
												f"{float('{:.5f}'.format(cHigh[-2] - atr))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) * 0.0008))}"

												f"\n2xATR |  {float('{:.2f}'.format(atrpercent * 2))}%  | {cHigh[-2]}  $ {int(risk / (atrpercent * 2 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent * 2 / 100)) / cHigh[-2]))}    "
												f"{float('{:.5f}'.format(cHigh[-2] - atr * 2))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent * 2 / 100) * 0.0008))}"

												f"\n3xATR |  {float('{:.2f}'.format(atrpercent * 3))}%  | {cHigh[-2]}  $ {int(risk / (atrpercent * 3 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent * 3 / 100)) / cHigh[-2]))}    "
												f"{float('{:.5f}'.format(cHigh[-2] - atr * 3))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent * 3 / 100) * 0.0008))}"

												f"\nhttps://www.binance.com/en/futures/{symbol}/",
									  disable_web_page_preview=True)
					screenshoter_DIV_d(timeinterval=timeinterval, symbol=symbol, direction=" -> BUY", atr1=atr, atr2=atr * 2, atr3=atr * 3)
					print(f"\nBUY ... {symbol} ... {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})\n")
			break

# search_DIVtz(symbol='MAGICUSDT', timeinterval='1h', risk=10)