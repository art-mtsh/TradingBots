import datetime
import sys
import time
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QVariant
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from Interface3_mp import get_data_table
from PyQt5.QtGui import QColor

# --- GUI ---

def sortTable(table, logicalIndex):
	table.sortItems(logicalIndex, Qt.DescendingOrder)

def refresh_table():
	time1 = time.perf_counter()
	print(f"Starting processes...at {datetime.datetime.now().strftime('%H:%M:%S')}")

	price_filter = 1000
	tick_filter = 0.01
	min_volume = 10
	table_data = get_data_table(filter1 = price_filter, filter2 = tick_filter, filter3 = min_volume)
	num_rows = len(table_data)
	table.setRowCount(num_rows)

	num_cols = 17
	table.setColumnCount(num_cols)
	table.setWindowTitle(f'Last price < {price_filter}, Tick size < {tick_filter}, 1 minute volume/1000 > {min_volume}')
	headers = ["TF",
			   "Symbol",
			   "Last price",
			   "Tick, %",
			   "1000, $",
			   "ATR-60, %",
			   "R10, %",
			   "R9, %",
			   "R8, %",
			   "R7, %",
			   "R6, %",
			   "R5, %",
			   "R4, %",
			   "R3, %",
			   "R2, %",
			   "R1, %",
			   "Swing"]
	table.setHorizontalHeaderLabels(headers)
	header_font = QFont("Calibri Light", 12, QFont.Bold)
	table.horizontalHeader().setFont(header_font)
	bg_color_g = QColor(230, 230, 230)
	bg_color_gr = QColor(240, 255, 222)
	bg_color_y = QColor(255, 255, 81)

	for i, row in enumerate(table_data):
		for j in range(num_cols):

			if isinstance(row[j], str):
				item = QTableWidgetItem()
				item.setData(Qt.DisplayRole, QVariant(row[j]))
			elif isinstance(row[j], int):
				item = QTableWidgetItem()
				item.setData(Qt.DisplayRole, QVariant(row[j]))
			elif isinstance(row[j], float):
				item = QTableWidgetItem()
				item.setData(Qt.DisplayRole, QVariant(row[j]))

			item.setTextAlignment(Qt.AlignCenter)
			item.setFont(QFont("Calibri Light", 12))
			table.setItem(i, j, item)
			table.setColumnWidth(j, 65)

			if j in range(6, 16):
				item.setBackground(bg_color_g)
				if row[j] > 3:
					item.setBackground(bg_color_y)
			if j == 16:
				item.setBackground(bg_color_gr)
				if row[j] > 2:
					item.setBackground(bg_color_y)

	table.sortByColumn(16, Qt.DescendingOrder)

	table.setColumnWidth(0, 50)
	table.setColumnWidth(1, 120)
	table.setColumnWidth(2, 90)
	table.setColumnWidth(3, 80)
	table.setColumnWidth(5, 100)

	table.setFixedWidth(1300)
	table.show()

	time2 = time.perf_counter()
	time3 = time2-time1
	print(f"Finished processes in {int(time3)} secs, at {datetime.datetime.now().strftime('%H:%M:%S')}")

def run():
	app = QApplication (sys.argv)
	global table
	table = QTableWidget()
	table.horizontalHeader().sectionClicked.connect(lambda index: sortTable(table, index))
	refresh_table()
	timer = QTimer()
	timer.timeout.connect(refresh_table)
	timer.start(1 * 60 * 1000)  # 5 minutes in milliseconds
	sys.exit(app.exec_())

if __name__ == '__main__':
	run()
