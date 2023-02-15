import pandas
import telebot
from requests import get
from datetime import datetime
from TWscreenshoter import sendScreen
from time import sleep

# --- TELEGRAM ---

TOKEN = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot = telebot.TeleBot(TOKEN)

# --- PENDING SEARCH ---

def divergence(symbol: str, timeinterval: int, risk: float):

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

	# --- CUMULATIVE DELTA ARRAY ---
	cumDeltaPeriod = 51
	cumDeltaValues = []

	for i in range(cumDeltaPeriod, 0, -1):

		if abs(cOpen[-i] - cClose[-i]) / ((cHigh[-i] - cLow[-i]) / 100) > 20 and \
			cClose[-i] >= cOpen[-i] and \
			cClose[-i] - cOpen[-i] + 2 * (cHigh[-i] - cClose[-i]) + 2 * (cOpen[-i] - cLow[-i]) > 0:

			U1 = cVolume[-i] * (cHigh[-i] - cLow[-i]) / (cClose[-i] - cOpen[-i] + 2 * (cHigh[-i] - cClose[-i]) + 2 * (cOpen[-i] - cLow[-i]))

		else:
			U1 = 0.0

		if abs(cOpen[-i] - cClose[-i]) / ((cHigh[-i] - cLow[-i]) / 100) > 20 and \
			cClose[-i] < cOpen[-i] and \
			cOpen[-i] - cClose[-i] + 2 * (cHigh[-i] - cOpen[-i]) + 2 * (cClose[-i] - cLow[-i]) > 0:

			D1 = cVolume[-i] * (cHigh[-i] - cLow[-i]) / (
					cOpen[-i] - cClose[-i] + 2 * (cHigh[-i] - cOpen[-i]) + 2 * (cClose[-i] - cLow[-i]))

		else:
			D1 = 0.0

		if cClose[-i] >= cOpen[-i]:
			if cumDeltaValues == []:
				cumDeltaValues.append(int(U1))
			else:
				cumDeltaValues.append(cumDeltaValues[-1] + int(U1))

		elif cClose[-i] < cOpen[-i]:
			if cumDeltaValues == []:
				cumDeltaValues.append(-int(D1))
			else:
				cumDeltaValues.append(cumDeltaValues[-1] - int(D1))

	# --- CUMULATIVE DELTA FRACTAL ---
	atr = (sum(sum([cHigh - cLow])) / len(cClose))
	atrpercent = atr / (cClose[-1] / 100)
	atrpercent = float('{:.2f}'.format(atrpercent))
	timeintimeframe = datetime.now().strftime('%H:') + str(int(datetime.now().strftime('%M'))//timeinterval*timeinterval)

	for i in range(2, cumDeltaPeriod - 5):
		if cumDeltaValues[-i] < cumDeltaValues[-i - 1] < cumDeltaValues[-i - 2] > cumDeltaValues[-i - 3] > cumDeltaValues[-i - 4]:
			if cumDeltaValues[-1] >= cumDeltaValues[-i - 2] and cHigh[-1] < cHigh[-i - 2] and abs(cHigh[-i - 2] - cHigh[-1]) > 0.3 * atr and atrpercent > 0.8:
				clean = 0
				for b in range(2, i + 2):
					if cHigh[-b] >= cHigh[-i - 2] or cumDeltaValues[-b] >= cumDeltaValues[-i - 2]:
						clean += 1
				if clean == 0:
					bot.send_message(662482931, f"🔴 SELL ... {symbol} ... {timeintimeframe} ({timeinterval}m)"
												f"\n1xATR: {float('{:.2f}'.format(atrpercent))}% ... "
												f"2xATR: {float('{:.2f}'.format(atrpercent*2))}% ... "
												f"3xATR: {float('{:.2f}'.format(atrpercent*3))}%\n"
												
												f"\nOpen parameters (risk: ${risk}):"
												f"\n    №    | ATR, % |  Price  | $ Size  | ₿ Size  | Stop | $ Fee"
												
												f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | {cLow[-1]}  $ {int(risk / (atrpercent / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100))/cLow[-1]))}    "
												f"{float('{:.5f}'.format(cLow[-1] + atr))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) *  0.0008))}"
												
												f"\n2xATR |  {float('{:.2f}'.format(atrpercent*2))}%  | {cLow[-1]}  $ {int(risk / (atrpercent*2 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent*2 / 100))/cLow[-1]))}    "
												f"{float('{:.5f}'.format(cLow[-1] + atr*2))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent*2 / 100) *  0.0008))}"
																								
												f"\n3xATR |  {float('{:.2f}'.format(atrpercent*3))}%  | {cLow[-1]}  $ {int(risk / (atrpercent*3 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent*3 / 100))/cLow[-1]))}    "
												f"{float('{:.5f}'.format(cLow[-1] + atr*3))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent*3 / 100) *  0.0008))}"
									
												f"\nhttps://www.binance.com/en/futures/{symbol}/",
									 disable_web_page_preview=True)
					sendScreen(timeinterval=timeinterval, symbol=symbol, cumDeltaValues=cumDeltaValues, dcoordinate=int(-i - 2), direction=" -> SELL")
					print(f"{datetime.now().strftime('%b %d, %H:%M')} Bearish {symbol}. CD fractal on {cVolume[-i - 2]} volume")
			break

	for i in range(2, cumDeltaPeriod - 5):
		if cumDeltaValues[-i] > cumDeltaValues[-i - 1] > cumDeltaValues[-i - 2] < cumDeltaValues[-i - 3] < cumDeltaValues[-i - 4]:
			if cumDeltaValues[-1] <= cumDeltaValues[-i - 2] and cLow[-1] > cLow[-i - 2] and abs(cLow[-1] - cLow[-i - 2]) > 0.3 * atr and atrpercent > 0.8:
				clean = 0
				for b in range(2, i + 2):
					if cLow[-b] <= cLow[-i - 2] or cumDeltaValues[-b] <= cumDeltaValues[-i - 2]:
						clean += 1
				if clean == 0:
					bot.send_message(662482931, f"🟢 BUY ... {symbol} ... {timeintimeframe} ({timeinterval}m)"
												f"\n1xATR: {float('{:.2f}'.format(atrpercent))}% ... "
												f"2xATR: {float('{:.2f}'.format(atrpercent*2))}% ... "
												f"3xATR: {float('{:.2f}'.format(atrpercent*3))}%\n"
												
												f"\nOpen parameters (risk: ${risk}):"
												f"\n    №    | ATR, % |  Price  | $ Size  | ₿ Size  | Stop | $ Fee"
												
												f"\n1xATR |  {float('{:.2f}'.format(atrpercent))}%  | {cHigh[-1]}  $ {int(risk / (atrpercent / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent / 100))/cHigh[-1]))}    "
												f"{float('{:.5f}'.format(cHigh[-1] - atr))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent / 100) *  0.0008))}"
												
												f"\n2xATR |  {float('{:.2f}'.format(atrpercent*2))}%  | {cHigh[-1]}  $ {int(risk / (atrpercent*2 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent*2 / 100))/cHigh[-1]))}    "
												f"{float('{:.5f}'.format(cHigh[-1] - atr*2))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent*2 / 100) *  0.0008))}"
																								
												f"\n3xATR |  {float('{:.2f}'.format(atrpercent*3))}%  | {cHigh[-1]}  $ {int(risk / (atrpercent*3 / 100))}   "
												f"₿ {float('{:.2f}'.format((risk / (atrpercent*3 / 100))/cHigh[-1]))}    "
												f"{float('{:.5f}'.format(cHigh[-1] - atr*3))}    "
												f"fee {float('{:.2f}'.format(risk / (atrpercent*3 / 100) *  0.0008))}"
									
												f"\nhttps://www.binance.com/en/futures/{symbol}/",
									 disable_web_page_preview=True)
					sendScreen(timeinterval=timeinterval, symbol=symbol, cumDeltaValues=cumDeltaValues, dcoordinate=int(-i - 2), direction=" -> BUY")
					print(f"{datetime.now().strftime('%b %d, %H:%M')} Bullish {symbol}. CD fractal on {cVolume[-i - 2]} volume")
			break

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
				divergence(symbol=i, timeinterval=5, risk=rsk)
				print(".", end="")
			print(f"{datetime.now().strftime('%H:%M:%S')} M5 end")

			if minutesnow == '13' or minutesnow == '43':
				print(f"{datetime.now().strftime('%H:%M:%S')} M15 start")
				for i in instruments:
					divergence(symbol=i, timeinterval=15, risk=rsk)
					print(".", end="")
				print(f"{datetime.now().strftime('%H:%M:%S')} M15 end")

			elif minutesnow == '28' or minutesnow == '58':
				print(f"{datetime.now().strftime('%H:%M:%S')} M15 start")
				for i in instruments:
					divergence(symbol=i, timeinterval=15, risk=rsk)
					print(".", end="")
				print(f"{datetime.now().strftime('%H:%M:%S')} M15 end")


				print(f"{datetime.now().strftime('%H:%M:%S')} M30 start")
				for i in instruments:
					divergence(symbol=i, timeinterval=30, risk=rsk)
					print(".", end="")
				print(f"{datetime.now().strftime('%H:%M:%S')} M30 end")

	except:
		sleep(60)
		bot.send_message(662482931, "Bot-1 stopped due an error")

	sleep(10)

# divergence('AAVEUSDT', 5, 1)


