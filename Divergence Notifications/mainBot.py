import pandas
import requests
from datetime import datetime
import calendar
import telebot
from screenshoter import sendScreen
from time import sleep

# --- TELEGRAM ---

TOKEN = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot = telebot.TeleBot(TOKEN)

# --- PENDING SEARCH ---

def divergence(cryptoPair: str, interval: int):
	symbol = cryptoPair
	timeinterval = interval

	# --- DATA ---

	now = datetime.utcnow()
	unixtime = calendar.timegm(now.utctimetuple())
	since = unixtime
	start = str(since - 60 * 60 * 10)

	url = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + str(
		timeinterval) + 'm' + '&limit=51'
	data = requests.get(url).json()

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

		if cClose[-i] >= cOpen[-i] and cClose[-i] - cOpen[-i] + 2 * (cHigh[-i] - cClose[-i]) + 2 * (
				cOpen[-i] - cLow[-i]) > 0:
			U1 = cVolume[-i] * (cHigh[-i] - cLow[-i]) / (
					cClose[-i] - cOpen[-i] + 2 * (cHigh[-i] - cClose[-i]) + 2 * (cOpen[-i] - cLow[-i]))
		else:
			U1 = 0.0

		if cClose[-i] < cOpen[-i] and cOpen[-i] - cClose[-i] + 2 * (cHigh[-i] - cOpen[-i]) + 2 * (
				cClose[-i] - cLow[-i]) > 0:
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

	for i in range(2, cumDeltaPeriod - 5):
		if cumDeltaValues[-i] < cumDeltaValues[-i - 1] < cumDeltaValues[-i - 2] > cumDeltaValues[-i - 3] > \
				cumDeltaValues[-i - 4]:
			if cumDeltaValues[-1] >= cumDeltaValues[-i - 2] and cHigh[-1] < cHigh[-i - 2]:
				clean = 0
				for b in range(2, i + 2):
					if cHigh[-b] >= cHigh[-i - 2] or cumDeltaValues[-b] >= cumDeltaValues[-i - 2]:
						clean += 1
				if clean == 0:
					bot.send_message(662482931, f"{datetime.now().strftime('%b %d, %H:%M')} ... {symbol}"
												f"\nBEARish pattern on {timeinterval}m timeframe"
												f"\nhttps://www.binance.com/en/futures/{symbol}/",
									 disable_web_page_preview=True)
					sendScreen(timeinterval=timeinterval, symbol=symbol, cumDeltaValues=cumDeltaValues, dcoordinate=int(-i - 2), direction=" is BEARish")
					print(f"{datetime.now().strftime('%b %d, %H:%M')} Bearish {symbol}. CD fractals on volumes: {cVolume[-1]} >= {cVolume[-i - 2]}")
			break

	for i in range(2, cumDeltaPeriod - 5):
		if cumDeltaValues[-i] > cumDeltaValues[-i - 1] > cumDeltaValues[-i - 2] < cumDeltaValues[-i - 3] < \
				cumDeltaValues[-i - 4]:
			if cumDeltaValues[-1] <= cumDeltaValues[-i - 2] and cLow[-1] > cLow[-i - 2]:
				clean = 0
				for b in range(2, i + 2):
					if cLow[-b] <= cLow[-i - 2] or cumDeltaValues[-b] <= cumDeltaValues[-i - 2]:
						clean += 1
				if clean == 0:
					bot.send_message(662482931, f"{datetime.now().strftime('%b %d, %H:%M')} ... {symbol}"
												f"\nBULLish pattern on {timeinterval}m timeframe"
												f"\nhttps://www.binance.com/en/futures/{symbol}/",
									 disable_web_page_preview=True)
					sendScreen(timeinterval=timeinterval, symbol=symbol, cumDeltaValues=cumDeltaValues, dcoordinate=int(-i - 2), direction=" is BULLish")
					print(f"{datetime.now().strftime('%b %d, %H:%M')} Bullish {symbol}. CD fractals on volumes: {cVolume[-1]} <= {cVolume[-i - 2]}")
			break

	# return sendScreen(timeinterval=timeinterval, symbol=symbol, cumDeltaValues=cumDeltaValues, dcoordinate=-10, direction=" is BULLish")

while True:
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
				   # "FOOTBALLUSDT",
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

	if datetime.now().strftime('%M')[-1] == "4" or datetime.now().strftime('%M')[-1] == "9":
		print(f"Starting new cycle at {datetime.now().strftime('%H:%M:%S')} ")
		for i in instruments:
			# print(f"running {i}...")
			divergence(i, 5)
		print(f"Finished current cycle at {datetime.now().strftime('%H:%M:%S')}")
		sleep(200)
	else:
		sleep(1)

# divergence('AAVEUSDT', 5)

