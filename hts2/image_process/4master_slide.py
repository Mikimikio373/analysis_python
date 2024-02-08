import copy
import os.path

import cv2

img_path = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png/L0_VX0001_VY0009/L0_VX0001_VY0009_13.png'
out_path = 'B:/data/powerpoint/master_presen/fig/roi'
img = cv2.imread(img_path, 0)
img_roi = copy.deepcopy(img[400:500, 400:500])
img_roi = cv2.resize(img_roi, None, fx=6, fy=6, interpolation=cv2.INTER_NEAREST)
cv2.imwrite(os.path.join(out_path, '1.png'), img_roi)

img_roi = copy.deepcopy(img[400:500, 440:540])
img_roi = cv2.resize(img_roi, None, fx=6, fy=6, interpolation=cv2.INTER_NEAREST)
cv2.imwrite(os.path.join(out_path, '2.png'), img_roi)
