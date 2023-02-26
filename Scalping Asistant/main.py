import datetime
from multiprocessing import Process, cpu_count
import time
from Search_SR import search_SR

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
				   "DEFIUSDT",
				   "DENTUSDT",
				   "DGBUSDT",
				   "DOGEUSDT",
				   "DOTUSDT",
				   "DUSKUSDT",
				   "DYDXUSDT",
				   "EGLDUSDT",
				   "ENJUSDT",
				   "ENSUSDT",
				   "EOSUSDT",
				   "ETCUSDT",
				   "ETHUSDT",
				   "ETHUSDT",
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
				   "SPELLUSDT",
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
				   "YFIUSDT",
				   "ZECUSDT",
				   "ZENUSDT",
				   "ZILUSDT",
				   "ZRXUSDT"]
risk = 10

def SRSearch_on_m1():

	# if datetime.datetime.now().strftime('%M')[-1] == '3' or \
	# 		datetime.datetime.now().strftime('%M')[-1] == '8':

	print(f"{datetime.datetime.now().strftime('%H:%M:%S')} Search for M1: start")
	for i in instruments:
		search_SR(symbol=i, timeinterval='1m', risk=risk, searchdistance=1, atrfilter=0.1)
		print(".", end="")
	print(f"\n{datetime.datetime.now().strftime('%H:%M:%S')} Search for M1: stop")

def SRSearch_on_m5():

	# if datetime.datetime.now().strftime('%M')[-1] == '0' or \
	# 		datetime.datetime.now().strftime('%M')[-1] == '5':

	print(f"{datetime.datetime.now().strftime('%H:%M:%S')} Search for M5: start")
	for i in instruments:
		search_SR(symbol=i, timeinterval='5m', risk=risk, searchdistance=1, atrfilter=0.1)
		print(".", end="")
	print(f"\n{datetime.datetime.now().strftime('%H:%M:%S')} Search for M5: stop")

def SRSearch_on_m15():

	# if datetime.datetime.now().strftime('%M') == '30' or \
	# 	datetime.datetime.now().strftime('%M') == '00' or \
	# 	datetime.datetime.now().strftime('%M') == '15' or \
	# 	datetime.datetime.now().strftime('%M') == '45':

	print(f"{datetime.datetime.now().strftime('%H:%M:%S')} Search for M15: start")
	for i in instruments:
		search_SR(symbol=i, timeinterval='15m', risk=risk, searchdistance=1, atrfilter=0.1)
		print(".", end="")
	print(f"\n{datetime.datetime.now().strftime('%H:%M:%S')} Search for M15: stop")


def main():

	time1 = time.perf_counter()

	print(f"Starting processes...at {datetime.datetime.now().strftime('%M:%S')}")

	# a = Process(target=divergenceSearch_on_m5)
	# b = Process(target=divergenceSearch_on_m15)
	# c = Process(target=divergenceSearch_on_m30)
	# d = Process(target=divergenceSearch_on_h1)

	# e = Process(target=highRangeSearch_on_m5)
	# f = Process(target=highRangeSearch_on_m15)
	# g = Process(target=highRangeSearch_on_m30)
	# h = Process(target=highRangeSearch_on_1H)

	j = Process(target=SRSearch_on_m1)
	k = Process(target=SRSearch_on_m5)
	l = Process(target=SRSearch_on_m15)

	# a.start()
	# b.start()
	# c.start()
	# d.start()
	# e.start()
	# f.start()
	# g.start()
	# h.start()
	j.start()
	k.start()
	l.start()

	# a.join()
	# b.join()
	# c.join()
	# d.join()
	# e.join()
	# f.join()
	# g.join()
	# h.join()
	j.join()
	k.join()
	l.join()

	time2 = time.perf_counter()
	time3 = time2-time1

	print(f"Finished processes in {int(time3)} secs, at {datetime.datetime.now().strftime('%M:%S')}")

	#closing
	# a.close()
	# b.close()
	# c.close()
	# d.close()
	# e.close()
	# f.close()
	# g.close()
	# h.close()
	j.close()
	k.close()
	l.close()

if __name__ == "__main__":
	while True:
		main()
		time.sleep(60)

# divergence("AAVEUSDT", 5, 10)