import pandas as pd
from requests import get
import telebot
import talib

# import datetime

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

# price <= filter
price_filter = 100000

# volume >= filter
volume_filter = 10

# atr10 >= filter
atr10_perc_filter = 0.0

# pin range >= filter
pin_range_filter = 0.2

# body/range ratio <= filter
br_ratio_filter = 15

# close inside bar range / filter
bar_part_filter = 3

# tick size <= filter
tick_size_filter = 0.04

# EMA basis
ema_basis = 10

# EMA delta
ema_delta = 10

def pin_finder1(sym: list):
    for symbol in sym:

        try:

            # --- DATA ---
            url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + '1m' + '&limit=20'
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

            ma1 = talib.EMA(cClose, 0 * ema_delta + ema_basis)
            ma2 = talib.EMA(cClose, 1 * ema_delta + ema_basis)
            ma3 = talib.EMA(cClose, 2 * ema_delta + ema_basis)
            ma4 = talib.EMA(cClose, 3 * ema_delta + ema_basis)
            ma5 = talib.EMA(cClose, 4 * ema_delta + ema_basis)
            ma6 = talib.EMA(cClose, 5 * ema_delta + ema_basis)
            ma7 = talib.EMA(cClose, 6 * ema_delta + ema_basis)
            ma8 = talib.EMA(cClose, 7 * ema_delta + ema_basis)
            ma9 = talib.EMA(cClose, 8 * ema_delta + ema_basis)
            ma10 = talib.EMA(cClose, 9 * ema_delta + ema_basis)

            if ma1[-1] >= ma2[-1]:
                bot3.send_message(662482931, f"21erdfwsddvsd")

            if ma1[-1] >= ma2[-1] >= ma3[-1] >= ma4[-1] >= ma5[-1] >= ma6[-1] >= ma7[-1] >= ma8[-1] >= ma9[-1] >= ma10[-1]:
                bot3.send_message(662482931, f"Rising {symbol}")
                if ma1[-2] <= ma2[-2]:
                    bot3.send_message(662482931, f"Cross OVER on {symbol}")
            elif ma1[-1] <= ma2[-1] <= ma3[-1] <= ma4[-1] <= ma5[-1] <= ma6[-1] <= ma7[-1] <= ma8[-1] <= ma9[-1] <= ma10[-1]:
                bot3.send_message(662482931, f"Falling {symbol}")
                if ma1[-2] >= ma2[-2]:
                    bot3.send_message(662482931, f"Cross UNDER on {symbol}")

        except:
            print(f'Pin calculation error for: {symbol}[-1]')



