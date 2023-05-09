import pandas as pd
from requests import get
from typing import List
from multiprocessing import Process, Manager
import instruments16
import telebot
import talib

def information_func(symbol: str, cOpen, cHigh, cLow, cClose, cVolume):

	# --- TICK SIZE ---
	url_tick = f"https://fapi.binance.com/fapi/v1/exchangeInfo"
	response = get(url_tick)
	data_tick = response.json()

	symbol_info = next(filter(lambda s: s['symbol'] == symbol, data_tick['symbols']), None)
	tick_size_filter = next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']), None)
	cTick1 = float(tick_size_filter['tickSize'])
	cTick = float(f"{cTick1:.8f}")

	ticksizeper = (cTick / (cClose[-1] / 100))
	avgvolume_60 = int(((sum(cVolume[-1:-61:-1]) / len(cVolume[-1:-61:-1])) * cClose[-1]) / 1000)
	atr_60m = (sum(sum([cHigh[-1:-61:-1] - cLow[-1:-61:-1]])) / len(cClose[-1:-61:-1]))
	atr_60per = atr_60m / (cClose[-1] / 100)


	lastprice = float(cClose[-1])
	ticksizeper = float('{:.4f}'.format(ticksizeper))
	atr_60per = float('{:.2f}'.format(atr_60per))

	return symbol, lastprice, ticksizeper, avgvolume_60, atr_60per