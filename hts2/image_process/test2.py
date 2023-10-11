import os
import sys

import cv2

basepath = 'A:/Test/20231012img_check/IMAGE/00_00'

for i in range(3, 19):
    img_path1 = os.path.join(basepath, 'ImageFilterWithInterpolation_GPU_2_00000000_0_{:03}.tif'.format(i))
    img_path2 = os.path.join(basepath, '{:03}_from.png'.format(i - 3))
    img1 = cv2.imread(img_path1, 0)
    img2 = cv2.imread(img_path2, 0)
    diff = img2 - img1
    print(cv2.countNonZero(diff))

