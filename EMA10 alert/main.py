import datetime
from multiprocessing import Process
import time
from ema_finder import pin_finder1
import instruments16

#
# instrument1 = 'ARBUSDT'
# instrument2 = 'LQTYUSDT'
# instrument3 = 'MAGICUSDT'
# instrument4 = 'RNDRUSDT'
#
# instrument5 = 'FOOTBALLUSDT'
# instrument6 = 'JASMYUSDT'
# instrument7 = 'PEOPLEUSDT'
# instrument8 = 'SXPUSDT'
# instrument9 = 'CHZUSDT'
# instrument10 = 'IOSTUSDT'
# instrument11 = 'SRMUSDT'
# instrument12 = 'OCEANUSDT'
# # instrument13 = 'RENUSDT'
# # instrument14 = 'MKRUSDT'


def main():

	time1 = time.perf_counter()
	print(f"Starting processes...at {datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}")

	p1 = Process(target=pin_finder1, args=(instruments16.section_1,))
	p2 = Process(target=pin_finder1, args=(instruments16.section_2,))
	p3 = Process(target=pin_finder1, args=(instruments16.section_3,))
	p4 = Process(target=pin_finder1, args=(instruments16.section_4,))
	p5 = Process(target=pin_finder1, args=(instruments16.section_5,))
	p6 = Process(target=pin_finder1, args=(instruments16.section_6,))
	p7 = Process(target=pin_finder1, args=(instruments16.section_7,))
	p8 = Process(target=pin_finder1, args=(instruments16.section_8,))
	p9 = Process(target=pin_finder1, args=(instruments16.section_9,))
	p10 = Process(target=pin_finder1, args=(instruments16.section_10,))
	p11 = Process(target=pin_finder1, args=(instruments16.section_11,))
	p12 = Process(target=pin_finder1, args=(instruments16.section_12,))
	p13 = Process(target=pin_finder1, args=(instruments16.section_13,))
	p14 = Process(target=pin_finder1, args=(instruments16.section_14,))
	p15 = Process(target=pin_finder1, args=(instruments16.section_15,))
	p16 = Process(target=pin_finder1, args=(instruments16.section_16,))

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
	p13.start()
	p14.start()
	p15.start()
	p16.start()

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
	p13.join()
	p14.join()
	p15.join()
	p16.join()

	time2 = time.perf_counter()
	time3 = time2-time1

	print(f"Finished processes in {int(time3)} secs, at {datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}")

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
	p13.close()
	p14.close()
	p15.close()
	p16.close()


def waiting():
	while True:
		now = datetime.datetime.now()
		if int(now.strftime('%S')) == 00:
			break
		time.sleep(0.1)


if __name__ == "__main__":
	while True:
		main()
		print("")
		time.sleep(40)
		waiting()
