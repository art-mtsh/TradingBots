import datetime
import pandas
import telebot
# from multiprocessing import Process  # cpu_count
import time
from requests import get
from risingScreenshoter import sendScreen3

# --- TELEGRAM ---

TOKEN1 = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot1 = telebot.TeleBot(TOKEN1)
TOKEN2 = '5947685641:AAEofMStDGj0M0nGhVdlMEEEFP-dOAgOPaw'
bot2 = telebot.TeleBot(TOKEN2)
TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

def risingfractals(symbol: str, timeinterval: str, risk: float, filter: float):
	# --- DATA ---

	url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=52'
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


	# --- VOLATILITY CALC ---
	atr = (sum(sum([cHigh - cLow])) / len(cClose))
	atrpercent = atr / (cClose[-1] / 100)
	atrpercent = float('{:.2f}'.format(atrpercent))
	# timeintimeframe = datetime.now().strftime('%H:') + str(int(datetime.now().strftime('%M')) // timeinterval * timeinterval)

	# --- HIGH RANGE BAR ---

	threeUps = []
	threeDns = []

	for i in range(0, len(cClose)-5):
		if cClose[-i] < cClose[-i-1] < cClose[-i-2] > cClose[-i-3] > cClose[-i-4]:
			threeUps.append(cHigh[-i-2])
		if cClose[-i] > cClose[-i-1] > cClose[-i-2] < cClose[-i-3] < cClose[-i-4]:
			threeDns.append((cLow[-i-2]))

	if len(threeUps) >=3 and cHigh[-1] < threeUps[0] < threeUps[1] < threeUps[2] and atrpercent > filter:
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
		sendScreen3(timeinterval=timeinterval, symbol=symbol, direction="bearish")
		print(f'🔵 {symbol} is trending DOWN, '
			  f'last 50 range: {float("{:.2f}".format(atrpercent))}%, '
			  f'now: {datetime.datetime.now().strftime("%H:%M:%S")} ({timeinterval})')

	if len(threeDns) >=3 and cLow[-1] > threeDns[0] > threeDns[1] > threeDns[2] and atrpercent > filter:
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
		sendScreen3(timeinterval=timeinterval, symbol=symbol, direction="bullish")
		print(f'🔵 {symbol} is trending UP, '
			  f'last 50 range: {float("{:.2f}".format(atrpercent))}%, '
			  f'now: {datetime.datetime.now().strftime("%H:%M:%S")} ({timeinterval})')

instruments = ["1000LUNCBUSD",
				   "1000LUNCUSDT",
				   "1000SHIBUSDT",
				   "1000XECUSDT",
				   "1INCHUSDT",
				   "AAVEUSDT",
				   "ADAUSDT",
				   "ALGOUSDT",
				   "ALICEUSDT",
				   "ALPHAUSDT",
				   "ANKRUSDT",
				   "ANTUSDT",
				   "APEUSDT",
				   "API3USDT",
				   "APTUSDT",
				   "ARPAUSDT",
				   "ARUSDT",
				   "ATAUSDT",
				   "ATOMUSDT",
				   "AUDIOUSDT",
				   "AVAXUSDT",
				   "AXSUSDT",
				   "BAKEUSDT",
				   "BALUSDT",
				   "BANDUSDT",
				   "BATUSDT",
				   "BCHUSDT",
				   "BELUSDT",
				   "BLUEBIRDUSDT",
				   "BLZUSDT",
				   "BNBUSDT",
				   "BNXUSDT",
				   # "BTCDOMUSDT",
				   # "BTCUSDT",
				   # "BTCUSDT",
				   "C98USDT",
				   "CELOUSDT",
				   "CELRUSDT",
				   "CHRUSDT",
				   "CHZUSDT",
				   "COMPUSDT",
				   "COTIUSDT",
				   "CRVUSDT",
				   "CTKUSDT",
				   "CTSIUSDT",
				   "CVXUSDT",
				   "DARUSDT",
				   "DASHUSDT",
				   # "DEFIUSDT",
				   "DENTUSDT",
				   "DGBUSDT",
				   "DOGEUSDT",
				   "DOTUSDT",
				   "DUSKUSDT",
				   "DYDXUSDT",
				   "EGLDUSDT",
				   "ENJUSDT",
				   "ENSUSDT",
				   # "EOSUSDT",
				   "ETCUSDT",
				   # "ETHUSDT",
				   # "ETHUSDT",
				   "FETUSDT",
				   "FILUSDT",
				   "FLMUSDT",
				   "FLOWUSDT",
				   "FOOTBALLUSDT",
				   "FTMUSDT",
				   "FXSUSDT",
				   "GALAUSDT",
				   "GALUSDT",
				   "GMTUSDT",
				   "GRTUSDT",
				   "GTCUSDT",
				   "HBARUSDT",
				   "HIGHUSDT",
				   "HNTUSDT",
				   "HOOKUSDT",
				   "HOTUSDT",
				   "ICPUSDT",
				   "ICXUSDT",
				   "IMXUSDT",
				   "INJUSDT",
				   "IOSTUSDT",
				   "IOTAUSDT",
				   "IOTXUSDT",
				   "JASMYUSDT",
				   "KAVAUSDT",
				   "KLAYUSDT",
				   "KNCUSDT",
				   "KSMUSDT",
				   "LDOUSDT",
				   "LINAUSDT",
				   "LINKUSDT",
				   "LITUSDT",
				   "LPTUSDT",
				   "LRCUSDT",
				   "LTCUSDT",
				   "LUNA2USDT",
				   "MAGICUSDT",
				   "MANAUSDT",
				   "MASKUSDT",
				   "MATICUSDT",
				   "MINAUSDT",
				   "MKRUSDT",
				   "MTLUSDT",
				   "NEARUSDT",
				   "NEOUSDT",
				   "NKNUSDT",
				   "OCEANUSDT",
				   "OGNUSDT",
				   "OMGUSDT",
				   "ONEUSDT",
				   "ONTUSDT",
				   "OPUSDT",
				   "PEOPLEUSDT",
				   "QNTUSDT",
				   "QTUMUSDT",
				   "REEFUSDT",
				   "RENUSDT",
				   "RLCUSDT",
				   "RNDRUSDT",
				   "ROSEUSDT",
				   "RSRUSDT",
				   "RUNEUSDT",
				   "RVNUSDT",
				   "SANDUSDT",
				   "SFPUSDT",
				   "SKLUSDT",
				   "SNXUSDT",
				   "SOLUSDT",
				   # "SPELLUSDT",
				   "STGUSDT",
				   "STMXUSDT",
				   "STORJUSDT",
				   "SUSHIUSDT",
				   "SXPUSDT",
				   "THETAUSDT",
				   "TOMOUSDT",
				   "TRBUSDT",
				   "TRXUSDT",
				   "TUSDT",
				   "UNFIUSDT",
				   "UNIUSDT",
				   "VETUSDT",
				   "WAVESUSDT",
				   "WOOUSDT",
				   # "XEMUSDT",
				   "XLMUSDT",
				   "XMRUSDT",
				   "XRPUSDT",
				   "XTZUSDT",
				   # "YFIUSDT",
				   "ZECUSDT",
				   "ZENUSDT",
				   "ZILUSDT",
				   "ZRXUSDT"]
risk = 10

while True:
	try:
		# if datetime.datetime.now().strftime('%M')[-1] == '0':

		print(f"{datetime.datetime.now().strftime('%H:%M:%S')} High-range search on m1: start")
		for i in instruments:
			risingfractals(symbol=i, timeinterval='1m', risk=risk, filter=0.5)
			print(".", end="")
		print(f"\n{datetime.datetime.now().strftime('%H:%M:%S')} High-range search on m1: stop")

	except:
		time.sleep(60)
		bot3.send_message(662482931, "Bot-1 stopped due an error")

	time.sleep(120)