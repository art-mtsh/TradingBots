# --- CUMULATIVE PIN BAR ---
# for i in range(3, 4):
#     mOpen = cClose[-i]
#     mHigh = max(cHigh[-2:-i:-1])
#     mLow = min(cLow[-2:-i:-1])
#     mClose = cClose[-2]
#     third = (mHigh - mLow) / 5
#     br_ratio = 0
#     if mHigh != mLow:
#         br_ratio += abs(mClose - mOpen) / ((mHigh - mLow) / 100)
# if br_ratio < 25 and \
#         ((mHigh > mClose > mHigh - third)
#         or
#         (mLow < mClose < mLow + third)):
#     pin_height += ((mHigh - mLow) / mHigh) * 100
#     pin_width += i-1
#     pinOpen += mOpen
#     pinHigh += mHigh
#     pinLow += mLow
#     pinClose += mClose
#     break