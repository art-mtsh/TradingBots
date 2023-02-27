import pandas as pd
from requests import get
from typing import List
from multiprocessing import Process, Manager
import telebot
import datetime

instruments1 = ["1000LUNCBUSD",
                "1000LUNCUSDT",
                "1000SHIBUSDT",
                "1000XECUSDT",
                "1INCHUSDT",
                "AAVEUSDT",
                "ADAUSDT",
                "ALGOUSDT",
                "ALICEUSDT",
                "ALPHAUSDT",
                "ANKRUSDT",
                "ANTUSDT",
                "APEUSDT",
                "API3USDT",
                "APTUSDT",
                "ARPAUSDT",
                "ARUSDT",
                "ATAUSDT",
                "ATOMUSDT",
                "AUDIOUSDT",
                "AVAXUSDT",
                "AXSUSDT",
                "BAKEUSDT",
                "BALUSDT",
                "BANDUSDT",
                "BATUSDT",
                "BCHUSDT",
                "BELUSDT",
                "BLUEBIRDUSDT",
                "BLZUSDT",
                "BNBUSDT",
                # "BNXUSDT",
                # "BTCDOMUSDT",
                # "BTCUSDT",
                # "BTCUSDT",
                "C98USDT",
                "CELOUSDT",
                "CELRUSDT",
                "CHRUSDT",
                "CHZUSDT",
                "COMPUSDT",
                "COTIUSDT",
                "CRVUSDT",
                "CTKUSDT",
                "CTSIUSDT",
                "CVXUSDT",
                "DARUSDT",
                "DASHUSDT",
                # "DEFIUSDT",
                "DENTUSDT"]
instruments2 = ["DGBUSDT",
                "DOGEUSDT",
                "DOTUSDT",
                "DUSKUSDT",
                "DYDXUSDT",
                "EGLDUSDT",
                "ENJUSDT",
                "ENSUSDT",
                # "EOSUSDT",
                "ETCUSDT",
                # "ETHUSDT",
                # "ETHUSDT",
                "FETUSDT",
                "FILUSDT",
                "FLMUSDT",
                "FLOWUSDT",
                "FOOTBALLUSDT",
                "FTMUSDT",
                "FXSUSDT",
                "GALAUSDT",
                "GALUSDT",
                "GMTUSDT",
                "GRTUSDT",
                "GTCUSDT",
                "HBARUSDT",
                "HIGHUSDT",
                "HNTUSDT",
                "HOOKUSDT",
                "HOTUSDT",
                "ICPUSDT",
                "ICXUSDT",
                "IMXUSDT",
                "INJUSDT",
                "IOSTUSDT",
                "IOTAUSDT",
                "IOTXUSDT",
                "JASMYUSDT",
                "KAVAUSDT",
                "KLAYUSDT"]
instruments3 = ["KNCUSDT",
                "KSMUSDT",
                "LDOUSDT",
                "LINAUSDT",
                "LINKUSDT",
                "LITUSDT",
                "LPTUSDT",
                "LRCUSDT",
                "LTCUSDT",
                "LUNA2USDT",
                "MAGICUSDT",
                "MANAUSDT",
                "MASKUSDT",
                "MATICUSDT",
                "MINAUSDT",
                "MKRUSDT",
                "MTLUSDT",
                "NEARUSDT",
                "NEOUSDT",
                "NKNUSDT",
                "OCEANUSDT",
                "OGNUSDT",
                "OMGUSDT",
                "ONEUSDT",
                "ONTUSDT",
                "OPUSDT",
                "PEOPLEUSDT",
                "QNTUSDT",
                "QTUMUSDT",
                "REEFUSDT",
                "RENUSDT",
                "RLCUSDT",
                "RNDRUSDT",
                "ROSEUSDT",
                "RSRUSDT"]
instruments4 = ["RUNEUSDT",
                "RVNUSDT",
                "SANDUSDT",
                "SFPUSDT",
                "SKLUSDT",
                "SNXUSDT",
                "SOLUSDT",
                # "SPELLUSDT",
                "STGUSDT",
                "STMXUSDT",
                "STORJUSDT",
                "STXUSDT",
                "SUSHIUSDT",
                "SXPUSDT",
                # "SSVUSDT",
                "THETAUSDT",
                "TOMOUSDT",
                "TRBUSDT",
                "TRXUSDT",
                "TUSDT",
                "UNFIUSDT",
                "UNIUSDT",
                "VETUSDT",
                "WAVESUSDT",
                "WOOUSDT",
                "XEMUSDT",
                "XLMUSDT",
                "XMRUSDT",
                "XRPUSDT",
                "XTZUSDT",
                # "YFIUSDT",
                "ZECUSDT",
                "ZENUSDT",
                "ZILUSDT",
                "ZRXUSDT"]

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

# --- FUNCTION ---
def screensaver(symbol: str, timeinterval: str) -> List:
    # --- DATA ---
    url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=100'
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

    '''
    upswingrange = 0

    if cHigh[-2] == max(cHigh[0:99]):
        for c in range(2, 20):
            if cClose[-c] > cClose[-c-1] and (abs(cOpen[-c] - cClose[-c]) / ((cHigh[-c] - cLow[-c]) / 100) > 75):
                upswingrange += abs(cClose[-c] - cClose[-c-1])
            else:
                break

    downswingrange = 0

    if cLow[-2] == min(cLow[0:99]):
        for c in range(2, 20):
            if cClose[-c] < cClose[-c-1] and (abs(cOpen[-c] - cClose[-c]) / ((cHigh[-c] - cLow[-c]) / 100) > 75):
                downswingrange += abs(cClose[-c-1] - cClose[-1])
            else:
                break

    upswingrange = upswingrange / (cClose[-1] / 100)
    upswingrange = float('{:.2f}'.format(upswingrange))

    downswingrange = downswingrange / (cClose[-1] / 100)
    downswingrange = float('{:.2f}'.format(downswingrange))

    swingrange = max(upswingrange, downswingrange)
    '''

    point1up_index = 0
    point1up_price = 0

    point2up_index = 0
    point2up_price = 0

    coefficient_falling = 0

    # if cHigh[-4] == max(cHigh[-2:-7:-1]):
    #     pass

    for a in range(2, 45):
        if cHigh[-a - 4] < cHigh[-a - 3] < cHigh[-a - 2] > cHigh[-a - 1] > cHigh[-a]:
            point1up_price = cHigh[-a - 2]
            point1up_index = -a - 2
            for b in range(a + 5, 45):
                if cHigh[-b - 4] < cHigh[-b - 3] < cHigh[-b - 2] > cHigh[-b - 1] > cHigh[-b] and cHigh[-a-2] < cHigh[-b - 2]:
                    point2up_price = cHigh[-b - 2]
                    point2up_index = -b - 2
                    coefficient_falling = (point1up_price - point2up_price) / (point1up_index - point2up_index)
                    break
            break

    point1dn_index = 0
    point1dn_price = 0

    point2dn_index = 0
    point2dn_price = 0

    coefficient_rising = 0

    # if cLow[-4] == min(cLow[-2:-7:-1]):
    #     pass

    for c in range(2, 45):
        if cLow[-c - 4] > cLow[-c - 3] > cLow[-c - 2] < cLow[-c - 1] < cLow[-c]:
            point1dn_price = cLow[-c - 2]
            point1dn_index = -c - 2
            for d in range(c + 5, 45):
                if cLow[-d - 4] > cLow[-d - 3] > cLow[-d - 2] < cLow[-d - 1] < cLow[-d] and cLow[-c - 2] > cLow[-d - 2]:
                    point2dn_price = cLow[-d - 2]
                    point2dn_index = -d - 2
                    coefficient_rising = (point1dn_price - point2dn_price) / (point1dn_index - point2dn_index)
                    break
            break

    signal = 0

    if coefficient_falling < 0 and coefficient_rising > 0:
        if cHigh[-1] < point1up_price - abs(coefficient_falling * point1up_index) and cLow[-1] > point1dn_price + abs(coefficient_rising * point1dn_index):
            signal += max(coefficient_rising, -coefficient_falling)

    signal = signal / (cClose[-1] / 100)
    signal = float('{:.6f}'.format(signal))

    atr = (sum(sum([cHigh - cLow])) / len(cClose))
    atrper = atr / (cClose[-1] / 100)
    atrper = float('{:.2f}'.format(atrper))

    # return [timeinterval, symbol, point1up_index, point1up_price, point2up_index, point2up_price, coefficient_falling, point1dn_index, point1dn_price, point2dn_index, point2dn_price, coefficient_rising, signal]
    return [timeinterval, symbol, atrper, signal, coefficient_rising, coefficient_falling]

def s_on_m11(my_list, searchfilter):
    for i in instruments1:
        data = screensaver(i, '1m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)


def s_on_m12(my_list, searchfilter):
    for i in instruments2:
        data = screensaver(i, '1m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m13(my_list, searchfilter):
    for i in instruments3:
        data = screensaver(i, '1m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m14(my_list, searchfilter):
    for i in instruments4:
        data = screensaver(i, '1m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m51(my_list, searchfilter):
    for i in instruments1:
        data = screensaver(i, '5m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m52(my_list, searchfilter):
    for i in instruments2:
        data = screensaver(i, '5m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m53(my_list, searchfilter):
    for i in instruments3:
        data = screensaver(i, '5m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m54(my_list, searchfilter):
    for i in instruments4:
        data = screensaver(i, '5m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m151(my_list, searchfilter):
    for i in instruments1:
        data = screensaver(i, '15m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m152(my_list, searchfilter):
    for i in instruments2:
        data = screensaver(i, '15m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m153(my_list, searchfilter):
    for i in instruments3:
        data = screensaver(i, '15m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def s_on_m154(my_list, searchfilter):
    for i in instruments4:
        data = screensaver(i, '15m')
        if 0 < data[-3] < searchfilter:
            my_list.append(data)

def get_data_table(searchfilter: float):
    manager = Manager()
    table_data = manager.list()

    p1 = Process(target=s_on_m11, args=(table_data, searchfilter,))
    p2 = Process(target=s_on_m12, args=(table_data, searchfilter,))
    p3 = Process(target=s_on_m13, args=(table_data, searchfilter,))
    p4 = Process(target=s_on_m14, args=(table_data, searchfilter,))

    p5 = Process(target=s_on_m51, args=(table_data, searchfilter,))
    p6 = Process(target=s_on_m52, args=(table_data, searchfilter,))
    p7 = Process(target=s_on_m53, args=(table_data, searchfilter,))
    p8 = Process(target=s_on_m54, args=(table_data, searchfilter,))

    p9 = Process(target=s_on_m151, args=(table_data, searchfilter,))
    p10 = Process(target=s_on_m152, args=(table_data, searchfilter,))
    p11 = Process(target=s_on_m153, args=(table_data, searchfilter,))
    p12 = Process(target=s_on_m154, args=(table_data, searchfilter,))

    # p13 = Process(target=s_on_m601, args=(table_data, atrfilter, searchfilter,))
    # p14 = Process(target=s_on_m602, args=(table_data, atrfilter, searchfilter,))
    # p15 = Process(target=s_on_m603, args=(table_data, atrfilter, searchfilter,))
    # p16 = Process(target=s_on_m604, args=(table_data, atrfilter, searchfilter,))

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
    # p13.start()
    # p14.start()
    # p15.start()
    # p16.start()

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
    # p13.join()
    # p14.join()
    # p15.join()
    # p16.join()

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
    # p13.close()
    # p14.close()
    # p15.close()
    # p16.close()

    return table_data
