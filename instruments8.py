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
section_length = math.ceil(len(perpetual_pairs) / 8)

# Split the list of perpetual futures trading pairs into eight sections
section_1 = perpetual_pairs[:section_length]
section_2 = perpetual_pairs[section_length:section_length*2]
section_3 = perpetual_pairs[section_length*2:section_length*3]
section_4 = perpetual_pairs[section_length*3:section_length*4]
section_5 = perpetual_pairs[section_length*4:section_length*5]
section_6 = perpetual_pairs[section_length*5:section_length*6]
section_7 = perpetual_pairs[section_length*6:section_length*7]
section_8 = perpetual_pairs[section_length*7:]

# Remaining pairs, if any, can be assigned to section_8 or section_1, based on your preference
# section_8.extend(perpetual_pairs[section_length*8:])

# Print or use the sections as needed
# print("Section 1:", section_1)
# print("Section 2:", section_2)
# print("Section 3:", section_3)
# print("Section 4:", section_4)
# print("Section 5:", section_5)
# print("Section 6:", section_6)
# print("Section 7:", section_7)
# print("Section 8:", section_8)
#
