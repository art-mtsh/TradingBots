import requests
import math

url = "https://fapi.binance.com/fapi/v1/exchangeInfo"

response = requests.get(url)
data = response.json()

# List of pairs to exclude
exclude = [""]

perpetual_pairs = [symbol['symbol'] for symbol in data['symbols'] if symbol['contractType'] == 'PERPETUAL' and symbol['symbol'] not in exclude]

# Sort the list of perpetual futures trading pairs alphabetically by name
perpetual_pairs.sort()

# Calculate the length of each section
section_length = math.ceil(len(perpetual_pairs) / 16)

# Split the list of perpetual futures trading pairs into four sections
section_1 = perpetual_pairs[:section_length]
section_2 = perpetual_pairs[section_length:section_length*2]
section_3 = perpetual_pairs[section_length*2:section_length*3]
section_4 = perpetual_pairs[section_length*3:section_length*4]
section_5 = perpetual_pairs[section_length*4:section_length*5]
section_6 = perpetual_pairs[section_length*5:section_length*6]
section_7 = perpetual_pairs[section_length*6:section_length*7]
section_8 = perpetual_pairs[section_length*7:section_length*8]
section_9 = perpetual_pairs[section_length*8:section_length*9]
section_10 = perpetual_pairs[section_length*9:section_length*10]
section_11 = perpetual_pairs[section_length*10:section_length*11]
section_12 = perpetual_pairs[section_length*11:section_length*12]
section_13 = perpetual_pairs[section_length*12:section_length*13]
section_14 = perpetual_pairs[section_length*13:section_length*14]
section_15 = perpetual_pairs[section_length*14:section_length*15]
section_16 = perpetual_pairs[section_length*15:]
