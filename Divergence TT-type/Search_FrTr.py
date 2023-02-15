import datetime
import pandas
import telebot
from requests import get
from Screenshoter_FrTr import screenshoter_FrTr

# --- TELEGRAM ---

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

def search_FrTr(symbol: str, timeinterval: str, risk: float, filter: float):
	# --- DATA ---

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

	threeUps = []
	threeDns = []

	for i in range(0, len(cClose)-40):
		if cClose[-i] < cClose[-i-1] < cClose[-i-2] > cClose[-i-3] > cClose[-i-4]:
			threeUps.append(cHigh[-i-2])
		if cClose[-i] > cClose[-i-1] > cClose[-i-2] < cClose[-i-3] < cClose[-i-4]:
			threeDns.append((cLow[-i-2]))

	if len(threeUps) >=3 and cHigh[-1] < threeUps[0] < threeUps[1] < threeUps[2] and atrpercent > filter and cHigh[-1] < sma:
		bot3.send_message(662482931, f"🔵 {symbol} is trending DOWN, "
									f"ATR50: {float('{:.2f}'.format(atrpercent))}%, "
									f"now: {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
									f"\n1xATR: {float('{:.2f}'.format(atrpercent))}% ... "
									f"2xATR: {float('{:.2f}'.format(atrpercent * 2))}% ... "
									f"3xATR: {float('{:.2f}'.format(atrpercent * 3))}%\n"

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
		screenshoter_FrTr(timeinterval=timeinterval, symbol=symbol, direction="SELL", atr1 = atr, atr2 = atr * 2, atr3 = atr * 3)
		print(f'🔵 {symbol} is trending DOWN, '
			  f'last 50 range: {float("{:.2f}".format(atrpercent))}%, '
			  f'now: {datetime.datetime.now().strftime("%H:%M:%S")} ({timeinterval})')

	if len(threeDns) >=3 and cLow[-1] > threeDns[0] > threeDns[1] > threeDns[2] and atrpercent > filter and cLow[-1] > sma:
		bot3.send_message(662482931, f"🔵 {symbol} is trending UP, "
									f"ATR50: {float('{:.2f}'.format(atrpercent))}%, "
									f"now: {datetime.datetime.now().strftime('%H:%M:%S')} ({timeinterval})"
									f"\n1xATR: {float('{:.2f}'.format(atrpercent))}% ... "
									f"2xATR: {float('{:.2f}'.format(atrpercent * 2))}% ... "
									f"3xATR: {float('{:.2f}'.format(atrpercent * 3))}%\n"

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
		screenshoter_FrTr(timeinterval=timeinterval, symbol=symbol, direction="BUY", atr1 = atr, atr2 = atr * 2, atr3 = atr * 3)
		print(f'🔵 {symbol} is trending UP, '
			  f'last 50 range: {float("{:.2f}".format(atrpercent))}%, '
			  f'now: {datetime.datetime.now().strftime("%H:%M:%S")} ({timeinterval})')