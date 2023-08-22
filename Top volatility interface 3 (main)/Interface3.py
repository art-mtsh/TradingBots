import datetime
import sys
import time
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QVariant
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from Interface3_module_calc import get_data_table
from PyQt5.QtGui import QColor

# --- GUI ---

def sortTable(table, logicalIndex):
	table.sortItems(logicalIndex, Qt.DescendingOrder)

def refresh_table():
	time1 = time.perf_counter()
	print(f"Starting processes...at {datetime.datetime.now().strftime('%H:%M:%S')}")

	price_filter = 2000
	tick_filter = 0.03
	min_volume_filter = 50
	
	atr_filter = 0.3
	table_data = get_data_table(filter1 = price_filter, filter2 = tick_filter, filter3 = min_volume_filter, filter4 = atr_filter)
	num_rows = len(table_data)
	table.setRowCount(num_rows)

	num_cols = 7
	table.setColumnCount(num_cols)
	table.setWindowTitle(f'PRICE < {price_filter}                TICKSIZE < {tick_filter}                VOLUME > {min_volume_filter}*100 USD/minute                ATR > {atr_filter}%')
	headers = ["TF",
			   "Symbol",
			   f"<{price_filter}$",
			   f"<{tick_filter}%",
			   f">{min_volume_filter}k/m",
			   f"ATR%",
	           f"Sonic"
			   # "R10,%",
			   # "R9,%",
			   # "R8,%",
			   # "R7,%",
			   # "R6,%",
			   # "R5,%",
			   # "R4,%",
			   # "R3,%",
			   # "R2,%",
			   # "R1,%",
			   # "10EMA",
			   # "Room",
			   # "2H",
			   # "4H",
			   # "8H",
			   # "12",
			   # "Level",
			   # "Dist, %"
	           ]

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

			# if j == 6:
			# 	item.setBackground(QColor(249, 251, 231))
			# 	if row[j] == "Up":
			# 		item.setBackground(QColor(220, 237, 200))
			# 	elif row[j] == "Down":
			# 		item.setBackground(QColor(255, 204, 188))
			#
			# if j == 7:
			# 	item.setBackground(QColor(255, 243, 224))
			# 	if row[j] > 60:
			# 		item.setBackground(QColor(255, 204, 128))
			#
			# if j == 8:
			# 	item.setBackground(QColor(255, 243, 224))
			# 	if row[j] < 0.5:
			# 		item.setBackground(QColor(255, 204, 128))
			#
			# if j == 9:
			# 	item.setBackground(QColor(255, 243, 224))
			# 	if row[j] < 0.5:
			# 		item.setBackground(QColor(255, 204, 128))
			#
			# if j == 10:
			# 	item.setBackground(QColor(255, 243, 224))
			# 	if row[j] < 0.5:
			# 		item.setBackground(QColor(255, 204, 128))
			#
			# if j == 11:
			# 	item.setBackground(QColor(255, 243, 224))
			# 	if row[j] < 0.5:
			# 		item.setBackground(QColor(255, 204, 128))
			#
			# if j == 12:
			# 	item.setBackground(QColor(255, 253, 231))
			#
			# if j == 13:
			# 	item.setBackground(QColor(255, 253, 231))
			# 	if 0 < row[j] <= 0.5:
			# 		item.setBackground(QColor(255, 245, 157))



	# table.sortByColumn(8, Qt.AscendingOrder)

	table.setColumnWidth(0, 45)
	table.setColumnWidth(1, 110)
	table.setColumnWidth(2, 100)
	table.setColumnWidth(3, 100)
	table.setColumnWidth(4, 100)
	table.setColumnWidth(5, 65)
	table.setColumnWidth(6, 65)
	# table.setColumnWidth(7, 65)
	# table.setColumnWidth(8, 65)
	# table.setColumnWidth(9, 65)
	# table.setColumnWidth(10, 65)
	# table.setColumnWidth(11, 65)
	# table.setColumnWidth(12, 65)
	# table.setColumnWidth(13, 65)

	table.setFixedWidth(900)
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
	timer.start(5 * 60 * 1000)  # 2 minutes in milliseconds
	sys.exit(app.exec_())

if __name__ == '__main__':
	run()
