import cv2
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.stats import poisson
from scipy.special import gamma, loggamma

# img_path = '16bit_search_inv.png'
img_path = 'R:\\minami\\20230213_Reversal\\1-7\\PL006\\deadpixel_test_size15htr14.tif'
# img_path = 'R:\\minami\\20230213_Reversal\\4-6\\PL006\\deadpixel_test.tif'
img = cv2.imread(img_path, cv2.IMREAD_ANYDEPTH)


print(img)

img_inv_ravel = np.ravel(img)

print(np.count_nonzero(np.asarray(img) > 1299))
plt.hist(img_inv_ravel, 2970, (0, 2970), log=True)
plt.axvline(x=1299, c='r')
plt.savefig('R:\\minami\\20230213_Reversal\\1-7\\PL006\\deadpixel_seach.pdf')
plt.clf()
plt.hist(img_inv_ravel, 1970, (1000, 2970), log=True)
plt.axvline(x=1299, c='r')
plt.savefig('R:\\minami\\20230213_Reversal\\1-7\\PL006\\deadpixel_seach_zoom.pdf')
# plt.savefig('R:\\minami\\20230213_Reversal\\4-6\\PL006\\deadpixel_seach.png', dpi=600)