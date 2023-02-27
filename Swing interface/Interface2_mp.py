import pandas as pd
from requests import get
from typing import List
from multiprocessing import Process, Manager


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
                   # "XEMUSDT",
                   "XLMUSDT",
                   "XMRUSDT",
                   "XRPUSDT",
                   "XTZUSDT",
                   # "YFIUSDT",
                   "ZECUSDT",
                   "ZENUSDT",
                   "ZILUSDT",
                   "ZRXUSDT"]

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

    maxpoint = max(cHigh[-2: -100: -1])
    upswingrange = 0

    for i in range(2, 10):
        if cHigh[-i] == maxpoint:
            for s in range(i, 50):
                if cClose[-s] > cClose[-s-1]:
                    upswingrange += cClose[-s] - cClose[-s-1]
                else:
                    break

    if upswingrange != 0 and maxpoint > max(cHigh[list(cHigh).index(maxpoint)+1:101]) and min(cLow[list(cHigh).index(maxpoint)+1:101]) > maxpoint - upswingrange / 3:
        upswingrange = upswingrange
    else:
        upswingrange = 0

    minpoint = min(cLow[-2: -100: -1])
    downswingrange = 0

    for i in range(2, 10):
        if cLow[-i] == minpoint:
            for s in range(i, 50):
                if cClose[-s] < cClose[-s - 1]:
                    downswingrange += cClose[-s - 1] - cClose[-s]
                else:
                    break

    if downswingrange != 0 and minpoint < min(cLow[list(cLow).index(minpoint)+1:101]) and max(cHigh[list(cLow).index(minpoint)+1:101]) < minpoint + downswingrange / 3:
        downswingrange = downswingrange
    else:
        downswingrange = 0

    upswingrange = upswingrange / (cClose[-1] / 100)
    upswingrange = float('{:.2f}'.format(upswingrange))

    downswingrange = downswingrange / (cClose[-1] / 100)
    downswingrange = float('{:.2f}'.format(downswingrange))

    swingrange = max(upswingrange, downswingrange)

    return [timeinterval, symbol, swingrange]

def s_on_m11(my_list, searchfilter):
    for i in instruments1:
        data = screensaver(i, '1m')
        if data[-1] > searchfilter:
            my_list.append(data)
def s_on_m12(my_list, searchfilter):
    for i in instruments2:
        data = screensaver(i, '1m')
        if data[-1] > searchfilter:
            my_list.append(data)
def s_on_m13(my_list, searchfilter):
    for i in instruments3:
        data = screensaver(i, '1m')
        if data[-1] > searchfilter:
            my_list.append(data)
def s_on_m14(my_list, searchfilter):
    for i in instruments4:
        data = screensaver(i, '1m')
        if data[-1] > searchfilter:
            my_list.append(data)

def s_on_m51(my_list, searchfilter):
    for i in instruments1:
        data = screensaver(i, '5m')
        if data[-1] > searchfilter:
            my_list.append(data)
def s_on_m52(my_list, searchfilter):
    for i in instruments2:
        data = screensaver(i, '5m')
        if data[-1] > searchfilter:
            my_list.append(data)
def s_on_m53(my_list, searchfilter):
    for i in instruments3:
        data = screensaver(i, '5m')
        if data[-1] > searchfilter:
            my_list.append(data)
def s_on_m54(my_list, searchfilter):
    for i in instruments4:
        data = screensaver(i, '5m')
        if data[-1] > searchfilter:
            my_list.append(data)

def s_on_m151(my_list, searchfilter):
    for i in instruments1:
        data = screensaver(i, '15m')
        if data[-1] > searchfilter:
            my_list.append(data)
def s_on_m152(my_list, searchfilter):
    for i in instruments2:
        data = screensaver(i, '15m')
        if data[-1] > searchfilter:
            my_list.append(data)
def s_on_m153(my_list, searchfilter):
    for i in instruments3:
        data = screensaver(i, '15m')
        if data[-1] > searchfilter:
            my_list.append(data)
def s_on_m154(my_list, searchfilter):
    for i in instruments4:
        data = screensaver(i, '15m')
        if data[-1] > searchfilter:
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


