import pandas as pd
from requests import get
import telebot
# import talib

# import datetime

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

# 10EMA basis
# emabasis = 10

# 10EMA delta
# emadelta = 1.2

# price <= filter
price_filter = 100000

# volume >= filter
volume_filter = 100

# atr10 >= filter
atr10_perc_filter = 0.2

# pin range >= filter
pin_range_filter = 0.1

# body/range ratio <= filter
br_ratio_filter = 10

# close inside bar range / filter
bar_part_filter = 3

# tick size <= filter
# tick_size_fil = 0.02

# room filter
# room_filter = 1

def pin_finder1(sym: list):
    for symbol in sym:
        try:
            # --- DATA ---
            url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + '1m' + '&limit=1010'
            data1 = get(url_klines).json()

            D1 = pd.DataFrame(data1)
            D1.columns = ['open_time',
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
                          'is_best_match']
            df1 = D1
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

            # ma1 = talib.EMA(cClose, emabasis)[-1]
            # ma2 = talib.EMA(cClose, int(emabasis * emadelta))[-1]
            # ma3 = talib.EMA(cClose, int(emabasis * emadelta * emadelta))[-1]
            # ma4 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta))[-1]
            # ma5 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta))[-1]
            # ma6 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
            # ma7 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
            # ma8 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
            # ma9 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
            # ma10 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]

            if cHigh[-1] != cLow[-1]:
                atr = (sum(sum([cHigh[-1:-11:-1] - cLow[-1:-11:-1]])) / len(cClose[-1:-11:-1]))
                atr_per = atr / (cClose[-1] / 100)
                atr_per = float('{:.2f}'.format(atr_per))

                candle_range = cHigh[-1] - cLow[-1]
                candle_spread = abs(cOpen[-1] - cClose[-1])
                br_ratio = candle_spread / (candle_range / 100)
                range_part = candle_range / bar_part_filter
                candle_range_perc = (candle_range / cHigh[-1]) * 100
                candle_range_perc = float('{:.2f}'.format(candle_range_perc))

                # if ma1 >= ma2 >= ma3 >= ma4 >= ma5 >= ma6 >= ma7 >= ma8 >= ma9 >= ma10 or\
                #     ma1 <= ma2 <= ma3 <= ma4 <= ma5 <= ma6 <= ma7 <= ma8 <= ma9 <= ma10:
                if cClose[-1] <= price_filter:
                    if ((sum(cVolume[-1:-11:-1]) / len(cVolume[-1:-11:-1])) * cClose[-1]) / 1000 >= volume_filter:
                        if cVolume[-1] >= cVolume[-2]:
                            if atr_per >= atr10_perc_filter:
                                if candle_range_perc >= pin_range_filter:
                                    if br_ratio <= br_ratio_filter:
                                        if (cHigh[-1] >= cClose[-1] >= (cHigh[-1] - range_part)) or (cLow[-1] <= cClose[-1] <= (cLow[-1] + range_part)):

                                            # --- TICK SIZE ---
                                            url_tick = f"https://fapi.binance.com/fapi/v1/exchangeInfo"
                                            response = get(url_tick)
                                            data_tick = response.json()

                                            symbol_info = next(filter(lambda s: s['symbol'] == symbol, data_tick['symbols']), None)
                                            tick_size_filter = next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']), None)
                                            cTick = float(tick_size_filter['tickSize'])
                                            tick_size = cTick / (cClose[-1] / 100)
                                            tick_size = float('{:.4f}'.format(tick_size))

                                            if tick_size <= 0.01:
                                                bot3.send_message(662482931, f"{symbol}[-1]. Price: {cClose[-1]}. Vol 10MA: {int(((sum(cVolume[-1:-11:-1]) / len(cVolume[-1:-11:-1])) * cClose[-1]) / 1000)}.\n"
                                                                             f"ATR% 10MA: {atr_per}%. Tick: {tick_size}%\n"
                                                                             f"Pin range: {candle_range_perc}%. B|R ratio: {int(br_ratio)}/100. Bar part: {bar_part_filter}")

            if cHigh[-2] != cLow[-2]:
                atr = (sum(sum([cHigh[-2:-12:-1] - cLow[-2:-12:-1]])) / len(cClose[-2:-12:-1]))
                atr_per = atr / (cClose[-2] / 100)
                atr_per = float('{:.2f}'.format(atr_per))

                candle_range = cHigh[-2] - cLow[-2]
                candle_spread = abs(cOpen[-2] - cClose[-2])
                br_ratio = candle_spread / (candle_range / 100)
                range_part = candle_range / bar_part_filter
                candle_range_perc = (candle_range / cHigh[-2]) * 100
                candle_range_perc = float('{:.2f}'.format(candle_range_perc))

                # if ma1 >= ma2 >= ma3 >= ma4 >= ma5 >= ma6 >= ma7 >= ma8 >= ma9 >= ma10 or\
                #     ma1 <= ma2 <= ma3 <= ma4 <= ma5 <= ma6 <= ma7 <= ma8 <= ma9 <= ma10:
                if cClose[-2] <= price_filter:
                    if (sum(cVolume[-2:-12:-1]) / len(cVolume[-2:-12:-1])) / 1000 >= volume_filter:
                        if cVolume[-2] >= cVolume[-3]:
                            if atr_per >= atr10_perc_filter:
                                if candle_range_perc >= pin_range_filter:
                                    if br_ratio <= br_ratio_filter:
                                        if (cHigh[-2] >= cClose[-2] >= (cHigh[-2] - range_part)) or (cLow[-2] <= cClose[-2] <= (cLow[-2] + range_part)):

                                            # --- TICK SIZE ---
                                            url_tick = f"https://fapi.binance.com/fapi/v1/exchangeInfo"
                                            response = get(url_tick)
                                            data_tick = response.json()

                                            symbol_info = next(filter(lambda s: s['symbol'] == symbol, data_tick['symbols']), None)
                                            tick_size_filter = next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']), None)
                                            cTick = float(tick_size_filter['tickSize'])
                                            tick_size = cTick / (cClose[-2] / 100)
                                            tick_size = float('{:.4f}'.format(tick_size))

                                            if tick_size <= 0.01:
                                                bot3.send_message(662482931, f"{symbol}[-2]. Price: {cClose[-2]}. Vol 10MA: {int(((sum(cVolume[-1:-11:-1]) / len(cVolume[-1:-11:-1])) * cClose[-1]) / 1000)}.\n"
                                                                             f"ATR% 10MA: {atr_per}%. Tick: {tick_size}%\n"
                                                                             f"Pin range: {candle_range_perc}%. B|R ratio: {int(br_ratio)}/100. Bar part: {bar_part_filter}")
        except:
            print(f"Pin calculation error for: {symbol}")

