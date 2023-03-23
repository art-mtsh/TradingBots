import pandas as pd
from requests import get
from typing import List
from multiprocessing import Process, Manager
from instruments import section_1, section_2, section_3, section_4

def calculator(symbol: str, timeinterval: str) -> List:
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
    data_tick = response.json()

    symbol_info = next(filter(lambda s: s['symbol'] == symbol, data_tick['symbols']), None)
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
    avgvolume_60 = 0
    ticksizeper = 0
    # signal = 0
    brratio_60 = 0
    brratio_10 = 0

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

        ticksizeper += (cTick / (cClose[-1] / 100))
        avgvolume_60 += int(((sum(cVolume[-1:-61:-1]) / len(cVolume[-1:-61:-1])) * cClose[-1]) / 1000)

        ratio_list = []
        for i in range(1, 61):
            if cHigh[-i] > 0 and cLow[-i] > 0 and cClose[-i] > 0 and cOpen[-i] > 0 and cHigh[-i] != cLow[-i]: # and cOpen[-i] != cClose[-i]:

                ratio = abs(cClose[-i] - cOpen[-i]) / ((cHigh[-i] - cLow[-i]) / 100)
                ratio_list.append(ratio)
            else:
                ratio_list.append(0)

        if sum(ratio_list[0:10]) > 0 and len(ratio_list[0:10]) > 0:
            brratio_10 += int(sum(ratio_list[0:10]) / len(ratio_list[0:10]))

        if sum(ratio_list) > 0 and len(ratio_list) > 0:
            brratio_60 += int(sum(ratio_list) / len(ratio_list))


        # point1up_index = 0
        # point1up_price = 0
        #
        # point2up_index = 0
        # point2up_price = 0
        #
        # coefficient_falling = 0
        #
        # for a in range(2, 45):
        #     if cHigh[-a - 4] < cHigh[-a - 3] < cHigh[-a - 2] > cHigh[-a - 1] > cHigh[-a]:
        #         point1up_price = cHigh[-a - 2]
        #         point1up_index = -a - 2
        #         for b in range(a + 5, 45):
        #             if cHigh[-b - 4] < cHigh[-b - 3] < cHigh[-b - 2] > cHigh[-b - 1] > cHigh[-b] and cHigh[-a - 2] < cHigh[-b - 2]:
        #                 point2up_price = cHigh[-b - 2]
        #                 point2up_index = -b - 2
        #                 coefficient_falling = (point1up_price - point2up_price) / (point1up_index - point2up_index)
        #                 for c in range(2, a + 2):
        #                     if cHigh[c] <= (point1up_price - coefficient_falling * (-point1up_index - c)):
        #                         pass
        #                     else:
        #                         coefficient_falling = 0
        #                         break
        #                 break
        #         break
        #
        # point1dn_index = 0
        # point1dn_price = 0
        #
        # point2dn_index = 0
        # point2dn_price = 0
        #
        # coefficient_rising = 0
        #
        # for a in range(2, 45):
        #     if cLow[-a - 4] > cLow[-a - 3] > cLow[-a - 2] < cLow[-a - 1] < cLow[-a]:
        #         point1dn_price = cLow[-a - 2]
        #         point1dn_index = -a - 2
        #         for b in range(a + 5, 45):
        #             if cLow[-b - 4] > cLow[-b - 3] > cLow[-b - 2] < cLow[-b - 1] < cLow[-b] and cLow[-a - 2] > cLow[-b - 2]:
        #                 point2dn_price = cLow[-b - 2]
        #                 point2dn_index = -b - 2
        #                 coefficient_rising = (point1dn_price - point2dn_price) / (point1dn_index - point2dn_index)
        #                 for c in range(2, a + 2):
        #                     if cLow[c] >= (point1dn_price + coefficient_rising * (-point1dn_index - c)):
        #                         pass
        #                     else:
        #                         coefficient_falling = 0
        #                         break
        #                 break
        #         break
        #
        # if coefficient_falling < 0 and coefficient_rising > 0:
        #     signal += 1

    except:
        print(f"Error for: {symbol}")

    ticksizeper = float('{:.4f}'.format(ticksizeper))
    volatility_60m = float('{:.2f}'.format(volatility_60m))
    atr_60per = float('{:.2f}'.format(atr_60per))
    lastprice = float(cClose[-1])

    return [timeinterval, symbol, ticksizeper, volatility_60m, atr_60per, brratio_60, brratio_10, avgvolume_60, lastprice]

def s_on_m11(my_list, searchfilter):
    for i in section_1:
        data = calculator(i, '1m')
        if data[2] < 0.01 and data[4] >= 0.2 and data[8] <= 6:
            my_list.append(data)
def s_on_m12(my_list, searchfilter):
    for i in section_2:
        data = calculator(i, '1m')
        if data[2] < 0.01 and data[4] >= 0.2 and data[8] <= 6:
            my_list.append(data)
def s_on_m13(my_list, searchfilter):
    for i in section_3:
        data = calculator(i, '1m')
        if data[2] < 0.01 and data[4] >= 0.2 and data[8] <= 6:
            my_list.append(data)
def s_on_m14(my_list, searchfilter):
    for i in section_4:
        data = calculator(i, '1m')
        if data[2] < 0.01 and data[4] >= 0.2 and data[8] <= 6:
            my_list.append(data)

def get_data_table(searchfilter: float):
    manager = Manager()
    table_data = manager.list()

    p1 = Process(target=s_on_m11, args=(table_data, searchfilter,))
    p2 = Process(target=s_on_m12, args=(table_data, searchfilter,))
    p3 = Process(target=s_on_m13, args=(table_data, searchfilter,))
    p4 = Process(target=s_on_m14, args=(table_data, searchfilter,))

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


