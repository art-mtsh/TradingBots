import pandas as pd
from requests import get
from multiprocessing import Process, Manager
import instruments16
import telebot
from module_information import information_func
from module_ten_ema import ten_ema_function
from module_room import room_function
from module_levels import levels_func

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

def calculation(instr, my_list, filter1, filter2, filter3, filter4):

    try:
        timeinterval = '1m'

        for symbol in instr:
            # --- DATA ---
            url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=1000'
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

            data = [timeinterval] + \
                   information_func(symbol=symbol, cHigh=cHigh, cLow=cLow, cClose=cClose, cVolume=cVolume) + \
                   ten_ema_function(cClose=cClose, emabasis=50, emadelta=1.2) + \
                   room_function(cHigh=cHigh, cLow=cLow, cClose=cClose) + \
                   levels_func(symbol=symbol, cHigh=cHigh, cLow=cLow, cClose=cClose)


            if data[2] <= filter1 and data[3] <= filter2 and data[4] >= filter3 and data[5] >= filter4:
                my_list.append(data)
                if data[-3] >= 60:
                    bot3.send_message(662482931, f"{data[1]} room {data[-3]}")
                # if 0 < data[-1] <= 0.5:
                #     bot3.send_message(662482931, f"{data[1]} level {data[-2]} in {data[-1]}%")
    except:
        print(f'Error main module for {symbol}')

def get_data_table(filter1, filter2, filter3, filter4):
    manager = Manager()
    table_data = manager.list()

    p1 = Process(target=calculation, args=(instruments16.section_1, table_data, filter1, filter2, filter3, filter4,))
    p2 = Process(target=calculation, args=(instruments16.section_2, table_data, filter1, filter2, filter3, filter4,))
    p3 = Process(target=calculation, args=(instruments16.section_3, table_data, filter1, filter2, filter3, filter4,))
    p4 = Process(target=calculation, args=(instruments16.section_4, table_data, filter1, filter2, filter3, filter4,))
    p5 = Process(target=calculation, args=(instruments16.section_5, table_data, filter1, filter2, filter3, filter4,))
    p6 = Process(target=calculation, args=(instruments16.section_6, table_data, filter1, filter2, filter3, filter4,))
    p7 = Process(target=calculation, args=(instruments16.section_7, table_data, filter1, filter2, filter3, filter4,))
    p8 = Process(target=calculation, args=(instruments16.section_8, table_data, filter1, filter2, filter3, filter4,))
    p9 = Process(target=calculation, args=(instruments16.section_9, table_data, filter1, filter2, filter3, filter4,))
    p10 = Process(target=calculation, args=(instruments16.section_10, table_data, filter1, filter2, filter3, filter4,))
    p11 = Process(target=calculation, args=(instruments16.section_11, table_data, filter1, filter2, filter3, filter4,))
    p12 = Process(target=calculation, args=(instruments16.section_12, table_data, filter1, filter2, filter3, filter4,))
    p13 = Process(target=calculation, args=(instruments16.section_13, table_data, filter1, filter2, filter3, filter4,))
    p14 = Process(target=calculation, args=(instruments16.section_14, table_data, filter1, filter2, filter3, filter4,))
    p15 = Process(target=calculation, args=(instruments16.section_15, table_data, filter1, filter2, filter3, filter4,))
    p16 = Process(target=calculation, args=(instruments16.section_16, table_data, filter1, filter2, filter3, filter4,))

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

