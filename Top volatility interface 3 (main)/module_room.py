def room_function(cHigh, cLow, cClose):

	high_room_counter = 0
	low_room_counter = 0

	for i in range(2, 241):
		if cHigh[-1] >= cHigh[-i]:
			high_room_counter += 1
		else:
			break

	for i in range(2, 241):
		if cLow[-1] <= cLow[-i]:
			low_room_counter += 1
		else:
			break

	# --- 120 ---

	max_of_range120 = max(cHigh[-1:-121:-1])
	min_of_range120 = min(cLow[-1:-121:-1])

	dist_max120 = abs(max_of_range120 - cClose[-1])
	dist_min120 = abs(min_of_range120 - cClose[-1])

	distance120 = min(dist_max120, dist_min120) / (cClose[-1] / 100)
	distance120 = float('{:.2f}'.format(distance120))

	# --- 240 ---

	max_of_range240 = max(cHigh[-1:-241:-1])
	min_of_range240 = min(cLow[-1:-241:-1])

	dist_max240 = abs(max_of_range240 - cClose[-1])
	dist_min240 = abs(min_of_range240 - cClose[-1])

	distance240 = min(dist_max240, dist_min240) / (cClose[-1] / 100)
	distance240 = float('{:.2f}'.format(distance240))

	# --- 480 ---

	max_of_range480 = max(cHigh[-1:-481:-1])
	min_of_range480 = min(cLow[-1:-481:-1])

	dist_max480 = abs(max_of_range480 - cClose[-1])
	dist_min480 = abs(min_of_range480 - cClose[-1])

	distance480 = min(dist_max480, dist_min480) / (cClose[-1] / 100)
	distance480 = float('{:.2f}'.format(distance480))

	# --- 240 ---

	max_of_range720 = max(cHigh[-1:-721:-1])
	min_of_range720 = min(cLow[-1:-721:-1])

	dist_max720 = abs(max_of_range720 - cClose[-1])
	dist_min720 = abs(min_of_range720 - cClose[-1])

	distance720 = min(dist_max720, dist_min720) / (cClose[-1] / 100)
	distance720 = float('{:.2f}'.format(distance720))

	return [max(high_room_counter, low_room_counter), distance120, distance240, distance480, distance720]

