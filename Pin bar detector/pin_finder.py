import pandas as pd
from requests import get
import telebot
# import datetime

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

def pin_finder1(symbol: str):

    try:

        # --- DATA ---
        url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + '15m' + '&limit=15'
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

        cOpen = df1['cOpen'].to_numpy()
        cHigh = df1['cHigh'].to_numpy()
        cLow = df1['cLow'].to_numpy()
        cClose = df1['cClose'].to_numpy()
    except:
        print(f"Import error: {symbol}")

    try:
        if cHigh[-1] != cLow[-1]:
            candle_range = cHigh[-1] - cLow[-1]
            candle_spread = abs(cOpen[-1] - cClose[-1])
            br_ratio = candle_spread / (candle_range / 100)
            range_part = candle_range / 4
            candle_range_perc = (candle_range / cHigh[-1]) * 100
            candle_range_perc = float('{:.2f}'.format(candle_range_perc))

            if br_ratio < 20 and \
                    ((cHigh[-1] >= cClose[-1] >= (cHigh[-1] - range_part) and cLow[-1] <= min(cLow[-1:-2:-1]))
                    or
                    (cLow[-1] <= cClose[-1] <= (cLow[-1] + range_part) and cHigh[-1] >= max(cHigh[-1:-2:-1]))):
                bot3.send_message(662482931, f"{symbol}[-1], {candle_range_perc}%, {int(br_ratio)}/100")

        if cHigh[-2] != cLow[-2]:
            candle_range = cHigh[-2] - cLow[-2]
            candle_spread = abs(cOpen[-2] - cClose[-2])
            br_ratio = candle_spread / (candle_range / 100)
            range_part = candle_range / 4
            candle_range_perc = (candle_range / cHigh[-2]) * 100
            candle_range_perc = float('{:.2f}'.format(candle_range_perc))

            if br_ratio < 20 and \
                    ((cHigh[-2] >= cClose[-2] >= (cHigh[-2] - range_part))
                    or
                    (cLow[-2] <= cClose[-2] <= (cLow[-2] + range_part))):
                bot3.send_message(662482931, f"{symbol}[-2], {candle_range_perc}%, {int(br_ratio)}/100")
    except:
        print(f"Pin calculation error for: {symbol}")

        '''and cLow[-2] <= min(cLow[-1:-2:-1])'''
        '''and cHigh[-2] >= max(cHigh[-1:-2:-1])'''


