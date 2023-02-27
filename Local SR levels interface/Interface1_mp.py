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
    url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=1000'
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
    atr = (sum(sum([cHigh[950:] - cLow[950:]])) / len(cClose[950:]))
    atrper = atr / (cClose[-1] / 100)
    atrper = float('{:.2f}'.format(atrper))

    distancetores = 0
    respoint = 0

    for i in range(2, 890):
        point = -i-50
        if max(cHigh[point:point - 50:-1]) == cHigh[point]:
            clean = 0
            doubletouchup = 0
            for b in range(2, -point):
                if cHigh[-b] > cHigh[point] + cHigh[point] * 0.001:
                    clean += 1

            for b in range(20, -point - 20):
                if cHigh[point] + cHigh[point] * 0.001 >= cHigh[-b] >= cHigh[point] - cHigh[point] * 0.001:
                    doubletouchup += 1

            if clean == 0 and doubletouchup > 1:
                distancetores += (cHigh[point] - cClose[-1]) / (cClose[-1] / 100)
                respoint += cHigh[point]
                break

    distancetosup = 0
    suppoint = 0

    for i in range(2, 890):
        point = -i - 50
        if min(cLow[point:point - 50:-1]) == cLow[point]:
            clean = 0
            doubletouchdn = 0
            for b in range(2, -point):
                if cLow[-b] < cLow[point] - cLow[point] * 0.001:
                    clean += 1

            for b in range(20, -point - 20):
                if cLow[point] - cLow[point] * 0.001 <= cLow[-b] <= cLow[point] + cLow[point] * 0.001:
                    doubletouchdn += 1

            if clean == 0 and doubletouchdn > 1:
                distancetosup += (cClose[-1] - cLow[point]) / (cClose[-1] / 100)
                suppoint += cLow[point]
                break

    distancetores = float('{:.2f}'.format(distancetores))
    distancetosup = float('{:.2f}'.format(distancetosup))

    closestdistance: float
    closestlevel: float
    closesttype: str

    if distancetores != 0 and distancetosup != 0:
        if distancetores < distancetosup:
            closestdistance = distancetores
            closestlevel = respoint
            closesttype = "resistance"
        else:
            closestdistance = distancetosup
            closestlevel = suppoint
            closesttype = "support"
    elif distancetores != 0 and distancetosup == 0:
        closestdistance = distancetores
        closestlevel = respoint
        closesttype = "resistance"
    elif distancetores == 0 and distancetosup != 0:
        closestdistance = distancetosup
        closestlevel = suppoint
        closesttype = "support"
    else:
        closestdistance = 0
        closestlevel = 0
        closesttype = "none"

    return [timeinterval, symbol, atrper, closestdistance, closestlevel, closesttype]

def s_on_m11(my_list, atrfilter, searchfilter):
    for i in instruments1:
        data = screensaver(i, '1m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)
def s_on_m12(my_list, atrfilter, searchfilter):
    for i in instruments2:
        data = screensaver(i, '1m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)
def s_on_m13(my_list, atrfilter, searchfilter):
    for i in instruments3:
        data = screensaver(i, '1m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)
def s_on_m14(my_list, atrfilter, searchfilter):
    for i in instruments4:
        data = screensaver(i, '1m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)

def s_on_m51(my_list, atrfilter, searchfilter):
    for i in instruments1:
        data = screensaver(i, '5m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)
def s_on_m52(my_list, atrfilter, searchfilter):
    for i in instruments2:
        data = screensaver(i, '5m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)
def s_on_m53(my_list, atrfilter, searchfilter):
    for i in instruments3:
        data = screensaver(i, '5m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)
def s_on_m54(my_list, atrfilter, searchfilter):
    for i in instruments4:
        data = screensaver(i, '5m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)

def s_on_m151(my_list, atrfilter, searchfilter):
    for i in instruments1:
        data = screensaver(i, '15m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)
def s_on_m152(my_list, atrfilter, searchfilter):
    for i in instruments2:
        data = screensaver(i, '15m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)
def s_on_m153(my_list, atrfilter, searchfilter):
    for i in instruments3:
        data = screensaver(i, '15m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)
def s_on_m154(my_list, atrfilter, searchfilter):
    for i in instruments4:
        data = screensaver(i, '15m')
        if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
            my_list.append(data)

# def s_on_m601(my_list, atrfilter, searchfilter):
#     for i in instruments1:
#         data = screensaver(i, '1h')
#         if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
#             my_list.append(data)
# def s_on_m602(my_list, atrfilter, searchfilter):
#     for i in instruments2:
#         data = screensaver(i, '1h')
#         if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
#             my_list.append(data)
# def s_on_m603(my_list, atrfilter, searchfilter):
#     for i in instruments3:
#         data = screensaver(i, '1h')
#         if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
#             my_list.append(data)
# def s_on_m604(my_list, atrfilter, searchfilter):
#     for i in instruments4:
#         data = screensaver(i, '1h')
#         if data[-4] >= atrfilter and searchfilter >= data[-3] > 0:
#             my_list.append(data)

def get_data_table(atrfilter: float, searchfilter: float):
    manager = Manager()
    table_data = manager.list()

    p1 = Process(target=s_on_m11, args=(table_data, atrfilter, searchfilter,))
    p2 = Process(target=s_on_m12, args=(table_data, atrfilter, searchfilter,))
    p3 = Process(target=s_on_m13, args=(table_data, atrfilter, searchfilter,))
    p4 = Process(target=s_on_m14, args=(table_data, atrfilter, searchfilter,))

    p5 = Process(target=s_on_m51, args=(table_data, atrfilter, searchfilter,))
    p6 = Process(target=s_on_m52, args=(table_data, atrfilter, searchfilter,))
    p7 = Process(target=s_on_m53, args=(table_data, atrfilter, searchfilter,))
    p8 = Process(target=s_on_m54, args=(table_data, atrfilter, searchfilter,))

    p9 = Process(target=s_on_m151, args=(table_data, atrfilter, searchfilter,))
    p10 = Process(target=s_on_m152, args=(table_data, atrfilter, searchfilter,))
    p11 = Process(target=s_on_m153, args=(table_data, atrfilter, searchfilter,))
    p12 = Process(target=s_on_m154, args=(table_data, atrfilter, searchfilter,))

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


