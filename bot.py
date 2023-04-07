import datetime
import pandas as pd
import numpy as np
import telebot
from requests import get
import os
import requests
import math
import time

# --- TELEGRAM ---

# TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
# bot3 = telebot.TeleBot(TOKEN3)
#
# bot3.send_message(662482931, "1234124123")

# def main():
# 	print("Processing...")
# 	print("")
#
# def waiting():
# 	while True:
# 		now = datetime.datetime.now()
# 		if int(now.strftime('%M')[-1]) % 2 == 0:
# 			print(f"full timestamp: {now.strftime('%H:%M:%S.%f')[:-3]}")
# 			print(f"minutes timestamp: {now.strftime('%M')}")
# 			print(f"waiting stop on: {now.strftime('%M')[-1]}")
# 			break
# 		time.sleep(60)
#
# if __name__ == "__main__":
# 	while True:
# 		print(datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3])
# 		main()
# 		time.sleep(60)
# 		waiting()


print(0 % 15)