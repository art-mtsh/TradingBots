import requests
import math

url = "https://fapi.binance.com/fapi/v1/exchangeInfo"

response = requests.get(url)
data = response.json()

# List of pairs to exclude
# exclude = ['BTCUSDT', 'ETHUSDT', 'BNXUSDT', 'SSVUSDT', 'CKBUSDT']
exclude = []

perpetual_pairs = [symbol['symbol'] for symbol in data['symbols'] if symbol['contractType'] == 'PERPETUAL' and symbol['symbol'] not in exclude]

# Sort the list of perpetual futures trading pairs alphabetically by name
perpetual_pairs.sort()

# Calculate the length of each section
section_length = math.ceil(len(perpetual_pairs) / 4)

# Split the list of perpetual futures trading pairs into four sections
section_1 = perpetual_pairs[:section_length]
section_2 = perpetual_pairs[section_length:section_length*2]
section_3 = perpetual_pairs[section_length*2:section_length*3]
section_4 = perpetual_pairs[section_length*3:]
