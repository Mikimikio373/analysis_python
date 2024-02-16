import os.path
import random
import sys

import json
import cv2
import numpy as np


# img_base = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png_thr_cubic/png_thr_cubic11_10_zfilt-0.40'
img_base = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png_thr_noncubic_freq0.08_z0.3/png_thr14_13'
json_base = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1'
out_base = 'Q:/minami/random_img'
out_dir_name = 'noncubic1413'
out_path = os.path.join(out_base, out_dir_name, 'IMAGE00_AREA-1', 'png')
os.makedirs(out_path, exist_ok=True)

width_max = 3072
height_max = 1632

nx = 27
ny = 55
layer = 0
npicsnap = 27

# 出力先フォルダの作成
for vy in range(ny):
    for l in range(2):
        for vx in range(nx):
            dir_name = 'L{}_VX{:04}_VY{:04}'.format(l, vx, vy)
            dir = os.path.join(out_path, dir_name)
            os.makedirs(dir, exist_ok=True)




listx = np.arange(nx).tolist()
listy = np.arange(ny).tolist()

vx_list = []
vy_list = []
for i in range(16):
    vx_list.append(random.sample(listx, len(listx)))
    vy_list.append(random.sample(listy, len(listy)))

for vy in range(ny):
    for vx in range(nx):
        view = vx + layer * nx + vy * nx * 2
        json_path = os.path.join(json_base, 'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view, layer, vx, vy, npicsnap))
        if not os.path.exists(json_path):
            sys.exit('there is no file: {}'.format(json_path))

        with open(json_path, 'rb') as f:
            j = json.load(f)

        if layer == 0:
            last = j['Last'] - 1
            first = last - 15
        else:
            first = j['First'] + 1
            last = first + 15

        picnum = 0
        for i in range(first, last + 1):
            img_path = os.path.join(img_base, 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy), 'L{}_VX{:04}_VY{:04}_{}.png'.format(layer, vx, vy, i))
            if not os.path.exists(img_path):
                sys.exit('there is no file: {}'.format(img_path))
            img = cv2.imread(img_path, 0)
            width = len(img[0])
            height = len(img)
            toptottom = int((height_max - height) / 2)
            lefttoright = int((width_max - width) / 2)
            # 3072*1632に調整
            img_out = cv2.copyMakeBorder(img, toptottom, toptottom, lefttoright, lefttoright,
                                               cv2.BORDER_CONSTANT, value=0)

            out_name0 = os.path.join(out_path,
                                    'L0_VX{:04}_VY{:04}'.format(vx_list[picnum][vx], vy_list[picnum][vy]),
                                    'L0_VX{:04}_VY{:04}_{}.png'.format(vx_list[picnum][vx], vy_list[picnum][vy],
                                                                        picnum))
            out_name1 = os.path.join(out_path,
                                     'L1_VX{:04}_VY{:04}'.format(vx_list[picnum][vx], vy_list[picnum][vy]),
                                     'L1_VX{:04}_VY{:04}_{}.png'.format(vx_list[picnum][vx], vy_list[picnum][vy],
                                                                        picnum))
            cv2.imwrite(out_name0, img_out)
            cv2.imwrite(out_name1, img_out)
            picnum += 1

        print('{} ended'.format(os.path.join(img_base, 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy))))


