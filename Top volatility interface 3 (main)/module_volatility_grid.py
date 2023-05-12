

def volatility_grid_function(cHigh, cLow, cClose):

	volatility_60m10 = ((max(cHigh[-541:-601:-1]) - min(cLow[-541:-601:-1])) / (cClose[-1] / 100))
	volatility_60m9 = ((max(cHigh[-481:-541:-1]) - min(cLow[-481:-541:-1])) / (cClose[-1] / 100))
	volatility_60m8 = ((max(cHigh[-421:-481:-1]) - min(cLow[-421:-481:-1])) / (cClose[-1] / 100))
	volatility_60m7 = ((max(cHigh[-361:-421:-1]) - min(cLow[-361:-421:-1])) / (cClose[-1] / 100))
	volatility_60m6 = ((max(cHigh[-301:-361:-1]) - min(cLow[-301:-361:-1])) / (cClose[-1] / 100))
	volatility_60m5 = ((max(cHigh[-241:-301:-1]) - min(cLow[-241:-301:-1])) / (cClose[-1] / 100))
	volatility_60m4 = ((max(cHigh[-181:-241:-1]) - min(cLow[-181:-241:-1])) / (cClose[-1] / 100))
	volatility_60m3 = ((max(cHigh[-121:-181:-1]) - min(cLow[-121:-181:-1])) / (cClose[-1] / 100))
	volatility_60m2 = ((max(cHigh[-61:-121:-1]) - min(cLow[-61:-121:-1])) / (cClose[-1] / 100))
	volatility_60m1 = ((max(cHigh[-1:-61:-1]) - min(cLow[-1:-61:-1])) / (cClose[-1] / 100))

	volatility_60m10 = float('{:.2f}'.format(volatility_60m10))
	volatility_60m9 = float('{:.2f}'.format(volatility_60m9))
	volatility_60m8 = float('{:.2f}'.format(volatility_60m8))
	volatility_60m7 = float('{:.2f}'.format(volatility_60m7))
	volatility_60m6 = float('{:.2f}'.format(volatility_60m6))
	volatility_60m5 = float('{:.2f}'.format(volatility_60m5))
	volatility_60m4 = float('{:.2f}'.format(volatility_60m4))
	volatility_60m3 = float('{:.2f}'.format(volatility_60m3))
	volatility_60m2 = float('{:.2f}'.format(volatility_60m2))
	volatility_60m1 = float('{:.2f}'.format(volatility_60m1))

	return [volatility_60m10, volatility_60m9, volatility_60m8, volatility_60m7, volatility_60m6, volatility_60m5, volatility_60m4, volatility_60m3, volatility_60m2, volatility_60m1]
