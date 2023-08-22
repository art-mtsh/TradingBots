import talipp.indicators.EMA as ema

def sonic_signal(cOpen, cHigh, cLow, cClose):
	ema34_basis = ema(period=34, input_values=cClose)
	ema34_low = ema(period=34, input_values=cLow)
	ema34_high = ema(period=34, input_values=cHigh)
	ema89 = ema(period=89, input_values=cClose)
	
	rising_dragon = ema34_low[-1] > ema89[-1]
	falling_dragon = ema34_high[-1] < ema89[-1]
	
	dragon_distance_k: float
	if ema34_high[-1] != ema34_low[-1]:
		dragon_distance_k = abs(ema34_basis[-1] - ema89[-1]) / (ema34_high[-1] - ema34_low[-1])
	else:
		dragon_distance_k = 0
	
	# room = 10
	
	# upper_room = cHigh[-1] >= max(cHigh[-1:-room:-1])
	# lower_room = cLow[-1] <= min(cLow[-1:-room:-1])
	
	# three_rising_candles = cClose[-1] > cOpen[-1] and cClose[-2] > cOpen[-2] and cClose[-3] > cOpen[-3]
	# three_falling_candles = cClose[-1] < cOpen[-1] and cClose[-2] < cOpen[-2] and cClose[-3] < cOpen[-3]
	
	# if dragon_distance_k > 1:
	# 	if rising_dragon and cOpen[-1] > cClose[-1] and ema34_high[-1] >= cLow[-1] >= ema89[-1]:
	# 		if three_falling_candles:
	# 			return ["Sonic STRONG"]
	# 		else:
	# 			return ["Sonic"]
	# 	elif falling_dragon and cOpen[-1] < cClose[-1] and ema34_low[-1] <= cHigh[-1] <= ema89[-1]:
	# 		if three_rising_candles:
	# 			return ["Sonic STRONG"]
	# 		else:
	# 			return ["Sonic"]
	# 	else:
	# 		return ["Sleep"]
	# else:
	# 	return ["Sleep"]
	
	cloud_above = 0
	cloud_below = 0
	
	for i in range(2, 12):
		if cLow[-i] < ema34_high[-i]:
			cloud_above += 1
			
	for i in range(2, 12):
		if cHigh[-i] > ema34_low[-i]:
			cloud_below += 1
	
	if dragon_distance_k > 1:
		if rising_dragon and cloud_above == 0 and ema34_high[-1] >= cLow[-1] >= ema89[-1]:
			return [f'Sonic RISE, Cloud above is {cloud_above}']
		elif falling_dragon and cloud_below == 0 and ema34_low[-1] <= cHigh[-1] <= ema89[-1]:
			return [f'Sonic FALL, Cloud below is {cloud_below}']
		else:
			return ['Sleep']
	else:
		return ['Sleep']

		