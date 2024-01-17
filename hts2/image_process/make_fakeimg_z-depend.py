import os
import sys

import numpy as np
import cv2
import yaml

basepath = 'Q:/minami/20231204_fakeimg'
width = 2896
height = 1538
# width = 2048
# height = 1088
width_max = 3072
height_max = 1632
toptottom = int((height_max - height) / 2)
lefttoright = int((width_max - width) / 2)
dilate_mode = True
# p = float(136541/(width * height))
# cubic_root2_dilate = 146256 / (width * height)
# rate = 105981.5 / (width * height)
rate = ((141009 + 151997) / 2) / (width * height)
rate = rate / 2.0  # orをとるため1/2
if dilate_mode:
    rate = rate / 4.0
for p in [rate]:
    if dilate_mode:
        outpath = os.path.join(basepath, 'p-{:.5}_cubic_dilate'.format(p), 'IMAGE00_AREA-1')
    else:
        outpath = os.path.join(basepath, 'p-{:.5}'.format(p), 'IMAGE00_AREA-1')
    os.makedirs(outpath)
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
                for i in range(17):
                    rand_img = np.random.rand(height, width)
                    ret, thr_img = cv2.threshold(rand_img, p, 255, cv2.THRESH_BINARY_INV)
                    if dilate_mode:
                        thr_img = cv2.dilate(thr_img, np.ones((2, 2), np.uint8))

                    thr_img = cv2.copyMakeBorder(thr_img, toptottom, toptottom, lefttoright, lefttoright, cv2.BORDER_CONSTANT, value=0)
                    rand_img_z.append(thr_img)
                for i in range(16):
                    or_img = rand_img_z[i] + rand_img_z[i+1]
                    out_name = os.path.join(out_dir, 'L{}_VX{:04}_VY{:04}_{}.png'.format(layer, vx, vy, i))
                    cv2.imwrite(out_name, or_img)
                    list_hitpixel.append(cv2.countNonZero(or_img))

                print('{} ended'.format(out_dir))

    hitpixel_log = os.path.join(outpath, 'hitpixel_log.txt')
    with open(hitpixel_log, 'w') as f:
        f.write('average,std_dev\n{},{}'.format(np.average(list_hitpixel), np.std(list_hitpixel)))

