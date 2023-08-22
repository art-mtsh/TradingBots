import pandas as pd
from requests import get
from multiprocessing import Process
import instruments8
import telebot
import time
import datetime
from module_information import information_func
from module_sonic import sonic_signal

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)


def calculation(instr, filter1, filter2, filter3, filter4):
	timeinterval = '5m'
	
	for symbol in instr:
		try:
			# --- DATA ---
			url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=95'
			data1 = get(url_klines).json()
			
			d1 = pd.DataFrame(data1)
			d1.columns = [
				'open_time',
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
				'is_best_match'
			]
			df1 = d1
			df1['cOpen'] = df1['cOpen'].astype(float)
			df1['cHigh'] = df1['cHigh'].astype(float)
			df1['cLow'] = df1['cLow'].astype(float)
			df1['cClose'] = df1['cClose'].astype(float)
			df1['cVolume'] = df1['cVolume'].astype(float)
			
			cOpen = df1['cOpen'].to_numpy()
			cHigh = df1['cHigh'].to_numpy()
			cLow = df1['cLow'].to_numpy()
			cClose = df1['cClose'].to_numpy()
			cVolume = df1['cVolume'].to_numpy()
			
			data = [timeinterval] + information_func(symbol=symbol, cHigh=cHigh, cLow=cLow, cClose=cClose, cVolume=cVolume) + sonic_signal(cOpen=cOpen, cHigh=cHigh, cLow=cLow, cClose=cClose)
			
			if data[2] <= filter1 and data[3] <= filter2 and data[4] >= filter3 and data[5] >= filter4:
				if data[-1] != "Sleep":
					print(
					f"{data[1]} {data[-1]}\n"
					f"Price: {data[2]} <= {filter1}\n"
					f"Tick: {data[3]} <= {filter2}\n"
					f"Vol: {data[4]} >= {filter3}\n"
					f"ATR: {data[5]} >= {filter4}\n"
					)
					
					bot3.send_message(
					662482931,
					f"{data[1]} {data[-1]}!\n"
					f"Price: ${data[2]} <= ${filter1}\n"
					f"Tick: {data[3]}% <= {filter2}%\n"
					f"Vol: ${data[4]}.000 >= ${filter3}.000\n"
					f"ATR: {data[5]}% >= {filter4}%"
					)
				
		except telebot.apihelper.ApiTelegramException as ex:
			print(f'Telegram error for {symbol}: {ex}')
			
		except Exception as exy:
			print(f'Error main module for {symbol}: {exy}')

def search_activale(filter1, filter2, filter3, filter4):
	time1 = time.perf_counter()
	print(f"Starting processes...at {datetime.datetime.now().strftime('%H:%M:%S')}")
	
	p1 = Process(target=calculation, args=(instruments8.section_1, filter1, filter2, filter3, filter4,))
	p2 = Process(target=calculation, args=(instruments8.section_2, filter1, filter2, filter3, filter4,))
	p3 = Process(target=calculation, args=(instruments8.section_3, filter1, filter2, filter3, filter4,))
	p4 = Process(target=calculation, args=(instruments8.section_4, filter1, filter2, filter3, filter4,))
	p5 = Process(target=calculation, args=(instruments8.section_5, filter1, filter2, filter3, filter4,))
	p6 = Process(target=calculation, args=(instruments8.section_6, filter1, filter2, filter3, filter4,))
	p7 = Process(target=calculation, args=(instruments8.section_7, filter1, filter2, filter3, filter4,))
	p8 = Process(target=calculation, args=(instruments8.section_8, filter1, filter2, filter3, filter4,))
	# p9 = Process(target=calculation, args=(instruments16.section_9, filter1, filter2, filter3, filter4,))
	# p10 = Process(target=calculation, args=(instruments16.section_10, filter1, filter2, filter3, filter4,))
	# p11 = Process(target=calculation, args=(instruments16.section_11, filter1, filter2, filter3, filter4,))
	# p12 = Process(target=calculation, args=(instruments16.section_12, filter1, filter2, filter3, filter4,))
	# p13 = Process(target=calculation, args=(instruments16.section_13, filter1, filter2, filter3, filter4,))
	# p14 = Process(target=calculation, args=(instruments16.section_14, filter1, filter2, filter3, filter4,))
	# p15 = Process(target=calculation, args=(instruments16.section_15, filter1, filter2, filter3, filter4,))
	# p16 = Process(target=calculation, args=(instruments16.section_16, filter1, filter2, filter3, filter4,))
	
	p1.start()
	p2.start()
	p3.start()
	p4.start()
	p5.start()
	p6.start()
	p7.start()
	p8.start()
	# p9.start()
	# p10.start()
	# p11.start()
	# p12.start()
	# p13.start()
	# p14.start()
	# p15.start()
	# p16.start()

	
	p1.join()
	p2.join()
	p3.join()
	p4.join()
	p5.join()
	p6.join()
	p7.join()
	p8.join()
	# p9.join()
	# p10.join()
	# p11.join()
	# p12.join()
	# p13.join()
	# p14.join()
	# p15.join()
	# p16.join()


	p1.close()
	p2.close()
	p3.close()
	p4.close()
	p5.close()
	p6.close()
	p7.close()
	p8.close()
	# p9.close()
	# p10.close()
	# p11.close()
	# p12.close()
	# p13.close()
	# p14.close()
	# p15.close()
	# p16.close()

	
	time2 = time.perf_counter()
	time3 = time2 - time1
	print(f"Finished processes in {int(time3)} secs, at {datetime.datetime.now().strftime('%H:%M:%S')}")


price_filter = 1000
tick_filter = 0.04
min_volume_filter = 5
atr_filter = 0.3

if __name__ == '__main__':

	while True:
		search_activale(filter1=price_filter, filter2=tick_filter, filter3=min_volume_filter, filter4=atr_filter)
		time.sleep(60*4)