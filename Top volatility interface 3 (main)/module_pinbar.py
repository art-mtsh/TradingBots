# # price <= filter
# price_filter = 100000
#
# # volume >= filter
# volume_filter = 10
#
# # atr10 >= filter
# atr10_perc_filter = 0.0
#
# # pin range >= filter
# pin_range_filter = 0.4
#
# # body/range ratio <= filter
# br_ratio_filter = 10
#
# # close inside bar range / filter
# bar_part_filter = 3
#
# # tick size <= filter
# tick_size_filter = 0.03


# try:
#     for i in range(3, 604):
#         if cHigh[-i] != cLow[-i]:
#             atr = (sum(sum([cHigh[-i:-i-10:-1] - cLow[-i:-i-10:-1]])) / len(cClose[-i:-i-10:-1]))
#             atr_per = atr / (cClose[-i] / 100)
#             atr_per = float('{:.2f}'.format(atr_per))
#
#             candle_range = cHigh[-i] - cLow[-i]
#             candle_spread = abs(cOpen[-i] - cClose[-i])
#             br_ratio = candle_spread / (candle_range / 100)
#             range_part = candle_range / bar_part_filter
#             candle_range_perc = (candle_range / cHigh[-i]) * 100
#             candle_range_perc = float('{:.2f}'.format(candle_range_perc))
#
#             if cClose[-i] <= price_filter:
#                 if ((sum(cVolume[-i:-i-10:-1]) / len(cVolume[-i:-i-10:-1])) * cClose[-i]) / 1000 >= volume_filter:
#                     if cVolume[-i] >= cVolume[-i-1]:
#                         if atr_per >= atr10_perc_filter:
#                             if candle_range_perc >= pin_range_filter:
#                                 if br_ratio <= br_ratio_filter:
#                                     if (cHigh[-i] >= cClose[-i] >= (cHigh[-i] - range_part)) or (cLow[-i] <= cClose[-i] <= (cLow[-i] + range_part)):
#                                         founded_pins += 1
#
# except:
#     print(f'Pin calculation error for: {symbol}[-1]')