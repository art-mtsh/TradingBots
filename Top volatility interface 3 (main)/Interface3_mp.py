import pandas as pd
from requests import get
from typing import List
from multiprocessing import Process, Manager
from instruments import section_1, section_2, section_3, section_4
import telebot

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
    volatility_10m = 0

    pin_height = 0
    pin_width = 0
    pinOpen = 0
    pinHigh = 0
    pinLow = 0
    pinClose = 0

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
        volatility_10m += ((max(cHigh[-1:-11:-1]) - min(cLow[-1:-11:-1])) / (cClose[-1] / 100))
        ma1 = sum(cClose[-1:-21:-1]) / 20
        ma2 = sum(cClose[-6:-26:-1]) / 20
        mangle += int(abs(ma1 - ma2) /  cTick)

        for i in range(2, 121):
            if cHigh[-1] >= cHigh[-i]:
                high_room_counter += 1
            else:
                break

        for i in range(2, 121):
            if cLow[-1] <= cLow[-i]:
                low_room_counter += 1
            else:
                break

    except:
        print(f"Error tick/volume/volatility/angle/room for: {symbol}")

    try:

        if cHigh[-2] != cLow[-2]:
            br_ratio = abs(cClose[-2] - cOpen[-2]) / ((cHigh[-2] - cLow[-2]) / 100)
            third = (cHigh[-2] - cLow[-2]) / 5
            if br_ratio < 25 and ((cHigh[-2] > cClose[-2] > cHigh[-2] - third)
                                  or
                                  (cLow[-2] < cClose[-2] < cLow[-2] + third)):
                pin_height += ((cHigh[-2] - cLow[-2]) / cHigh[-2]) * 100
                pin_width += i-1
    except:
        print(f"Error pin-bar for: {symbol}")

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
    volatility_10m = float('{:.2f}'.format(volatility_10m))
    pin_height = float('{:.2f}'.format(pin_height))

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
            mangle,
            volatility_10m,
            pin_height,
            pin_width,
            max(high_room_counter, low_room_counter)]

def s_on_m11(my_list, filter1, filter2, filter3, filter4):
    for i in section_1:
        data = calculator(i, '1m')
        if data[2] <= filter1 and data[3] <= filter2 and data[4] >= filter3 and data[5] >= filter4:
            my_list.append(data)
            # if data[-5] > 0:
            #     bot3.send_message(662482931, f"{data[1]} pin on {data[-5]}, width: {data[-6]}\n"
            #                                  f"O:{data[-4]}, H:{data[-3]}, L:{data[-2]}, C:{data[-1]}")

def s_on_m12(my_list, filter1, filter2, filter3, filter4):
    for i in section_2:
        data = calculator(i, '1m')
        if data[2] <= filter1 and data[3] <= filter2 and data[4] >= filter3 and data[5] >= filter4:
            my_list.append(data)
            # if data[-5] > 0:
            #     bot3.send_message(662482931, f"{data[1]} pin on {data[-5]}, width: {data[-6]}\n"
            #                                  f"O:{data[-4]}, H:{data[-3]}, L:{data[-2]}, C:{data[-1]}")

def s_on_m13(my_list, filter1, filter2, filter3, filter4):
    for i in section_3:
        data = calculator(i, '1m')
        if data[2] <= filter1 and data[3] <= filter2 and data[4] >= filter3 and data[5] >= filter4:
            my_list.append(data)
            # if data[-5] > 0:
            #     bot3.send_message(662482931, f"{data[1]} pin on {data[-5]}, width: {data[-6]}\n"
            #                                  f"O:{data[-4]}, H:{data[-3]}, L:{data[-2]}, C:{data[-1]}")

def s_on_m14(my_list, filter1, filter2, filter3, filter4):
    for i in section_4:
        data = calculator(i, '1m')
        if data[2] <= filter1 and data[3] <= filter2 and data[4] >= filter3 and data[5] >= filter4:
            my_list.append(data)
            # if data[-5] > 0:
            #     bot3.send_message(662482931, f"{data[1]} pin on {data[-5]}, width: {data[-6]}\n"
            #                                  f"O:{data[-4]}, H:{data[-3]}, L:{data[-2]}, C:{data[-1]}")

def get_data_table(filter1, filter2, filter3, filter4):
    manager = Manager()
    table_data = manager.list()

    p1 = Process(target=s_on_m11, args=(table_data, filter1, filter2, filter3, filter4,))
    p2 = Process(target=s_on_m12, args=(table_data, filter1, filter2, filter3, filter4,))
    p3 = Process(target=s_on_m13, args=(table_data, filter1, filter2, filter3, filter4,))
    p4 = Process(target=s_on_m14, args=(table_data, filter1, filter2, filter3, filter4,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    p1.close()
    p2.close()
    p3.close()
    p4.close()

    return table_data


