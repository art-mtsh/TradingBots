import datetime
import pandas
import telebot
import matplotlib.pyplot as plt
from requests import get
from os import remove

# --- TELEGRAM ---

TOKEN1 = '5657267406:AAExhEvjG3tjb0KL6mTM9otoFiL6YJ_1aSA'
bot1 = telebot.TeleBot(TOKEN1)

# --- PENDING SEARCH ---

def screenshoter_DIV_d(timeinterval:str, symbol:str, direction:str, atr1: float, atr2: float, atr3: float):

	# --- DATA CANDLES ---

	url_klines = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + timeinterval + '&limit=101'
	url_bs = 'https://fapi.binance.com/futures/data/takerlongshortRatio?symbol=' + symbol + '&period=' + timeinterval + '&limit=100'
	data1 = get(url_klines).json()
	data2 = get(url_bs).json()

	# --- K-LINE ---

	D1 = pandas.DataFrame(data1)
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
	df1['open_time'] = df1['open_time'].apply(
		lambda d: datetime.datetime.fromtimestamp(int(d) / 1000).strftime('%H:%M:%S'))

	cClose = df1['cClose'].to_numpy()

	# --- BUY SELL RATIO ---

	D2 = pandas.DataFrame(data2)
	df2 = D2
	df2['buySellRatio'] = df2['buySellRatio'].astype(float)
	df2['buyVol'] = df2['buyVol'].astype(float)
	df2['sellVol'] = df2['sellVol'].astype(float)
	df2['timestamp'] = df2['timestamp'].apply(lambda d: datetime.datetime.fromtimestamp(int(d) / 1000).strftime('%H:%M:%S'))

	cBuyVol = df2['buyVol'].to_numpy()
	cSellVol = df2['sellVol'].to_numpy()

	# --- PLOTS ---
	fig, af = plt.subplots(2, sharex='col', sharey='row')
	plt.suptitle(symbol + direction + ' at ' + datetime.datetime.now().strftime('%H:%M:%S') + f" ({timeinterval})")

	stock_prices = df1
	up = stock_prices[stock_prices.cClose >= stock_prices.cOpen]
	down = stock_prices[stock_prices.cClose < stock_prices.cOpen]

	# Up candles
	af[0].bar(x=up.index, height=up.cClose - up.cOpen, width = 0.9, bottom=up.cOpen, color='green')
	af[0].bar(x=up.index, height=up.cHigh - up.cClose, width = 0.05, bottom=up.cClose, color='green')
	af[0].bar(x=up.index, height=up.cLow - up.cOpen, width = 0.05, bottom=up.cOpen, color='green')
	# Down candles
	af[0].bar(x=down.index, height=down.cClose - down.cOpen, width = 0.9, bottom=down.cOpen, color='red')
	af[0].bar(x=down.index, height=down.cHigh - down.cOpen, width = 0.05, bottom=down.cOpen, color='red')
	af[0].bar(x=down.index, height=down.cLow - down.cClose, width = 0.05, bottom=down.cClose, color='red')
	# ATRs
	ly1 = [cClose[-1] - atr1, cClose[-1] - atr1]
	ly2 = [cClose[-1] - atr2, cClose[-1] - atr2]
	ly3 = [cClose[-1] - atr3, cClose[-1] - atr3]
	ly4 = [cClose[-1] + atr1, cClose[-1] + atr1]
	ly5 = [cClose[-1] + atr2, cClose[-1] + atr2]
	ly6 = [cClose[-1] + atr3, cClose[-1] + atr3]
	lx = [101, 110]
	af[0].plot(lx, ly1, color='green', linewidth=0.6)
	af[0].plot(lx, ly2, color='green', linewidth=0.6)
	af[0].plot(lx, ly3, color='green', linewidth=0.6)
	af[0].plot(lx, ly4, color='red', linewidth=0.6)
	af[0].plot(lx, ly5, color='red', linewidth=0.6)
	af[0].plot(lx, ly6, color='red', linewidth=0.6)

	# grid
	af[0].grid(color='grey', linestyle='-', linewidth=0.1)

	# --- Cumulative delta percent ---

	delta_p = list((lambda a, b, c: (a - b) / (c / 100))(cBuyVol, cSellVol, cBuyVol + cSellVol))
	cd_p = [0]


	for i in range(0, len(cSellVol)):
		one_perc_volume = (cBuyVol[i] + cSellVol[i]) / 100
		delta_per = cBuyVol[i] - cSellVol[i]
		delta_percent = delta_per / one_perc_volume
		cd_p.append(int(cd_p[-1] + delta_percent))
		# print(delta_percent)
	cd_p = cd_p[:100]

	updelta_p = []
	dndelta_p = []

	for i in range(0, len(delta_p)):
		if delta_p[i] > 0:
			updelta_p.append(delta_p[i])
			dndelta_p.append(0)
		else:
			updelta_p.append(0)
			dndelta_p.append(delta_p[i])

	af[1].bar(x=range(0, len(cd_p)), height=updelta_p, width=0.9, align='center', bottom=cd_p, color='green')
	af[1].bar(x=range(0, len(cd_p)), height=dndelta_p, width=0.9, align='center', bottom=cd_p, color='red')
	# grid
	af[1].grid(color='grey', linestyle='-', linewidth=0.1)

	# plt.show()

	# SAVE AND SEND
	plt.savefig(f'DIV{symbol}{timeinterval}.png', dpi=400, bbox_inches='tight', pad_inches=0.2)
	pic = open(f'DIV{symbol}{timeinterval}.png', 'rb')
	bot1.send_photo(662482931, pic)

	# CLEANING
	pic.close()
	remove(f'DIV{symbol}{timeinterval}.png')
	plt.cla()
	plt.clf()


# screenshoter_DIV_d(timeinterval='15m', symbol='AAVEUSDT', direction='bullish', atr1=0.36, atr2=0, atr3=0)