import os
import sys
from math import sqrt

import numpy as np
import cv2
import yaml

basepath = 'Q:/minami/20231204_fakeimg'
# width = 2896
# height = 1538
width = 2048
height = 1088
width_max = 3072
height_max = 1632
toptottom = int((height_max - height) / 2)
lefttoright = int((width_max - width) / 2)

rate_t = 75246.4 / (width * height) * 1.02
rate_z = 0.3215 * 0.937
# rate_t = 161259 / (width * height) * 1.017
# rate_z = 0.3459
print(rate_z, rate_t)

hitrate_a = rate_t * rate_z / 9
hitrate_b = rate_t / 9 * (1 - 2 * rate_z)
print(hitrate_a, hitrate_b)
# outname = 'cubic98'
outname = 'noncubic1615'

# outpath = os.path.join(basepath, 'p-{:.3}-z{:.3}_cubic_dilate'.format(rate_t, rate_z), 'IMAGE00_AREA-1')
outpath = os.path.join(basepath, outname, 'IMAGE00_AREA-1')
print(outpath)
os.makedirs(outpath, exist_ok=True)
param_path = os.path.join(basepath, 'AreaScan4Param.yml')

with open(param_path, 'rb') as f:
    param = yaml.safe_load(f)
nx = param['Area'][0]['NViewX']
ny = param['Area'][0]['NViewY']
list_hitpixel = []
for vy in range(ny):
    for layer in range(2):
        for vx in range(nx):
            out_dir = os.path.join(outpath, 'png', 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy))
            os.makedirs(out_dir, exist_ok=True)
            rand_img_z = []
            # z方向に50%の依存性を持たせる
            for i in range(17):
                rand_img = np.random.rand(height, width)
                ret, thr_img = cv2.threshold(rand_img, hitrate_a, 255, cv2.THRESH_BINARY_INV)

                rand_img_z.append(thr_img)
            for i in range(16):
                or_img = rand_img_z[i] + rand_img_z[i+1]
                # hitrate bのランダム画像を作って足す
                rand_img_b = np.random.rand(height, width)
                ret, thr_img_b = cv2.threshold(rand_img_b, hitrate_b, 255, cv2.THRESH_BINARY_INV)
                # z依存性とランダムを足して、z依存性を調整
                add_img = or_img + thr_img_b
                # 膨張処理
                # add_img = cv2.dilate(add_img, np.ones((2, 2), np.uint8))
                add_img = cv2.dilate(add_img, np.ones((3, 3), np.uint8))
                # 3072*1632に調整
                add_img_cubic = cv2.copyMakeBorder(add_img, toptottom, toptottom, lefttoright, lefttoright, cv2.BORDER_CONSTANT, value=0)
                out_name = os.path.join(out_dir, 'L{}_VX{:04}_VY{:04}_{}.png'.format(layer, vx, vy, i))
                cv2.imwrite(out_name, add_img_cubic)
                list_hitpixel.append(cv2.countNonZero(add_img_cubic))

            print('{} ended'.format(out_dir))

hitpixel_log = os.path.join(outpath, 'hitpixel_log.txt')
with open(hitpixel_log, 'w') as f:
    f.write('average,std_dev\n{},{}'.format(np.average(list_hitpixel), np.std(list_hitpixel)))

