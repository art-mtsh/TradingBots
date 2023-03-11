import pandas as pd
from requests import get
from typing import List
from multiprocessing import Process, Manager
from instruments import section_1, section_2, section_3, section_4


# --- FUNCTION ---
def screensaver(symbol: str, timeinterval: str) -> List:
    # --- DATA ---
    url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=300'
    data1 = get(url_klines).json()

    # --- K-LINE ---
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

    # Lists:
    cOpen = df1['cOpen'].to_numpy()
    cHigh = df1['cHigh'].to_numpy()
    cLow = df1['cLow'].to_numpy()
    cClose = df1['cClose'].to_numpy()
    cVolume = df1['cVolume'].to_numpy()

    url_tick = f"https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = get(url_tick)
    data = response.json()


    symbol_info = next(filter(lambda s: s['symbol'] == symbol, data['symbols']), None)
    tick_size_filter = next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']), None)
    cTick1 = float(tick_size_filter['tickSize'])
    cTick = float(f"{cTick1:.8f}")

    atr_10m = 0
    atr_60m = 0
    atr_240m = 0
    volatility_10m = 0
    volatility_60m = 0
    volatility_240m = 0
    atr_10per = 0
    atr_60per = 0
    atr_240per = 0
    mpl_10 = 0
    mpl_60 = 0
    mpl_240 = 0

    try:
        atr_10m += (sum(sum([cHigh[-1:-11:-1] - cLow[-1:-11:-1]])) / len(cClose[-1:-11:-1]))
        atr_60m += (sum(sum([cHigh[-1:-61:-1] - cLow[-1:-61:-1]])) / len(cClose[-1:-61:-1]))
        atr_240m += (sum(sum([cHigh[-1:-241:-1] - cLow[-1:-241:-1]])) / len(cClose[-1:-241:-1]))

        atr_10per += atr_10m / (cClose[-1] / 100)
        atr_60per += atr_60m / (cClose[-1] / 100)
        atr_240per += atr_240m / (cClose[-1] / 100)

        volatility_10m += abs((max(cHigh[-1:-11:-1]) - min(cLow[-1:-11:-1])) / (cClose[-1] / 100))
        volatility_60m += abs((max(cHigh[-1:-61:-1]) - min(cLow[-1:-61:-1])) / (cClose[-1] / 100))
        volatility_240m += abs((max(cHigh[-1:-240:-1]) - min(cLow[-1:-240:-1])) / (cClose[-1] / 100))

        if atr_10m != 0 and volatility_10m != 0:
            mpl_10 += int(abs(volatility_10m / atr_10per))

        if atr_60m != 0 and volatility_60m != 0:
            mpl_60 += int(abs(volatility_60m / atr_60per))

        if atr_240m != 0 and volatility_240m != 0:
            mpl_240 += int(abs(volatility_240m / atr_240per))

    except:
        print(f"Error for: {symbol}")

    atr_10per = float('{:.2f}'.format(atr_10per))
    atr_60per = float('{:.2f}'.format(atr_60per))
    atr_240per = float('{:.2f}'.format(atr_240per))

    volatility_10m = float('{:.2f}'.format(volatility_10m))
    volatility_60m = float('{:.2f}'.format(volatility_60m))
    volatility_240m = float('{:.2f}'.format(volatility_240m))

    avgvolume_60 = int(((sum(cVolume[-1:-61:-1]) / len(cVolume[-1:-61:-1])) * cClose[-1]) / 1000)

    ticksizeper = (cTick / (cClose[-1] / 100))
    ticksizeper = float('{:.4f}'.format(ticksizeper))

    return [timeinterval, symbol, ticksizeper, volatility_60m, atr_60per, avgvolume_60]

def s_on_m11(my_list, searchfilter):
    for i in section_1:
        data = screensaver(i, '1m')
        if data[2] <= 0.01 and abs(data[4]) > 0.2 and data[5] >= 100:
            my_list.append(data)
def s_on_m12(my_list, searchfilter):
    for i in section_2:
        data = screensaver(i, '1m')
        if data[2] <= 0.01 and abs(data[4]) > 0.2 and data[5] >= 100:
            my_list.append(data)
def s_on_m13(my_list, searchfilter):
    for i in section_3:
        data = screensaver(i, '1m')
        if data[2] <= 0.01 and abs(data[4]) > 0.2 and data[5] >= 100:
            my_list.append(data)
def s_on_m14(my_list, searchfilter):
    for i in section_4:
        data = screensaver(i, '1m')
        if data[2] <= 0.01 and abs(data[4]) > searchfilter and data[5] >= 100:
            my_list.append(data)

# def s_on_m51(my_list, searchfilter):
#     for i in section_1:
#         data = screensaver(i, '5m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
# def s_on_m52(my_list, searchfilter):
#     for i in section_2:
#         data = screensaver(i, '5m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
# def s_on_m53(my_list, searchfilter):
#     for i in section_3:
#         data = screensaver(i, '5m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
# def s_on_m54(my_list, searchfilter):
#     for i in section_4:
#         data = screensaver(i, '5m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
#
# def s_on_m151(my_list, searchfilter):
#     for i in section_1:
#         data = screensaver(i, '15m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
# def s_on_m152(my_list, searchfilter):
#     for i in section_2:
#         data = screensaver(i, '15m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
# def s_on_m153(my_list, searchfilter):
#     for i in section_3:
#         data = screensaver(i, '15m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
# def s_on_m154(my_list, searchfilter):
#     for i in section_4:
#         data = screensaver(i, '15m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
#
# def s_on_m301(my_list, searchfilter):
#     for i in section_1:
#         data = screensaver(i, '30m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
# def s_on_m302(my_list, searchfilter):
#     for i in section_2:
#         data = screensaver(i, '30m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
# def s_on_m303(my_list, searchfilter):
#     for i in section_3:
#         data = screensaver(i, '30m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)
# def s_on_m304(my_list, searchfilter):
#     for i in section_4:
#         data = screensaver(i, '30m')
#         if abs(data[2]) > searchfilter:
#             my_list.append(data)

def get_data_table(searchfilter: float):
    manager = Manager()
    table_data = manager.list()

    p1 = Process(target=s_on_m11, args=(table_data, searchfilter,))
    p2 = Process(target=s_on_m12, args=(table_data, searchfilter,))
    p3 = Process(target=s_on_m13, args=(table_data, searchfilter,))
    p4 = Process(target=s_on_m14, args=(table_data, searchfilter,))

    # p5 = Process(target=s_on_m51, args=(table_data, searchfilter,))
    # p6 = Process(target=s_on_m52, args=(table_data, searchfilter,))
    # p7 = Process(target=s_on_m53, args=(table_data, searchfilter,))
    # p8 = Process(target=s_on_m54, args=(table_data, searchfilter,))

    # p9 = Process(target=s_on_m151, args=(table_data, searchfilter,))
    # p10 = Process(target=s_on_m152, args=(table_data, searchfilter,))
    # p11 = Process(target=s_on_m153, args=(table_data, searchfilter,))
    # p12 = Process(target=s_on_m154, args=(table_data, searchfilter,))
    #
    # p13 = Process(target=s_on_m301, args=(table_data, searchfilter,))
    # p14 = Process(target=s_on_m302, args=(table_data, searchfilter,))
    # p15 = Process(target=s_on_m303, args=(table_data, searchfilter,))
    # p16 = Process(target=s_on_m304, args=(table_data, searchfilter,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    # p5.start()
    # p6.start()
    # p7.start()
    # p8.start()
    # p9.start()
    # p10.start()
    # p11.start()
    # p12.start()
    # p13.start()
    # p14.start()
    # p15.start()
    # p16.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    # p5.join()
    # p6.join()
    # p7.join()
    # p8.join()
    # p9.join()
    # p10.join()
    # p11.join()
    # p12.join()
    # p13.join()
    # p14.join()
    # p15.join()
    # p16.join()
    #
    p1.close()
    p2.close()
    p3.close()
    p4.close()
    # p5.close()
    # p6.close()
    # p7.close()
    # p8.close()
    # p9.close()
    # p10.close()
    # p11.close()
    # p12.close()
    # p13.close()
    # p14.close()
    # p15.close()
    # p16.close()

    return table_data


