import datetime
import pandas
import numpy as np
import telebot
from requests import get
from Screenshoter_FrTr import screenshoter_FrTr
import talib as ta

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
	atr = (sum(sum([cHigh[700:] - cLow[700:]])) / len(cClose[700:]))
	atrpercent = atr / (cClose[-1] / 100)
	atrpercent = float('{:.2f}'.format(atrpercent))
	# timeintimeframe = datetime.now().strftime('%H:') + str(int(datetime.now().strftime('%M')) // timeinterval * timeinterval)

	# --- LINEAR REGRESSION ANGLE ---
	slope_angle = list(ta.LINEARREG_ANGLE(cClose, 20))

	# --- DECISION MAKING ---

	# if len(threeUps) >=3 and cHigh[-1] < threeUps[0] < threeUps[1] < threeUps[2] and atrpercent > filter and cHigh[-1] < sma:
	# if slope_angle[-1] < -15:
	for i in range(2, 550):
		point = -i-120
		if max(cHigh[-i:-i-360:-1]) == cHigh[point]:
			clean = 0
			for b in range(2, -point):
				if cHigh[-b] <= cHigh[point]:
					clean += 1
			distance_r = (cHigh[point] - cClose[-1]) / (cClose[-1] / 100)
			distance_r = float('{:.2f}'.format(distance_r))
			if clean == 0 and 1 > distance_r > 0 and atrpercent > 0.3:
				bot3.send_message(662482931, f"🔵 {symbol} resistance in {distance_r}% at {cHigh[point]}, "
											f"now: {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
				
											f"\nOpen parameters (risk: ${risk}):"
											f"\n    №    | ATR, % |  $ Size  |  ₿ Size  | $ Fee"
			
											f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | $ {int(risk / (atrpercent / 100))}    "
											f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100)) / cClose[-1]))}    "
											f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) * 0.0008))}"
			
											f"\n2xATR |  {float('{:.2f}'.format(atrpercent * 2))}%  | $ {int(risk / (atrpercent * 2 / 100))}    "
											f"₿ {float('{:.2f}'.format((risk / (atrpercent * 2 / 100)) / cClose[-1]))}    "
											f"fee {float('{:.2f}'.format(risk / (atrpercent * 2 / 100) * 0.0008))}"
			
											f"\n3xATR |  {float('{:.2f}'.format(atrpercent * 3))}%  | $ {int(risk / (atrpercent * 3 / 100))}    "
											f"₿ {float('{:.2f}'.format((risk / (atrpercent * 3 / 100)) / cClose[-1]))}    "
											f"fee {float('{:.2f}'.format(risk / (atrpercent * 3 / 100) * 0.0008))}"
			
											f"\nhttps://www.binance.com/en/futures/{symbol}/",
								  disable_web_page_preview=True)
				screenshoter_FrTr(timeinterval=timeinterval, symbol=symbol, direction="resistance", distancetoSR=distance_r, atr1 = atr, atr2 = atr * 2, atr3 = atr * 3, point=cHigh[point])
				print(f'🔵 {symbol} distance to resistance: {distance_r}%, '
					  f'now: {datetime.datetime.now().strftime("%H:%M:%S")} ({timeinterval})')

	# if len(threeDns) >=3 and cLow[-1] > threeDns[0] > threeDns[1] > threeDns[2] and atrpercent > filter and cLow[-1] > sma:
	# if slope_angle[-1] > 15:
	for i in range(2, 400):
		point = -i - 120
		if min(cLow[-i:-i - 360:-1]) == cLow[point]:
			clean = 0
			for b in range(2, -point):
				if cLow[-b] <= cLow[point]:
					clean += 1
			distance_s = (cClose[-1] - cLow[point]) / (cClose[-1] / 100)
			distance_s = float('{:.2f}'.format(distance_s))
			if clean == 0 and 1 > distance_s > 0 and atrpercent > 0.3:
				bot3.send_message(662482931, f"🔵 {symbol} support in {distance_s}% at {cLow[point]}, "
											f"now: {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
			
											f"\nOpen parameters (risk: ${risk}):"
											f"\n    №    | ATR, % |  $ Size  |  ₿ Size  | $ Fee"
			
											f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | $ {int(risk / (atrpercent / 100))}    "
											f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100)) / cClose[-1]))}    "
											f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) * 0.0008))}"
			
											f"\n2xATR |  {float('{:.2f}'.format(atrpercent * 2))}%  | $ {int(risk / (atrpercent * 2 / 100))}    "
											f"₿ {float('{:.2f}'.format((risk / (atrpercent * 2 / 100)) / cClose[-1]))}    "
											f"fee {float('{:.2f}'.format(risk / (atrpercent * 2 / 100) * 0.0008))}"
			
											f"\n3xATR |  {float('{:.2f}'.format(atrpercent * 3))}%  | $ {int(risk / (atrpercent * 3 / 100))}    "
											f"₿ {float('{:.2f}'.format((risk / (atrpercent * 3 / 100)) / cClose[-1]))}    "
											f"fee {float('{:.2f}'.format(risk / (atrpercent * 3 / 100) * 0.0008))}"
			
											f"\nhttps://www.binance.com/en/futures/{symbol}/",
								  disable_web_page_preview=True)
				screenshoter_FrTr(timeinterval=timeinterval, symbol=symbol, direction="support", distancetoSR=distance_s, atr1 = atr, atr2 = atr * 2, atr3 = atr * 3, point=cLow[point])
				print(f'🔵 {symbol} distance to support: {distance_s}%, '
					  f'now: {datetime.datetime.now().strftime("%H:%M:%S")} ({timeinterval})')

# search_FrTr(symbol='AAVEUSDT', timeinterval='1h', risk=10, filter=0.2)