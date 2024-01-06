import os
import sys

import numpy as np
import cv2
import matplotlib.pyplot as plt

# basepath = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-0.06/png/L0_VX0000_VY0000'
# basepath = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_nogdilate/png_thr10_9/L0_VX0000_VY0000'
basepath = 'Q:/minami/20220429_suganami/006/IMAGE00_AREA-1/png_thr_nolilate/png_thr10_9/L0_VX0000_VY0000'

# for i in range(0, 1):
img_path = os.path.join(basepath, 'L0_VX0000_VY0000_{}.png'.format(11))
img = cv2.imread(img_path, 0)
ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
retval, labels, stats, centor_ids = cv2.connectedComponentsWithStats(img)
print(retval, np.count_nonzero(img))
print(np.count_nonzero(img) / (2048 * 1088))

stats = np.asarray(np.delete(stats, 0, axis=0))
area = []
for stat in stats:
    area.append(stat[4])

plt.hist(area, bins=100, range=(0.5, 100.5), log=True)
plt.show()

# test = np.random.rand(9, 9)
# ret, test = cv2.threshold(test, 0.05, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow('test', test)
# cv2.waitKey(0)
#
# test = cv2.dilate(test, np.ones((2, 2), np.uint8))
# cv2.imshow('test', test)
# cv2.waitKey(0)
