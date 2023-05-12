import pandas as pd
from requests import get
from typing import List
from multiprocessing import Process, Manager
import instruments16
import telebot
import talib

# 10EMA basis
emabasis = 100

# 10EMA delta
emadelta = 1.25

# # price <= filter
# price_filter = 100000
#
# # volume >= filter
# volume_filter = 10
#
# # atr10 >= filter
# atr10_perc_filter = 0.0
#
# # pin range >= filter
# pin_range_filter = 0.4
#
# # body/range ratio <= filter
# br_ratio_filter = 10
#
# # close inside bar range / filter
# bar_part_filter = 3
#
# # tick size <= filter
# tick_size_filter = 0.03

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

def calculator(symbol: str, timeinterval: str) -> List:
    try:
        # --- DATA ---
        url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=650'
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

        # --- TICK SIZE ---
        url_tick = f"https://fapi.binance.com/fapi/v1/exchangeInfo"
        response = get(url_tick)
        data_tick = response.json()

        symbol_info = next(filter(lambda s: s['symbol'] == symbol, data_tick['symbols']), None)
        tick_size_filter = next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']), None)
        cTick1 = float(tick_size_filter['tickSize'])
        cTick = float(f"{cTick1:.8f}")
    except:
        print(f"Error downloading data for: {symbol}")

    ticksizeper = 0
    avgvolume_60 = 0
    atr_60m = 0
    atr_60per = 0
    volatility_60m10 = 0
    volatility_60m9 = 0
    volatility_60m8 = 0
    volatility_60m7 = 0
    volatility_60m6 = 0
    volatility_60m5 = 0
    volatility_60m4 = 0
    volatility_60m3 = 0
    volatility_60m2 = 0
    volatility_60m1 = 0
    tenema = 0

    # founded_pins = 0
    realized_pins = 0

    mangle = 0
    high_room_counter = 0
    low_room_counter = 0

    try:
        ticksizeper += (cTick / (cClose[-1] / 100))
        avgvolume_60 += int(((sum(cVolume[-1:-61:-1]) / len(cVolume[-1:-61:-1])) * cClose[-1]) / 1000)
        atr_60m += (sum(sum([cHigh[-1:-61:-1] - cLow[-1:-61:-1]])) / len(cClose[-1:-61:-1]))
        atr_60per += atr_60m / (cClose[-1] / 100)
        volatility_60m10 += ((max(cHigh[-541:-601:-1]) - min(cLow[-541:-601:-1])) / (cClose[-1] / 100))
        volatility_60m9 += ((max(cHigh[-481:-541:-1]) - min(cLow[-481:-541:-1])) / (cClose[-1] / 100))
        volatility_60m8 += ((max(cHigh[-421:-481:-1]) - min(cLow[-421:-481:-1])) / (cClose[-1] / 100))
        volatility_60m7 += ((max(cHigh[-361:-421:-1]) - min(cLow[-361:-421:-1])) / (cClose[-1] / 100))
        volatility_60m6 += ((max(cHigh[-301:-361:-1]) - min(cLow[-301:-361:-1])) / (cClose[-1] / 100))
        volatility_60m5 += ((max(cHigh[-241:-301:-1]) - min(cLow[-241:-301:-1])) / (cClose[-1] / 100))
        volatility_60m4 += ((max(cHigh[-181:-241:-1]) - min(cLow[-181:-241:-1])) / (cClose[-1] / 100))
        volatility_60m3 += ((max(cHigh[-121:-181:-1]) - min(cLow[-121:-181:-1])) / (cClose[-1] / 100))
        volatility_60m2 += ((max(cHigh[-61:-121:-1]) - min(cLow[-61:-121:-1])) / (cClose[-1] / 100))
        volatility_60m1 += ((max(cHigh[-1:-61:-1]) - min(cLow[-1:-61:-1])) / (cClose[-1] / 100))

        ma1 = talib.EMA(cClose, emabasis)[-1]
        ma2 = talib.EMA(cClose, int(emabasis * emadelta))[-1]
        ma3 = talib.EMA(cClose, int(emabasis * emadelta * emadelta))[-1]
        ma4 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta))[-1]
        ma5 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta))[-1]
        ma6 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
        ma7 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
        ma8 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
        ma9 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
        ma10 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]

        if ma1 >= ma2 >= ma3 >= ma3 >= ma4 >= ma5 >= ma6 >= ma7 >= ma8 >= ma9 >= ma10:
            tenema += 1
        elif ma1 <= ma2 <= ma3 <= ma4 <= ma5 <= ma6 <= ma7 <= ma8 <= ma9 <= ma10:
            tenema -= 1

        ma1 = sum(cClose[-1:-21:-1]) / 20
        ma2 = sum(cClose[-6:-26:-1]) / 20
        mangle += int(abs(ma1 - ma2) /  cTick)

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

    except:
        print(f"Error tick/volume/volatility/angle/room for: {symbol}")

    # try:
    #     for i in range(3, 604):
    #         if cHigh[-i] != cLow[-i]:
    #             atr = (sum(sum([cHigh[-i:-i-10:-1] - cLow[-i:-i-10:-1]])) / len(cClose[-i:-i-10:-1]))
    #             atr_per = atr / (cClose[-i] / 100)
    #             atr_per = float('{:.2f}'.format(atr_per))
    #
    #             candle_range = cHigh[-i] - cLow[-i]
    #             candle_spread = abs(cOpen[-i] - cClose[-i])
    #             br_ratio = candle_spread / (candle_range / 100)
    #             range_part = candle_range / bar_part_filter
    #             candle_range_perc = (candle_range / cHigh[-i]) * 100
    #             candle_range_perc = float('{:.2f}'.format(candle_range_perc))
    #
    #             if cClose[-i] <= price_filter:
    #                 if ((sum(cVolume[-i:-i-10:-1]) / len(cVolume[-i:-i-10:-1])) * cClose[-i]) / 1000 >= volume_filter:
    #                     if cVolume[-i] >= cVolume[-i-1]:
    #                         if atr_per >= atr10_perc_filter:
    #                             if candle_range_perc >= pin_range_filter:
    #                                 if br_ratio <= br_ratio_filter:
    #                                     if (cHigh[-i] >= cClose[-i] >= (cHigh[-i] - range_part)) or (cLow[-i] <= cClose[-i] <= (cLow[-i] + range_part)):
    #                                         founded_pins += 1
    #
    # except:
    #     print(f'Pin calculation error for: {symbol}[-1]')

    lastprice = float(cClose[-1])
    ticksizeper = float('{:.4f}'.format(ticksizeper))
    atr_60per = float('{:.2f}'.format(atr_60per))
    volatility_60m10 = float('{:.2f}'.format(volatility_60m10))
    volatility_60m9 = float('{:.2f}'.format(volatility_60m9))
    volatility_60m8 = float('{:.2f}'.format(volatility_60m8))
    volatility_60m7 = float('{:.2f}'.format(volatility_60m7))
    volatility_60m6 = float('{:.2f}'.format(volatility_60m6))
    volatility_60m5 = float('{:.2f}'.format(volatility_60m5))
    volatility_60m4 = float('{:.2f}'.format(volatility_60m4))
    volatility_60m3 = float('{:.2f}'.format(volatility_60m3))
    volatility_60m2 = float('{:.2f}'.format(volatility_60m2))
    volatility_60m1 = float('{:.2f}'.format(volatility_60m1))
    tenema = float('{:.2f}'.format(tenema))

    return [timeinterval,
            symbol,
            lastprice,
            ticksizeper,
            avgvolume_60,
            atr_60per,
            volatility_60m10,
            volatility_60m9,
            volatility_60m8,
            volatility_60m7,
            volatility_60m6,
            volatility_60m5,
            volatility_60m4,
            volatility_60m3,
            volatility_60m2,
            volatility_60m1,
            # mangle,
            tenema,
            max(high_room_counter, low_room_counter)]

def s_on_m1(instr, my_list, filter1, filter2, filter3, filter4):
    for i in instr:
        data = calculator(i, '1m')
        if data[2] <= filter1 and data[3] <= filter2 and data[4] >= filter3 and data[5] >= filter4:
            my_list.append(data)
            if data[-1] >= 120:
                bot3.send_message(662482931, f"{data[1]} room {data[-1]}")


def get_data_table(filter1, filter2, filter3, filter4):
    manager = Manager()
    table_data = manager.list()

    p1 = Process(target=s_on_m1, args=(instruments16.section_1, table_data, filter1, filter2, filter3, filter4,))
    p2 = Process(target=s_on_m1, args=(instruments16.section_2, table_data, filter1, filter2, filter3, filter4,))
    p3 = Process(target=s_on_m1, args=(instruments16.section_3, table_data, filter1, filter2, filter3, filter4,))
    p4 = Process(target=s_on_m1, args=(instruments16.section_4, table_data, filter1, filter2, filter3, filter4,))
    p5 = Process(target=s_on_m1, args=(instruments16.section_5, table_data, filter1, filter2, filter3, filter4,))
    p6 = Process(target=s_on_m1, args=(instruments16.section_6, table_data, filter1, filter2, filter3, filter4,))
    p7 = Process(target=s_on_m1, args=(instruments16.section_7, table_data, filter1, filter2, filter3, filter4,))
    p8 = Process(target=s_on_m1, args=(instruments16.section_8, table_data, filter1, filter2, filter3, filter4,))
    p9 = Process(target=s_on_m1, args=(instruments16.section_9, table_data, filter1, filter2, filter3, filter4,))
    p10 = Process(target=s_on_m1, args=(instruments16.section_10, table_data, filter1, filter2, filter3, filter4,))
    p11 = Process(target=s_on_m1, args=(instruments16.section_11, table_data, filter1, filter2, filter3, filter4,))
    p12 = Process(target=s_on_m1, args=(instruments16.section_12, table_data, filter1, filter2, filter3, filter4,))
    p13 = Process(target=s_on_m1, args=(instruments16.section_13, table_data, filter1, filter2, filter3, filter4,))
    p14 = Process(target=s_on_m1, args=(instruments16.section_14, table_data, filter1, filter2, filter3, filter4,))
    p15 = Process(target=s_on_m1, args=(instruments16.section_15, table_data, filter1, filter2, filter3, filter4,))
    p16 = Process(target=s_on_m1, args=(instruments16.section_16, table_data, filter1, filter2, filter3, filter4,))

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

    return table_data


