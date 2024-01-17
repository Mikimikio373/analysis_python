import os.path
import sys

import yaml
import cv2
import pandas as pd


if not len(sys.argv) == 4:
    sys.exit('command line error. please input [basepath], [AreaScanParam_path], [picnum]')

basepath = sys.argv[1]
yaml_path = sys.argv[2]
picnum = int(sys.argv[3])

with open(yaml_path, 'rb') as f:
    param = yaml.safe_load(f)

nx = param['Area'][0]['NViewX']
ny = param['Area'][0]['NViewY']
l = param['Area'][0]['NLayer']

nog_list = [[], []]
obj_num = [[], []]
for layer in range(l):
    for vy in range(ny):
        for vx in range(nx):
            fname = 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy)
            png_path = os.path.join(basepath, fname, fname + '_{}.png'.format(picnum))

            if not os.path.exists(png_path):
                sys.exit('There is no file: {}'.format(png_path))

            img = cv2.imread(png_path, 0)
            nog = cv2.countNonZero(img)
            nog_list[layer].append(nog)
            ret, thr = cv2.threshold(img, 2, 255, cv2.THRESH_BINARY)
            retval, labels = cv2.connectedComponents(thr)
            obj_num[layer].append(retval - 1)
        print('vy: {} / {} ended'.format(vy, ny))

out_df = pd.DataFrame()
out_df['L0'] = nog_list[0]
out_df['L1'] = nog_list[1]
out_df['obj_L0'] = obj_num[0]
out_df['obj_L1'] = obj_num[1]
out_path = os.path.join(basepath, 'nog_list.csv')
out_df.to_csv(out_path, index=False)

