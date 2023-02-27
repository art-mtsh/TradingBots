# import datetime
# import pandas
# import numpy as np
import telebot
# from requests import get
import os

# --- TELEGRAM ---

TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
bot3 = telebot.TeleBot(TOKEN3)

# bot3.send_message(662482931, "1234124123")

filename = "log.txt"

# Check if line exists in the file
with open(filename, "r+") as file:
    if "hello world" not in file.read():
        # Move the file pointer to the beginning of the file
        file.seek(0)

        # Write the new lines to the file
        file.write("hello world\n")
        file.write("12345\n")

# Close the file
file.close()

