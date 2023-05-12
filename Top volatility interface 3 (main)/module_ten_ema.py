import talib


def ten_ema_function(cClose, emabasis: int, emadelta: float):

	ma1 = talib.EMA(cClose, emabasis)[-1]
	ma2 = talib.EMA(cClose, int(emabasis * emadelta))[-1]
	ma3 = talib.EMA(cClose, int(emabasis * emadelta * emadelta))[-1]
	ma4 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta))[-1]
	ma5 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta))[-1]
	ma6 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
	ma7 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
	ma8 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
	ma9 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]
	ma10 = talib.EMA(cClose, int(emabasis * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta * emadelta))[-1]

	tenema = ""

	if ma1 >= ma2 >= ma3 >= ma4 >= ma5 >= ma6 >= ma7 >= ma8 >= ma9 >= ma10:
		tenema += "Up"
	elif ma1 <= ma2 <= ma3 <= ma4 <= ma5 <= ma6 <= ma7 <= ma8 <= ma9 <= ma10:
		tenema += "Down"

	return [tenema]
