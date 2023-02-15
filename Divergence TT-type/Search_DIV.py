import datetime
import pandas
import telebot
from multiprocessing import Process  # cpu_count
import time
from requests import get
from Screenshoer_DIV import screenshoter_DIV

# --- TELEGRAM ---

TOKEN1 = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot1 = telebot.TeleBot(TOKEN1)

def search_DIV(symbol: str, timeinterval: str, risk: float):

	url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=102'
	url_bs = 'https://fapi.binance.com/futures/data/takerlongshortRatio?symbol=' + symbol + '&period=' + timeinterval + '&limit=51'
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
	cHigh = df1['cHigh'].to_numpy()[50:101]
	cLow = df1['cLow'].to_numpy()[50:101]
	cClose = df1['cClose'].to_numpy()[50:101]
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

	cumDeltaValues = []
	for i in range(1, len(cBuyVol)+1):
		cumDeltaValues.append(int(sum(cBuyVol[0:i])-sum(cSellVol[0:i])))

	# --- SMA ---
	sma = sum(cClose) / len(cClose)

	# --- VOLATILITY ---

	atr = (sum(sum([cHigh - cLow])) / len(cClose))
	atrpercent = atr / (cClose[-1] / 100)
	atrpercent = float('{:.2f}'.format(atrpercent))

	# --- CUMULATIVE DELTA FRACTAL ---

	for i in range(2, 45):
		if cumDeltaValues[-i] < cumDeltaValues[-i - 1] < cumDeltaValues[-i - 2] > cumDeltaValues[-i - 3] > cumDeltaValues[-i - 4]:
			# print(f"High fractals volume: {cVolume[-i - 2]}")
			# print(f"High fractals on high: {cHigh[-i - 2]}")
			if cumDeltaValues[-1] >= cumDeltaValues[-i - 2] and \
				cHigh[-1] < cHigh[-i - 2] and \
				cHigh[-1] < sma and \
				abs(cHigh[-i - 2] - cHigh[-1]) > 0.3 * atr and \
				atrpercent > 0.8:

				clean = 0
				for b in range(2, i + 2):
					if cHigh[-b] >= cHigh[-i - 2] or cumDeltaValues[-b] >= cumDeltaValues[-i - 2]:
						clean += 1
				if clean == 0:
					bot1.send_message(662482931, f"🔴 SELL ... {symbol} ... {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
												f"\n1xATR: {float('{:.2f}'.format(atrpercent))}% ... "
												f"2xATR: {float('{:.2f}'.format(atrpercent * 2))}% ... "
												f"3xATR: {float('{:.2f}'.format(atrpercent * 3))}%\n"

												f"\nOpen parameters (risk: ${risk}):"
												f"\n    №    | ATR, % |  Price  | $ Size  | ₿ Size  | Stop | $ Fee"

												f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | {cLow[-1]}  $ {int(risk / (atrpercent / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100)) / cLow[-1]))}    "
												f"{float('{:.5f}'.format(cLow[-1] + atr))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) * 0.0008))}"

												f"\n2xATR |  {float('{:.2f}'.format(atrpercent * 2))}%  | {cLow[-1]}  $ {int(risk / (atrpercent * 2 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent * 2 / 100)) / cLow[-1]))}    "
												f"{float('{:.5f}'.format(cLow[-1] + atr * 2))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent * 2 / 100) * 0.0008))}"

												f"\n3xATR |  {float('{:.2f}'.format(atrpercent * 3))}%  | {cLow[-1]}  $ {int(risk / (atrpercent * 3 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent * 3 / 100)) / cLow[-1]))}    "
												f"{float('{:.5f}'.format(cLow[-1] + atr * 3))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent * 3 / 100) * 0.0008))}"

												f"\nhttps://www.binance.com/en/futures/{symbol}/",
									  disable_web_page_preview=True)
					screenshoter_DIV(timeinterval=timeinterval, symbol=symbol, direction=" -> SELL", atr1 = atr, atr2 = atr*2, atr3 = atr* 3)
					print(f"\nSELL ... {symbol} ... {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})\n")
			break

	for i in range(2, 45):
		if cumDeltaValues[-i] > cumDeltaValues[-i - 1] > cumDeltaValues[-i - 2] < cumDeltaValues[-i - 3] < cumDeltaValues[-i - 4]:
			# print(f"Low fractals volume: {cVolume[-i - 2]}")
			# print(f"Low fractals on high: {cLow[-i - 2]}")
			if cumDeltaValues[-1] <= cumDeltaValues[-i - 2] and \
				cLow[-1] > cLow[-i - 2] and \
				cLow[-1] > sma and \
				abs(cLow[-1] - cLow[-i - 2]) > 0.3 * atr and \
				atrpercent > 0.8:
				clean = 0
				for b in range(2, i + 2):
					if cLow[-b] <= cLow[-i - 2] or cumDeltaValues[-b] <= cumDeltaValues[-i - 2]:
						clean += 1
				if clean == 0:
					bot1.send_message(662482931, f"🟢 BUY ... {symbol} ... {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
												f"\n1xATR: {float('{:.2f}'.format(atrpercent))}% ... "
												f"2xATR: {float('{:.2f}'.format(atrpercent * 2))}% ... "
												f"3xATR: {float('{:.2f}'.format(atrpercent * 3))}%\n"

												f"\nOpen parameters (risk: ${risk}):"
												f"\n    №    | ATR, % |  Price  | $ Size  | ₿ Size  | Stop | $ Fee"

												f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | {cHigh[-1]}  $ {int(risk / (atrpercent / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100)) / cHigh[-1]))}    "
												f"{float('{:.5f}'.format(cHigh[-1] - atr))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) * 0.0008))}"

												f"\n2xATR |  {float('{:.2f}'.format(atrpercent * 2))}%  | {cHigh[-1]}  $ {int(risk / (atrpercent * 2 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent * 2 / 100)) / cHigh[-1]))}    "
												f"{float('{:.5f}'.format(cHigh[-1] - atr * 2))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent * 2 / 100) * 0.0008))}"

												f"\n3xATR |  {float('{:.2f}'.format(atrpercent * 3))}%  | {cHigh[-1]}  $ {int(risk / (atrpercent * 3 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent * 3 / 100)) / cHigh[-1]))}    "
												f"{float('{:.5f}'.format(cHigh[-1] - atr * 3))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent * 3 / 100) * 0.0008))}"

												f"\nhttps://www.binance.com/en/futures/{symbol}/",
									  disable_web_page_preview=True)
					screenshoter_DIV(timeinterval=timeinterval, symbol=symbol, direction=" -> BUY", atr1 = atr, atr2 = atr * 2, atr3 = atr * 3)
					print(f"\nBUY ... {symbol} ... {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})\n")
			break

# search_DIV(symbol='AAVEUSDT', timeinterval='5m', risk=10)