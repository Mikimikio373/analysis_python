import os
import sys

import numpy as np
import cv2
import yaml

width = 2048
height = 1088
dilate_mode = True
# p = float(136541/(width * height))
for p in [0.01]:
    if dilate_mode:
        basepath = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-{}_dilate'.format(p)
    else:
        basepath = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-{}'.format(p)
    os.makedirs(basepath)
    param_path = os.path.join(basepath, '../AreaScan4Param.yml')

    with open(param_path, 'rb') as f:
        param = yaml.safe_load(f)
    nx = param['Area'][0]['NViewX']
    ny = param['Area'][0]['NViewY']

    for vy in range(ny):
        for layer in range(2):
            for vx in range(nx):
                out_dir = os.path.join(basepath, 'png', 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy))
                os.makedirs(out_dir, exist_ok=True)
                for i in range(16):
                    rand_img = np.random.rand(height, width)
                    ret, thr_img = cv2.threshold(rand_img, p, 255, cv2.THRESH_BINARY_INV)
                    if dilate_mode:
                        thr_img = cv2.dilate(thr_img, np.ones((2, 2), np.uint8))

                    out_name = os.path.join(out_dir, 'L{}_VX{:04}_VY{:04}_{}.png'.format(layer, vx, vy, i))
                    cv2.imwrite(out_name, thr_img)

                print('{} ended'.format(out_dir))

