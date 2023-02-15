import pandas
import telebot
from requests import get
from datetime import datetime
from time import sleep

# --- TELEGRAM ---

TOKEN = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot = telebot.TeleBot(TOKEN)

# --- PENDING SEARCH ---

def highvolatility(symbol: str, timeinterval: int, risk: float):

	# --- DATA ---

	url = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + str(timeinterval) + 'm' + '&limit=51'
	data = get(url).json()

	D = pandas.DataFrame(data)
	D.columns = ['open_time', 'cOpen', 'cHigh', 'cLow', 'cClose', 'cVolume', 'close_time', 'qav', 'num_trades',
				 'taker_base_vol', 'taker_quote_vol', 'is_best_match']
	df = D

	df['cOpen'] = df['cOpen'].astype(float)
	df['cHigh'] = df['cHigh'].astype(float)
	df['cLow'] = df['cLow'].astype(float)
	df['cClose'] = df['cClose'].astype(float)
	df['cVolume'] = df['cVolume'].astype(float)

	cOpen = df['cOpen'].to_numpy()
	cHigh = df['cHigh'].to_numpy()
	cLow = df['cLow'].to_numpy()
	cClose = df['cClose'].to_numpy()
	cVolume = df['cVolume'].to_numpy()

	# --- CUMULATIVE DELTA FRACTAL ---
	atr = (sum(sum([cHigh - cLow])) / len(cClose))
	atrpercent = atr / (cClose[-1] / 100)
	atrpercent = float('{:.2f}'.format(atrpercent))
	timeintimeframe = datetime.now().strftime('%H:') + str(int(datetime.now().strftime('%M'))//timeinterval*timeinterval)

	# --- HIGH RANGE BAR ---

	lastbarperc = (abs(cOpen[-1] - cClose[-1])) / (cClose[-1] / 100)
	# bullish = cClose[-1] > cClose[-2] > cClose[-3]
	# bearish = cClose[-1] < cClose[-2] < cClose[-3]

	if lastbarperc > 3:
		bot.send_message(662482931, f"🟡 {symbol} last body range: {float('{:.2f}'.format(lastbarperc))}% ... "
									f"{timeintimeframe} ({timeinterval}m)"
									f"\n1xATR: {float('{:.2f}'.format(atrpercent))}% ... "
									f"2xATR: {float('{:.2f}'.format(atrpercent*2))}% ... "
									f"3xATR: {float('{:.2f}'.format(atrpercent*3))}%\n"
									
									f"\nOpen parameters (risk: ${risk}):"
									f"\n    №    | ATR, % |  $ Size  |  ₿ Size  | $ Fee"
									
									f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | $ {int(risk / (atrpercent / 100))}    "
									f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100))/cClose[-1]))}    "
									f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) *  0.0008))}"
									
									f"\n2xATR |  {float('{:.2f}'.format(atrpercent*2))}%  | $ {int(risk / (atrpercent*2 / 100))}    "
									f"₿ {float('{:.2f}'.format((risk / (atrpercent*2 / 100))/cClose[-1]))}    "
									f"fee {float('{:.2f}'.format(risk / (atrpercent*2 / 100) *  0.0008))}"
																					
									f"\n3xATR |  {float('{:.2f}'.format(atrpercent*3))}%  | $ {int(risk / (atrpercent*3 / 100))}    "
									f"₿ {float('{:.2f}'.format((risk / (atrpercent*3 / 100))/cClose[-1]))}    "
									f"fee {float('{:.2f}'.format(risk / (atrpercent*3 / 100) *  0.0008))}"
									
									f"\nhttps://www.binance.com/en/futures/{symbol}/",
						 disable_web_page_preview=True)

		print(f"{datetime.now().strftime('%b %d, %H:%M')} Check {symbol} ... 2LastBodies = {float('{:.2f}'.format(lastbarperc))}%")

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

while True:
	try:
		rsk = 10
		minutesnow = datetime.now().strftime('%M')

		if minutesnow[-1] == '3' or minutesnow[-1] == '8':
			print(f"{datetime.now().strftime('%H:%M:%S')} M5 start")
			for i in instruments:
				highvolatility(symbol=i, timeinterval=5, risk=rsk)
				print(".", end="")
			print(f"{datetime.now().strftime('%H:%M:%S')} M5 end")

			if minutesnow == '13' or minutesnow == '43':
				print(f"{datetime.now().strftime('%H:%M:%S')} M15 start")
				for i in instruments:
					highvolatility(symbol=i, timeinterval=15, risk=rsk)
					print(".", end="")
				print(f"{datetime.now().strftime('%H:%M:%S')} M15 end")

			elif minutesnow == '28' or minutesnow == '58':
				print(f"{datetime.now().strftime('%H:%M:%S')} M15 start")
				for i in instruments:
					highvolatility(symbol=i, timeinterval=15, risk=rsk)
					print(".", end="")
				print(f"{datetime.now().strftime('%H:%M:%S')} M15 end")


				print(f"{datetime.now().strftime('%H:%M:%S')} M30 start")
				for i in instruments:
					highvolatility(symbol=i, timeinterval=30, risk=rsk)
					print(".", end="")
				print(f"{datetime.now().strftime('%H:%M:%S')} M30 end")

	except:
		sleep(60)
		bot.send_message(662482931, "Bot-2 stopped due an error")


	sleep(10)

# divergence('AAVEUSDT', 5, 1)

