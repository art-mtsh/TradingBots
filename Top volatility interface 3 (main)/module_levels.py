
def levels_func(symbol, cHigh, cLow, cClose):

	try:

		distancetores = 0.0
		respoint = 0.0
		rescoordinate = 0

		for point in range(-60, -890, -1):
			if max(cHigh[point:point - 30:-1]) == cHigh[point]:
				unclean = 0
				doubletouchup = 0
				for b in range(-1, point, -1):
					if cHigh[b] > cHigh[point] + cHigh[point] * 0.001:
						unclean += 1
				for b in range(-1, point + 30, -1):
					if cHigh[point] + cHigh[point] * 0.001 >= cHigh[b] >= cHigh[point] - cHigh[point] * 0.001:
						doubletouchup += 1

				if unclean == 0 and doubletouchup > 1:
					distancetores += abs(cHigh[point] - cClose[-1]) / (cClose[-1] / 100)
					respoint += cHigh[point]
					rescoordinate += point
					# print(f'at {symbol} level {cHigh[point]} on {point} and {b}')
					break

		distancetosup = 0.0
		suppoint = 0.0
		supcoordinate = 0

		for point in range(-60, -890, -1):

			if min(cLow[point:point - 30:-1]) == cLow[point]:
				unclean = 0
				doubletouchdn = 0
				for b in range(-1, point, -1):
					if cLow[b] < cLow[point] - cLow[point] * 0.001:
						unclean += 1
				for b in range(-1, point + 30, -1):
					if cLow[point] - cLow[point] * 0.001 <= cLow[b] <= cLow[point] + cLow[point] * 0.001:
						doubletouchdn += 1

				if unclean == 0 and doubletouchdn > 1:
					distancetosup += abs(cClose[-1] - cLow[point]) / (cClose[-1] / 100)
					suppoint += cLow[point]
					supcoordinate += point
					# print(f'at {symbol} level {cLow[point]} on {point} and {b}')
					break

		distancetores = float('{:.2f}'.format(distancetores))
		distancetosup = float('{:.2f}'.format(distancetosup))

		if abs(respoint - cClose[-1]) < abs(suppoint - cClose[-1]):
			return [float(respoint), distancetores]
		elif abs(respoint - cClose[-1]) > abs(suppoint - cClose[-1]):
			return [float(suppoint), distancetosup]
		else:
			return [0, 0]

	except:
		print(f'Error levels for {symbol}')