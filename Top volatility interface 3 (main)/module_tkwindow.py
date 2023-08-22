import tkinter as tk
import pandas as pd
from requests import get
from multiprocessing import Process, Manager
import instruments8
import telebot
import time
from module_information import information_func
from module_sonic import sonic_signal
import datetime

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

def calculation(instr, timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, formatted_text, exit_flag):
    while not exit_flag.value:
        # the_result = 'Starting...\n\n'
        for symbol in instr:
            # try:
            # --- DATA ---
            url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeframe_value.value + '&limit=110'
            # print(url_klines)
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
            # print(f'{cOpen}')

            data = [timeframe_value] + information_func(symbol=symbol, cHigh=cHigh, cLow=cLow, cClose=cClose, cVolume=cVolume) + \
                   sonic_signal(cOpen=cOpen, cHigh=cHigh, cLow=cLow, cClose=cClose)

            if data[2] <= price_value.value and data[3] <= tick_value.value and data[4] >= volume_value.value and data[5] >= atr_value.value and data[6] != "Sleep":
                # formatted_text.value += f'{data[1]} have price {data[2]} <= {price_value.value}, tick size is {data[3]} <= {tick_value.value}, volume is {data[4]} >= {volume_value.value} and ATR is {data[5]}% >= {atr_value.value}\n'
                formatted_text.value += f'{data[1]} have {data[6]} sonic\n'
                bot3.send_message(662482931, f"{data[1]} have {data[6]} sonic")
                
            # except:
            #     print(f'Error main module for {symbol}')
            
        # formatted_text.value += f"finished cycle at {datetime.datetime.now().strftime('%H:%M:%S')}\n"
        time.sleep(refresh_time.value)

def tk_window(timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, exit_flag, formatted_text):
    def save_values():
        timeframe_value.value = str(timeframe_entry.get())
        price_value.value = int(price_entry.get())
        tick_value.value = float(tick_entry.get())
        volume_value.value = int(volume_entry.get())
        atr_value.value = float(atr_entry.get())
        refresh_time.value = int(refresh_entry.get())

    def update_label():
        result_label.config(text=formatted_text.value)
        root.after(1000, update_label)  # Update the label every 1 second

    root = tk.Tk()
    root.title("Input Window")
    root.geometry("700x500")  # Set window dimensions
    root.iconphoto(True, tk.PhotoImage(file='tk_logo2.png'))  # Set window icon
    
    # Create frames for left and right zones with borders
    left_frame = tk.Frame(borderwidth=2, relief="solid")  # Add border and relief options
    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    
    right_frame = tk.Frame(borderwidth=2, relief="solid")  # Add border and relief options
    right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)
    
    # Default values
    default_timeframe = timeframe_value.value
    default_price = price_value.value
    default_tick = tick_value.value
    default_volume = volume_value.value
    default_atr = atr_value.value
    default_refresh = refresh_time.value

    # Create input fields and labels in the left zone
    
    timeframe_label = tk.Label(left_frame, text="Timeframe analysis:")
    timeframe_label.pack(anchor="w")
    timeframe_entry = tk.Entry(left_frame, validate="key", width=30)
    timeframe_entry.insert(0, default_timeframe)
    timeframe_entry.pack(anchor="w")
    
    price_label = tk.Label(left_frame, text="Current $-price, max:")
    price_label.pack(anchor="w")
    price_entry = tk.Entry(left_frame, validate="key", width=30)
    price_entry.insert(0, default_price)
    price_entry.pack(anchor="w")

    tick_label = tk.Label(left_frame, text="Tick size in %, max:")
    tick_label.pack(anchor="w")
    tick_entry = tk.Entry(left_frame, validate="key", width=30)
    tick_entry.insert(0, default_tick)
    tick_entry.pack(anchor="w")

    volume_label = tk.Label(left_frame, text="Volume 1000$/minute, min :")
    volume_label.pack(anchor="w")
    volume_entry = tk.Entry(left_frame, validate="key", width=30)
    volume_entry.insert(0, default_volume)
    volume_entry.pack(anchor="w")

    atr_label = tk.Label(left_frame, text="ATR in %, min:")
    atr_label.pack(anchor="w")
    atr_entry = tk.Entry(left_frame, validate="key", width=30)
    atr_entry.insert(0, default_atr)
    atr_entry.pack(anchor="w")

    refresh_label = tk.Label(left_frame, text="Refresh speed, seconds:")
    refresh_label.pack(anchor="w")
    refresh_entry = tk.Entry(left_frame, validate="key", width=30)
    refresh_entry.insert(0, default_refresh)
    refresh_entry.pack(anchor="w")

    save_button = tk.Button(left_frame, text="Save", command=save_values)
    save_button.pack(anchor="w")

    # Add a label to display values in the right zone
    result_label = tk.Label(right_frame, text="", justify='left')
    result_label.pack(fill="both", expand=True)

    # Register the closing event handler
    def on_closing():
        exit_flag.value = True
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)  # Call on_closing() when the window is closed

    # Start the label update loop
    update_label()

    # Start the Tkinter event loop
    root.mainloop()

def search_active():
    with Manager() as manager:
        timeframe_value = manager.Value('s', '15m')
        price_value = manager.Value('i', 2000)
        tick_value = manager.Value('d', 0.02)
        volume_value = manager.Value('i', 50)
        atr_value = manager.Value('d', 0.40)
        refresh_time = manager.Value('i', 60)
        exit_flag = manager.Value('b', False)
        formatted_text = manager.Value('s', "")  # Shared formatted text variable
        

        # Create the Tkinter window process
        p1 = Process(target=tk_window, args=(timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, exit_flag, formatted_text))
        p2 = Process(target=calculation, args=(instruments7.section_1, timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, formatted_text, exit_flag))
        p3 = Process(target=calculation, args=(instruments7.section_2, timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, formatted_text, exit_flag))
        p4 = Process(target=calculation, args=(instruments7.section_3, timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, formatted_text, exit_flag))
        p5 = Process(target=calculation, args=(instruments7.section_4, timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, formatted_text, exit_flag))
        p6 = Process(target=calculation, args=(instruments7.section_5, timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, formatted_text, exit_flag))
        p7 = Process(target=calculation, args=(instruments7.section_6, timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, formatted_text, exit_flag))
        p8 = Process(target=calculation, args=(instruments7.section_7, timeframe_value, price_value, tick_value, volume_value, atr_value, refresh_time, formatted_text, exit_flag))
        
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()
        p8.start()
        
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()
        p8.join()

if __name__ == '__main__':
    search_active()
