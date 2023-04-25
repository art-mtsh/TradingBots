import pandas as pd
from requests import get
import telebot
from talib import EMA

# import datetime
#
# TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
# bot3 = telebot.TeleBot(TOKEN3)
#
# bot3.send_message(662482931, "Cross UNDER")

url_tick = f"https://fapi.binance.com/fapi/v1/exchangeInfo"
response = get(url_tick)
data_tick = response.json()

symbol_info = next(filter(lambda s: s['symbol'] == "INJUSDT", data_tick['symbols']), None)
print(symbol_info)
tick_size_filter = next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']), None)
print(tick_size_filter)
cTick = float(tick_size_filter['tickSize'])
print(cTick)