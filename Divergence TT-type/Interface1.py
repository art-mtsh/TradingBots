import pandas as pd
from requests import get
import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from typing import List


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
				   # "BNXUSDT",
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

# --- FUNCTION ---
def screensaver(symbol: str, timeinterval: str) -> List:
	# --- DATA ---
	url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=800'
	data1 = get(url_klines).json()

	# --- K-LINE ---
	D1 = pd.DataFrame(data1)
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
	atrper = (sum(sum([cHigh - cLow])) / len(cClose)) / (cClose[-1] / 100)
	atrper = float('{:.2f}'.format(atrper))

	distancetores = 0
	distancetosup = 0

	for i in range(2, 550):
		point = -i-120
		if max(cHigh[-i:-i-360:-1]) == cHigh[point]:
			clean = 0
			for b in range(2, -point):
				if cHigh[-b] <= cHigh[point]:
					clean += 1
			if clean == 0:
				distancetores += (cHigh[point] - cClose[-1]) / (cClose[-1] / 100)
				break

	for i in range(2, 400):
		point = -i-120
		if min(cLow[-i:-i-360:-1]) == cLow[point]:
			clean = 0
			for b in range(2, -point):
				if cLow[-b] <= cLow[point]:
					clean += 1
			if clean == 0:
				distancetosup += (cClose[-1] - cLow[point]) / (cClose[-1] / 100)
				break

	distancetores = float('{:.2f}'.format(distancetores))
	distancetosup = float('{:.2f}'.format(distancetosup))

	# return a list of 6 elements
	return [symbol, cOpen[-1], cHigh[-1], cLow[-1], cClose[-1], cVolume[-1], atrper, distancetores, distancetosup]

# --- GUI ---
app = QApplication(sys.argv)
table = QTableWidget()

# Set the number of rows and columns of the table
num_cols = 9
table.setColumnCount(num_cols)

# Set the headers of the table
headers = ["Symbol", "Open", "High", "Low", "Close", "Volume", "ATR %", "To RES %", "To SUP %"]
table.setHorizontalHeaderLabels(headers)

# Set the crypto pairs
crypto_pairs = instruments

# filter of volatility in %
table_data = []
for i, row in enumerate(crypto_pairs):
	data = screensaver(row, '1m')
	if 1 >= data[-1] > 0 or 1 >= data[-2] > 0:  # check the value of the atrper column
		table_data.append(data)

# Set the number of rows of the table
num_rows = len(table_data)
table.setRowCount(num_rows)

# Fill the table with filtered data
for i, row in enumerate(table_data):
	for j in range(num_cols):
		table.setItem(i, j, QTableWidgetItem(str(row[j])))

# Set the width of the window based on the table's width
window_width = table.horizontalHeader().length() + 60  # Add 30 pixels for the window border
window_height = table.verticalHeader().length() + 60

table.setFixedWidth(window_width)
table.setFixedHeight(window_height)

table.sortByColumn(7, Qt.DescendingOrder)

# Show the table
table.show()

# Run the event loop
sys.exit(app.exec_())