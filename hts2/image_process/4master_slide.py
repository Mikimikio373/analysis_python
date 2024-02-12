import copy
import os.path

import cv2

img_path1 = 'Q:/minami/randfake_img/noncubic1413/IMAGE00_AREA-1/png/L0_VX0003_VY0034/L0_VX0003_VY0034_2.png'
img_path2 = 'Q:/minami/randfake_img/noncubic1413/IMAGE00_AREA-1/png/L0_VX0003_VY0034/L0_VX0003_VY0034_3.png'
out_path = 'B:/data/powerpoint/master_presen/fig/fake_img_roi'
os.makedirs(out_path, exist_ok=True)
img = cv2.imread(img_path1, 0)
img_roi = copy.deepcopy(img[1000:1100, 1400:1500])
# cv2.imshow('test', img_roi)
# cv2.waitKey(0)
cv2.imwrite(os.path.join(out_path, '1.png'), cv2.resize(img_roi, None, fx=6, fy=6, interpolation=cv2.INTER_NEAREST))

img2 = cv2.imread(img_path2, 0)
img_roi2 = copy.deepcopy(img2[1000:1100, 1400:1500])
cv2.imwrite(os.path.join(out_path, '2.png'), cv2.resize(img_roi2, None, fx=6, fy=6, interpolation=cv2.INTER_NEAREST))

img_and = cv2.bitwise_and(img_roi, img_roi2)
img_color = cv2.cvtColor(img_roi, cv2.COLOR_GRAY2BGR)
img_color2 = cv2.cvtColor(img_roi2, cv2.COLOR_GRAY2BGR)
for y in range(len(img_color)):
    for x in range(len(img_color[0])):
        if not img_and[y][x] == 0:
            img_color[y][x] = [124, 252, 0]
            img_color2[y][x] = [124, 252, 0]

cv2.imwrite(os.path.join(out_path, '1color.png'), cv2.resize(img_color, None, fx=6, fy=6, interpolation=cv2.INTER_NEAREST))
cv2.imwrite(os.path.join(out_path, '2color.png'), cv2.resize(img_color2, None, fx=6, fy=6, interpolation=cv2.INTER_NEAREST))