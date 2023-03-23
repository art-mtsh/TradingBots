# import datetime
import pandas as pd
# import numpy as np
import telebot
# from requests import get
import os
import requests
import math

# --- TELEGRAM ---

# TOKEN3 = '6077915522:AAFuMUVPhw-cEaX4gCuPOa-chVwwMTpsUz8'
# bot3 = telebot.TeleBot(TOKEN3)

# bot3.send_message(662482931, "1234124123")


# import requests
#
# # set the symbol you want to get the depth for
# symbol = 'LQTYUSDT'
#
# # set the search distance (in percent)
# searchdistance = 3
#
# # make a request to the Binance API endpoint for the symbol depth
# url_depth = f"https://api.binance.com/api/v3/depth?symbol={symbol}"
# response = requests.get(url_depth)
#
# # parse the response and get the bids and asks data
# data = response.json()
# bids = data['bids']
# asks = data['asks']
#
# # print(data)
#
# # get the current price
# current_price = float(data['lastUpdateId']) * 0.00000001
#
# print(f"Current price: {current_price}")
# print("")
#
# # calculate the minimum and maximum prices for the search distance
# min_price = current_price * (1 - searchdistance/100)
# max_price = current_price * (1 + searchdistance/100)
#
# print(f"Min search price: {min_price}")
# print(f"Max search price: {max_price}")
# print("")
#
# # filter the bids and asks based on the search distance
# bids_within_search_distance = [b for b in bids if float(b[0]) >= min_price and float(b[0]) <= max_price]
# asks_within_search_distance = [a for a in asks if float(a[0]) >= min_price and float(a[0]) <= max_price]
#
# print(f"Bids within distance: {bids_within_search_distance}")
# print(f"Asks within distance: {asks_within_search_distance}")
# print("")
#
# # calculate the total sum of bids and asks within the search distance
# bidssum = sum(float(b[1]) for b in bids_within_search_distance)
# askssum = sum(float(a[1]) for a in asks_within_search_distance)
#
# # print the results
# print(f"Total sum of bids within {searchdistance}% of current price ({current_price}): {bidssum}")
# print(f"Total sum of asks within {searchdistance}% of current price ({current_price}): {askssum}")
# print("")
#
# bids = data['bids']
# asks = data['asks']
#
# print("Bids:")
# for bid in bids:
#     price = float(bid[0])
#     quantity = float(bid[1])
#     print(f"Price: {price}, Quantity: {quantity}")
#
# print("Asks:")
# for ask in asks:
#     price = float(ask[0])
#     quantity = float(ask[1])
#     print(f"Price: {price}, Quantity: {quantity}")

from requests import get
import pandas as pd

symbol = 'LQTYUSDT'
search_distance = 0.01 # 5%
depth_url = f'https://api.binance.com/api/v3/depth?symbol={symbol}&limit=1000'
price_url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'

# Get the current price
current_price = float(get(price_url).json()['price'])
print(f'Current price: {current_price}')

# Get the depth data
data = get(depth_url).json()
asks = data['asks']
bids = data['bids']

searchrangemax = current_price * (1 + search_distance)
searchrangemin = current_price * (1 - search_distance)


# Filter the bids and asks by price within the search distance
bids_within_search_distance = [bid for bid in bids if searchrangemax > float(bid[0]) > searchrangemin]
asks_within_search_distance = [ask for ask in asks if searchrangemax > float(ask[0]) > searchrangemin]

# print(bids_within_search_distance)
# print(asks_within_search_distance)

# Calculate the bid and ask sums within the search distance
bidssum = sum([float(bid[1]) for bid in bids_within_search_distance])
askssum = sum([float(ask[1]) for ask in asks_within_search_distance])

print(f'Bid liquidity in USD: {bidssum * current_price}')
print(f'Ask liquidity in USD: {askssum * current_price}')


# # Print the results
# print(f"Range: {current_price * (1 - search_distance) - current_price * (1 + search_distance)}")
# print(f'Bid sum within {search_distance * 100}% of current price: {int(bidssum)}')
# print(f'Ask sum within {search_distance * 100}% of current price: {int(askssum)}')
# print(f'Its sum: {int(askssum) + int(bidssum)}')

