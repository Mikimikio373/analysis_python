import os.path

import cv2
import numpy as np
import json

i = 0
img_list = []
nog = []
z_relate = []
for i in range(16):
    path = 'Q:/minami/20231204_fakeimg/noncubic1615/IMAGE00_AREA-1/png/L0_VX0000_VY0000/L0_VX0000_VY0000_{}.png'.format(i)

    img = cv2.imread(path, 0)
    img_list.append(img)
    print(cv2.countNonZero(img))
    nog.append(cv2.countNonZero(img))

for i in range(15):
    img_and = cv2.bitwise_and(img_list[i], img_list[i+1])
    relate = cv2.countNonZero(img_and) / nog[i]
    z_relate.append(relate)

print(np.average(nog), np.std(nog))
print(np.average(z_relate), np.std(z_relate))
