import datetime
from multiprocessing import Process
import time
from pin_finder import pin_finder1


instrument1 = 'ARBUSDT'
instrument2 = 'LQTYUSDT'
instrument3 = 'MAGICUSDT'
instrument4 = 'RNDRUSDT'

instrument5 = 'ACHUSDT'
instrument6 = 'AUDIOUSDT'
instrument7 = 'ENJUSDT'
instrument8 = 'INJUSDT'
instrument9 = 'ICXUSDT'
instrument10 = 'JASMYUSDT'
instrument11 = 'TOMOUSDT'
instrument12 = 'UNFIUSDT'
# instrument13 = 'RENUSDT'
# instrument14 = 'MKRUSDT'


def main():

	# time1 = time.perf_counter()

	# print(f"Starting processes...at {datetime.datetime.now().strftime('%M:%S.%f')[:-3]}")

	p1 = Process(target=pin_finder1, args=(instrument1,))
	p2 = Process(target=pin_finder1, args=(instrument2,))
	p3 = Process(target=pin_finder1, args=(instrument3,))
	p4 = Process(target=pin_finder1, args=(instrument4,))
	p5 = Process(target=pin_finder1, args=(instrument5,))
	p6 = Process(target=pin_finder1, args=(instrument6,))
	p7 = Process(target=pin_finder1, args=(instrument7,))
	p8 = Process(target=pin_finder1, args=(instrument8,))
	p9 = Process(target=pin_finder1, args=(instrument9,))
	p10 = Process(target=pin_finder1, args=(instrument10,))
	p11 = Process(target=pin_finder1, args=(instrument11,))
	p12 = Process(target=pin_finder1, args=(instrument12,))
	# p13 = Process(target=pin_finder1, args=(instrument13,))
	# p14 = Process(target=pin_finder1, args=(instrument14,))

	p1.start()
	p2.start()
	p3.start()
	p4.start()
	p5.start()
	p6.start()
	p7.start()
	p8.start()
	p9.start()
	p10.start()
	p11.start()
	p12.start()
	# p13.start()
	# p14.start()

	p1.join()
	p2.join()
	p3.join()
	p4.join()
	p5.join()
	p6.join()
	p7.join()
	p8.join()
	p9.join()
	p10.join()
	p11.join()
	p12.join()
	# p13.join()
	# p14.join()

	# time2 = time.perf_counter()
	# time3 = time2-time1

	# print(f"Finished processes in {int(time3)} secs, at {datetime.datetime.now().strftime('%M:%S.%f')[:-3]}")

	p1.close()
	p2.close()
	p3.close()
	p4.close()
	p5.close()
	p6.close()
	p7.close()
	p8.close()
	p9.close()
	p10.close()
	p11.close()
	p12.close()
	# p13.close()
	# p14.close()

def waiting():
	while True:
		now = datetime.datetime.now()
		if int(now.strftime('%M')) % 15 == 0:
			print(f"full timestamp: {now.strftime('%H:%M:%S.%f')[:-3]}")
			print(f"minutes timestamp: {now.strftime('%M')}")
			print(f"waiting stop on: {now.strftime('%M')} % 15 == 0")
			break
		time.sleep(60)

if __name__ == "__main__":
	while True:
		print(datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3])
		main()
		print("")
		time.sleep(60)
		waiting()
