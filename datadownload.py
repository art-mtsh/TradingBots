import pandas
import requests
from datetime import datetime
import calendar


def dataget(symbol: str, timeinterval: int):

	now = datetime.utcnow()
	unixtime = calendar.timegm(now.utctimetuple())
	since = unixtime

	url = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + str(timeinterval) + 'm' + '&limit=51'
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

	return cOpen, cHigh, cLow, cClose, cVolume, df

print(dataget("AAVEUSDT", 5)[0])