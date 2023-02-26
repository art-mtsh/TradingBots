import pandas as pd
from requests import get
import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer
from typing import List
import time
import datetime


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
	url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=1000'
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
	atr = (sum(sum([cHigh[950:] - cLow[950:]])) / len(cClose[950:]))
	atrper = atr / (cClose[-1] / 100)
	atrper = float('{:.2f}'.format(atrper))

	distancetores = 0
	respoint = 0

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

			if clean == 0 and doubletouchup > 0:
				distancetores += (cHigh[point] - cClose[-1]) / (cClose[-1] / 100)
				respoint += cHigh[point]
				break

	distancetosup = 0
	suppoint = 0

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

			if clean == 0 and doubletouchdn > 0:
				distancetosup += (cClose[-1] - cLow[point]) / (cClose[-1] / 100)
				suppoint += cLow[point]
				break

	distancetores = float('{:.2f}'.format(distancetores))
	distancetosup = float('{:.2f}'.format(distancetosup))

	# return a list of 6 elements
	return [timeinterval, symbol, atrper, distancetores, respoint, distancetosup, suppoint]

# --- GUI ---
app = QApplication(sys.argv)
table = QTableWidget()
table.setStyleSheet("QTableWidget { alignment: center; }")


# table_data = []
#
# def s_on_m1():
# 	for i in instruments:
# 		data1 = screensaver(i, '1m')
# 		table_data.append(data1)
#
# def s_on_m5():
# 	for i in instruments:
# 		data5 = screensaver(i, '5m')
# 		table_data.append(data5)
#
# def s_on_m15():
# 	for i in instruments:
# 		data15 = screensaver(i, '15m')
# 		table_data.append(data15)
#
# a = Process(target=s_on_m1)
# b = Process(target=s_on_m5)
# c = Process(target=s_on_m15)

# Define a function to refresh the table
def refresh_table():

	# Set the number of rows and columns of the table
	num_cols = 7
	table.setColumnCount(num_cols)

	# Set the headers of the table
	headers = ["Timeframe", "Symbol", "ATR %", "To RES %", "RES", "To SUP %", "SUP"]
	table.setHorizontalHeaderLabels(headers)

	time1 = time.perf_counter()
	print(f"Starting processes...at {datetime.datetime.now().strftime('%M:%S')}")

	table_data = []

	for i in instruments:
		data1 = screensaver(i, '1m')
		if 0 < data1[-2] < 1 or 0 < data1[-4] < 1:
			table_data.append(data1)

	for i in instruments:
		data5 = screensaver(i, '5m')
		if 0 < data5[-2] < 1 or 0 < data5[-4] < 1:
			table_data.append(data5)

	time2 = time.perf_counter()
	time3 = time2-time1

	print(f"Finished processes in {int(time3)} secs, at {datetime.datetime.now().strftime('%M:%S')}")

	# Set the number of rows of the table
	num_rows = len(table_data)
	table.setRowCount(num_rows)

	# Fill the table with filtered data
	for i, row in enumerate(table_data):
		for j in range(num_cols):
			table.setItem(i, j, QTableWidgetItem(str(row[j])))

	table.sortByColumn(2, Qt.DescendingOrder)

	table.setColumnWidth(0, 200)
	table.setColumnWidth(1, 200)
	table.setColumnWidth(2, 200)
	table.setColumnWidth(3, 200)
	table.setColumnWidth(4, 200)
	table.setColumnWidth(5, 200)
	table.setColumnWidth(6, 200)

	table.setFixedWidth(1460)
	# table.setFixedHeight(window_height)

	table.setStyleSheet("QTableWidget { alignment: center; }")

	# Show the table
	table.show()


	table_data.clear()

if __name__ == '__main__':

	# Call the refresh_table function to populate the table for the first time
	refresh_table()

	# Set up a QTimer to refresh the table every 5 minutes
	timer = QTimer()
	timer.timeout.connect(refresh_table)
	timer.start(2 * 60 * 1000)  # 1 minutes in milliseconds

	# Run the event loop
	sys.exit(app.exec_())

