import os
import random
import sys

import numpy as np
import yaml
import cv2

ori_path = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1'
ori_ymlpath = os.path.join(ori_path, '../AreaScan4Param.yml')

# out_path = 'Q:/minami/20231205_rand_grain2023/img/png'
out_path = 'Q:/minami/20231205_rand_grain2023/graine2023_thr10-9_cubic/png'

with open(ori_ymlpath, 'rb') as f:
    ori_yml = yaml.safe_load(f)

nx = ori_yml['Area'][0]['NViewX']
ny = ori_yml['Area'][0]['NViewY']

img_list = []
for layer in range(2):
    for vx in range(nx):
        for vy in range(ny):
            fname = 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy)
            # img_path = os.path.join(ori_path, 'png_thr_dilate', 'png_thr10_9', fname, fname + '_11.png')
            img_path = os.path.join(ori_path, 'png_thr_dilate', 'png_thr_cubic10_9_zfilt-0.15', fname, fname + '_11.png')
            if not os.path.exists(img_path):
                print('there is no file: {}'.format(img_path))
                continue
            img = cv2.imread(img_path, 0)
            img_list.append(img)
            print('read, L{}, vx{}, vy{} ended'.format(layer, vx, vy))

print(len(img_list))
num = len(img_list)
print(np.count_nonzero(img_list[0]))


for layer in range(2):
    for vx in range(nx):
        for vy in range(ny):
            fname = 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy)
            fpath = os.path.join(out_path, fname)
            os.makedirs(fpath)
            for i in range(16):
                rand = random.randrange(num)
                img = img_list[rand]
                img_path = os.path.join(fpath, 'L{}_VX{:04}_VY{:04}_{}.png'.format(layer, vx, vy, i))
                cv2.imwrite(img_path, img)

            print('write, L{}, vx{}, vy{} ended'.format(layer, vx, vy))
