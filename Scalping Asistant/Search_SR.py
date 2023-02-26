import datetime
import pandas
import telebot
from requests import get
from Screenshoter_SR import screenshoter_FrTr
import talib as ta

# --- TELEGRAM ---

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

def search_SR(symbol: str, timeinterval: str, risk: float, searchdistance: float, atrfilter: float):
	# --- DATA ---

	url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=1000'
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
	atr = (sum(sum([cHigh[950:] - cLow[950:]])) / len(cClose[950:]))
	atrpercent = atr / (cClose[-1] / 100)
	atrpercent = float('{:.2f}'.format(atrpercent))
	# timeintimeframe = datetime.now().strftime('%H:') + str(int(datetime.now().strftime('%M')) // timeinterval * timeinterval)

	# --- LINEAR REGRESSION ANGLE ---
	slope_angle = list(ta.LINEARREG_ANGLE(cClose, 20))

	# --- DECISION MAKING ---

	for i in range(2, 635):
		point = -i-120
		if max(cHigh[point:-i-360:-1]) == cHigh[point]:
			clean = 0
			doubletouchup = 0
			for b in range(2, -point):
				if cHigh[-b] > cHigh[point] + cHigh[point] * 0.0015:
					clean += 1

			for b in range(20, -point - 20):
				if cHigh[point] + cHigh[point] * 0.0015 >= cHigh[-b] >= cHigh[point] - cHigh[point] * 0.0015:
					doubletouchup += 1

			distance_r = abs((cHigh[point] - cClose[-1]) / (cClose[-1] / 100))
			distance_r = float('{:.2f}'.format(distance_r))
			if clean == 0 and searchdistance > distance_r > 0 and atrpercent > atrfilter and doubletouchup > 0:
				bot3.send_message(662482931, f"🔵 {symbol} resistance in {distance_r}% at {cHigh[point]}, "
											f"now: {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
				
											f"\nOpen parameters (risk: ${risk}):"
											f"\n    №    | ATR, % |  $ Size  |  ₿ Size  | $ Fee"
			
											f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | $ {int(risk / (atrpercent / 100))}    "
											f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100)) / cHigh[point]))}    "
											f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) * 0.0008))}"
											 
											f"\nRISK/5 |  1.00%  | $ {int(risk / (1 / 100) / 5)}    "
											f"₿ {int((risk / (1 / 100)) / cHigh[point] / 5)}    "
											f"fee {float('{:.2f}'.format(risk / (1 / 100) * 0.0008 / 5))}"

											f"\nRISK    |  1.00%  | $ {int(risk / (1 / 100))}    "
											f"₿ {int((risk / (1 / 100)) / cHigh[point])}    "
											f"fee {float('{:.2f}'.format(risk / (1 / 100) * 0.0008))}"
			
											# f"\n3xATR |  {float('{:.2f}'.format(atrpercent * 3))}%  | $ {int(risk / (atrpercent * 3 / 100))}    "
											# f"₿ {float('{:.2f}'.format((risk / (atrpercent * 3 / 100)) / cHigh[point]))}    "
											# f"fee {float('{:.2f}'.format(risk / (atrpercent * 3 / 100) * 0.0008))}"
											# 
											# f"\n5xATR |  {float('{:.2f}'.format(atrpercent * 5))}%  | $ {int(risk / (atrpercent * 5 / 100))}    "
											# f"₿ {float('{:.2f}'.format((risk / (atrpercent * 5 / 100)) / cHigh[point]))}    "
											# f"fee {float('{:.2f}'.format(risk / (atrpercent * 5 / 100) * 0.0008))}"
			
											f"\nhttps://www.binance.com/en/futures/{symbol}/",
								  disable_web_page_preview=True)
				screenshoter_FrTr(timeinterval=timeinterval, symbol=symbol, direction="resistance", distancetoSR=distance_r, atr1 = atr, atr2 = atr * 3, atr3 = atr * 5, point=cHigh[point])
				print(f'{symbol} distance to resistance: {distance_r}%, '
					  f'now: {datetime.datetime.now().strftime("%H:%M:%S")} ({timeinterval})')
				break

	for i in range(2, 635):
		point = -i - 120
		if min(cLow[point:-i - 360:-1]) == cLow[point]:
			clean = 0
			doubletouchdn = 0
			for b in range(2, -point):
				if cLow[-b] < cLow[point] - cLow[point] * 0.0015:
					clean += 1

			for b in range(20, -point - 20):
				if cLow[point] - cLow[point] * 0.0015 <= cLow[-b] <= cLow[point] + cLow[point] * 0.0015:
					doubletouchdn += 1
			distance_s = abs((cClose[-1] - cLow[point]) / (cClose[-1] / 100))
			distance_s = float('{:.2f}'.format(distance_s))
			if clean == 0 and searchdistance > distance_s > 0 and atrpercent > atrfilter and doubletouchdn > 0:
				bot3.send_message(662482931, f"🔵 {symbol} support in {distance_s}% at {cLow[point]}, "
											f"now: {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
			
											f"\nOpen parameters (risk: ${risk}):"
											f"\n    №    | ATR, % |  $ Size  |  ₿ Size  | $ Fee"
			
											f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | $ {int(risk / (atrpercent / 100))}    "
											f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100)) / cLow[point]))}    "
											f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) * 0.0008))}"
											 
											f"\nRISK/5 |  1.00%  | $ {int(risk / (1 / 100) / 5)}    "
											f"₿ {int((risk / (1 / 100)) / cLow[point] / 5)}    "
											f"fee {float('{:.2f}'.format(risk / (1 / 100) * 0.0008 / 5))}"
											 
											f"\nRISK    |  1.00%  | $ {int(risk / (1 / 100))}    "
											f"₿ {int((risk / (1 / 100)) / cLow[point])}    "
											f"fee {float('{:.2f}'.format(risk / (1 / 100) * 0.0008))}"
											 
											# f"\n3xATR |  {float('{:.2f}'.format(atrpercent * 3))}%  | $ {int(risk / (atrpercent * 3 / 100))}    "
											# f"₿ {float('{:.2f}'.format((risk / (atrpercent * 3 / 100)) / cLow[point]))}    "
											# f"fee {float('{:.2f}'.format(risk / (atrpercent * 3 / 100) * 0.0008))}"
											# 
											# f"\n5xATR |  {float('{:.2f}'.format(atrpercent * 5))}%  | $ {int(risk / (atrpercent * 5 / 100))}    "
											# f"₿ {float('{:.2f}'.format((risk / (atrpercent * 5 / 100)) / cLow[point]))}    "
											# f"fee {float('{:.2f}'.format(risk / (atrpercent * 5 / 100) * 0.0008))}"
			
											f"\nhttps://www.binance.com/en/futures/{symbol}/",
								  disable_web_page_preview=True)
				screenshoter_FrTr(timeinterval=timeinterval, symbol=symbol, direction="support", distancetoSR=distance_s, atr1 = atr, atr2 = atr * 3, atr3 = atr * 5, point=cLow[point])
				print(f'{symbol} distance to support: {distance_s}%, '
					  f'now: {datetime.datetime.now().strftime("%H:%M:%S")} ({timeinterval})')
				break

# search_FrTr(symbol='AAVEUSDT', timeinterval='1h', risk=10, filter=0.2)