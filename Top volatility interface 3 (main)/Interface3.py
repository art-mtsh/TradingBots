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
	tick_filter = 0.02
	min_volume_filter = 100
	atr_filter = 0.2
	table_data = get_data_table(filter1 = price_filter, filter2 = tick_filter, filter3 = min_volume_filter, filter4 = atr_filter)
	num_rows = len(table_data)
	table.setRowCount(num_rows)

	num_cols = 19
	table.setColumnCount(num_cols)
	table.setWindowTitle("MILLION DOLLARS")
	headers = ["TF",
			   "Symbol",
			   f"Price<{price_filter}",
			   f"Tick<{tick_filter}",
			   f"Vol>{min_volume_filter}k/m",
			   f"ATR>{atr_filter}",
			   "R10,%",
			   "R9,%",
			   "R8,%",
			   "R7,%",
			   "R6,%",
			   "R5,%",
			   "R4,%",
			   "R3,%",
			   "R2,%",
			   "R1,%",
			   "Ang.10m",
			   "10EMA",
			   "Room"]
	table.setHorizontalHeaderLabels(headers)
	header_font = QFont("Calibri Light", 12, QFont.Bold)
	table.horizontalHeader().setFont(header_font)

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
			table.setColumnWidth(j, 55)

			if j in range(6, 16):
				item.setBackground(QColor(227, 242, 253))
				if row[j] > 3:
					item.setBackground(QColor(187, 222, 251))

			if j == 16:
				item.setBackground(QColor(232, 245, 233))
				if row[j] > 100:
					item.setBackground(QColor(200, 230, 201))

			if j == 17:
				item.setBackground(QColor(232, 245, 233))
				if row[j] != 0:
					item.setBackground(QColor(200, 230, 201))

			if j == 18:
				item.setBackground(QColor(252, 249, 249))
				if row[j] > 120:
					item.setBackground(QColor(255, 204, 188))


	table.sortByColumn(5, Qt.DescendingOrder)

	table.setColumnWidth(0, 50)
	table.setColumnWidth(1, 110)
	table.setColumnWidth(2, 110)
	table.setColumnWidth(3, 110)
	table.setColumnWidth(4, 110)
	table.setColumnWidth(5, 80)
	table.setColumnWidth(16, 80)
	table.setColumnWidth(17, 80)
	table.setColumnWidth(18, 80)

	table.setFixedWidth(1400)
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
	timer.start(2 * 60 * 1000)  # 2 minutes in milliseconds
	sys.exit(app.exec_())

if __name__ == '__main__':
	run()
