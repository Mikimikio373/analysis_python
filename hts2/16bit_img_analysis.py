import cv2
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.stats import poisson
from scipy.special import gamma, loggamma

# img_path = '16bit_search_inv.png'
img_path = 'R:\\minami\\20230213_Reversal\\1-7\\PL006\\deadpixel_test_size15htr8.tif'
# img_path = 'R:\\minami\\20230213_Reversal\\4-6\\PL006\\deadpixel_test.tif'
img = cv2.imread(img_path, cv2.IMREAD_ANYDEPTH)


# print(img)

img_inv_ravel = np.ravel(img)

print(np.count_nonzero(np.asarray(img) > 1299))
# plt.hist(img_inv_ravel, 2970, (0, 2970), log=True)
# plt.axvline(x=1299, c='r')
# plt.savefig('R:\\minami\\20230213_Reversal\\1-7\\PL006\\deadpixel_seach.pdf')
# plt.clf()
# plt.hist(img_inv_ravel, 1970, (1000, 2970), log=True)
# plt.axvline(x=1299, c='r')
# plt.savefig('R:\\minami\\20230213_Reversal\\1-7\\PL006\\deadpixel_seach_zoom.pdf')
# plt.savefig('R:\\minami\\20230213_Reversal\\4-6\\PL006\\deadpixel_seach.png', dpi=600)

ret, img_thr = cv2.threshold(img, 1299, 255, cv2.THRESH_BINARY_INV)
img_thr = img_thr.astype(np.uint8)
print(img_thr.dtype)
cv2.imshow('window', img_thr)
cv2.waitKey(0)

cv2.imwrite('A:\\test.png', img_thr)
