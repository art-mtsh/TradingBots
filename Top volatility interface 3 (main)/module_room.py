import pandas as pd
from requests import get
from typing import List
from multiprocessing import Process, Manager
import instruments16
import telebot
import talib

def room_function(symbol: str, cOpen, cHigh, cLow, cClose, cVolume):

	high_room_counter = 0
	low_room_counter = 0

	for i in range(2, 241):
		if cHigh[-1] >= cHigh[-i]:
			high_room_counter += 1
		else:
			break

	for i in range(2, 241):
		if cLow[-1] <= cLow[-i]:
			low_room_counter += 1
		else:
			break

	return max(high_room_counter, low_room_counter)
