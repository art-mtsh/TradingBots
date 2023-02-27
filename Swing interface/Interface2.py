import datetime
import sys
import time
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from Interface2_mp import get_data_table

# --- GUI ---
app = QApplication(sys.argv)
table = QTableWidget()


def refresh_table():

	time1 = time.perf_counter()
	print(f"Starting processes...at {datetime.datetime.now().strftime('%H:%M:%S')}")

	table_data = get_data_table(searchfilter=0.1)
	num_rows = len(table_data)
	table.setRowCount(num_rows)

	num_cols = 3
	table.setColumnCount(num_cols)
	headers = ["Timeframe", "Symbol", "Swing"]
	table.setHorizontalHeaderLabels(headers)
	header_font = QFont("Calibri Light", 12, QFont.Bold)
	table.horizontalHeader().setFont(header_font)

	# Fill the table with filtered data
	for i, row in enumerate(table_data):
		for j in range(num_cols):
			item = QTableWidgetItem(str(row[j]))
			item.setTextAlignment(Qt.AlignCenter)
			item.setFont(QFont("Calibri Light", 12))
			table.setItem(i, j, item)
			table.setColumnWidth(j, 200)

	table.sortByColumn(2, Qt.DescendingOrder)
	table.setFixedWidth(640)
	table.show()

	time2 = time.perf_counter()
	time3 = time2-time1
	print(f"Finished processes in {int(time3)} secs, at {datetime.datetime.now().strftime('%H:%M:%S')}")


if __name__ == '__main__':

	# Call the refresh_table function to populate the table for the first time
	refresh_table()

	# Set up a QTimer to refresh the table every 5 minutes
	timer = QTimer()
	timer.timeout.connect(refresh_table)
	timer.start(1 * 60 * 1000)  # 1 minutes in milliseconds

	# Run the event loop
	sys.exit(app.exec_())
