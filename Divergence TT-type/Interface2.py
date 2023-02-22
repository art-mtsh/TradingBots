import pandas as pd
from requests import get
import sys
from typing import List
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QVBoxLayout, QWidget
import os

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

def screensaver(symbol: str, timeinterval: str) -> List:
    # --- DATA ---
    url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=300'
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

    # return a list of 6 elements
    return [symbol, cOpen[-1], cHigh[-1], cLow[-1], cClose[-1], cVolume[-1], atrper]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create table widget
        self.table = QTableWidget()
        self.num_cols = 7
        self.headers = ["Symbol", "Open", "High", "Low", "Close", "Volume", "ATR"]
        self.table.setColumnCount(self.num_cols)
        self.table.setHorizontalHeaderLabels(self.headers)

        # Create button to restart the script
        self.restart_button = QPushButton("Restart")
        self.restart_button.clicked.connect(self.restart)

        # Create input field for filter
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Enter filter")

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.restart_button)
        layout.addWidget(self.filter_edit)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Set the crypto pairs
        self.crypto_pairs = instruments

        # Fill the table
        self.fill_table()

    def fill_table(self):
        # Clear existing data in table
        self.table.setRowCount(0)

        # Get filter text
        filter_text = self.filter_edit.text()

        # Populate table with data that matches the filter
        table_data = []
        for i, row in enumerate(self.crypto_pairs):
            data = screensaver(row, '1m')
            if str(data[-1]) > filter_text:  # check the value of the atrper column
                table_data.append(data)

        num_rows = len(table_data)
        self.table.setRowCount(num_rows)

        for i, row in enumerate(table_data):
            for j in range(self.num_cols):
                self.table.setItem(i, j, QTableWidgetItem(str(row[j])))

        window_width = self.table.horizontalHeader().length() + 60  # Add 30 pixels for the window border
        self.table.setFixedWidth(window_width)

    def restart(self):
        # Restart the script
        python = sys.executable
        os.execl(python, python, *sys.argv)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
