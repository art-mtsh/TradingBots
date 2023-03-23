import datetime
import sys
import time
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QVariant
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from Interface3_mp import get_data_table

# --- GUI ---

def sortTable(table, logicalIndex):
	table.sortItems(logicalIndex, Qt.DescendingOrder)

def refresh_table():
	time1 = time.perf_counter()
	print(f"Starting processes...at {datetime.datetime.now().strftime('%H:%M:%S')}")

	table_data = get_data_table(searchfilter=0.2)
	num_rows = len(table_data)
	table.setRowCount(num_rows)

	num_cols = 9
	table.setColumnCount(num_cols)
	headers = ["TF", "Symbol", "Tick size, %", "Range-60, %", "ATR-60, %", "B/R-60, %", "B/R-10, %", "Avg.vol./1000, $", "Last price"]
	table.setHorizontalHeaderLabels(headers)
	header_font = QFont("Calibri Light", 12, QFont.Bold)
	table.horizontalHeader().setFont(header_font)

	# Fill the table with filtered data
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
			table.setColumnWidth(j, 150)

	table.sortByColumn(4, Qt.DescendingOrder)

	table.setColumnWidth(0, 50)
	table.setColumnWidth(1, 120)
	table.setColumnWidth(2, 120)
	table.setColumnWidth(3, 120)
	table.setColumnWidth(4, 120)
	table.setColumnWidth(5, 120)
	table.setColumnWidth(6, 120)
	table.setColumnWidth(7, 150)
	table.setColumnWidth(8, 150)
	# table.setColumnWidth(9, 70)
	# table.setColumnWidth(10, 70)
	# table.setColumnWidth(11, 70)

	table.setFixedWidth(1130)
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
	timer.start(5 * 60 * 1000)  # 5 minutes in milliseconds
	sys.exit(app.exec_())

if __name__ == '__main__':
	run()
