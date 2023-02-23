import datetime
import pandas
import telebot
from multiprocessing import Process  # cpu_count
import time
from requests import get
from Screenshoter_HR import screenshoter_HR

# --- TELEGRAM ---

TOKEN2 = '5947685641:AAEofMStDGj0M0nGhVdlMEEEFP-dOAgOPaw'
bot2 = telebot.TeleBot(TOKEN2)

def search_HR(symbol: str, timeinterval: str, risk: float, filter: float):
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
	atrpercent = atr / (cClose[-2] / 100)
	atrpercent = float('{:.2f}'.format(atrpercent))
	# timeintimeframe = datetime.now().strftime('%H:') + str(int(datetime.now().strftime('%M')) // timeinterval * timeinterval)

	# --- HIGH RANGE BAR ---

	lastbarperc = (abs(cOpen[-2] - cClose[-2])) / (cClose[-2] / 100)
	# bullish = cClose[-1] > cClose[-2] > cClose[-3]
	# bearish = cClose[-1] < cClose[-2] < cClose[-3]

	if lastbarperc > filter and atrpercent > 0.0 and (cClose[-2] > cOpen[-2] > sma or cClose[-2] < cOpen[-2] < sma):
		bot2.send_message(662482931, f"🟡 {symbol} last range: {float('{:.2f}'.format(lastbarperc))}%, "
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
		screenshoter_HR(timeinterval=timeinterval, symbol=symbol, atr1 = atr, atr2 = atr * 2, atr3 = atr * 3)
		print(f'{symbol} last range: {float("{:.2f}".format(lastbarperc))}%, '
			  f'last 50 range: {float("{:.2f}".format(atrpercent))}%, '
			  f'now: {datetime.datetime.now().strftime("%H:%M:%S")} ({timeinterval})')

