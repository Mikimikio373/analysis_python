import os.path
import sys

import yaml
import cv2
import pandas as pd
import numpy as np
import itertools

if not len(sys.argv) == 3:
    sys.exit('command line error. please input [basepath], [AreaScanParam_path]')

basepath = sys.argv[1]
yaml_path = sys.argv[2]

with open(yaml_path, 'rb') as f:
    param = yaml.safe_load(f)

nx = param['Area'][0]['NViewX']
ny = param['Area'][0]['NViewY']
l = param['Area'][0]['NLayer']

area = [[], []]
for layer in range(l):
    for vy in range(ny):
        for vx in range(nx):
            fname = 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy)
            png_path = os.path.join(basepath, fname, fname + '_11.png')

            if not os.path.exists(png_path):
                sys.exit('There is no file: {}'.format(png_path))

            img = cv2.imread(png_path, 0)
            ret, thr = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)
            retval, labels, stats, center_ids = cv2.connectedComponentsWithStats(thr)
            stats_del = np.asarray(np.delete(stats, 0, axis=0))
            tmp = [a[4] for a in stats_del]
            area[layer].append(tmp)
        print('vy: {} / {} ended'.format(vy, ny))

flatten0 = list(itertools.chain.from_iterable(area[0]))
flatten1 = list(itertools.chain.from_iterable(area[1]))
out_df0 = pd.DataFrame()
out_df1 = pd.DataFrame()
out_df0['L0'] = flatten0
out_df1['L1'] = flatten1
out_path0 = os.path.join(basepath, 'area_list_l0.csv')
out_path1 = os.path.join(basepath, 'area_list_l1.csv')
out_df0.to_csv(out_path0, index=False)
out_df1.to_csv(out_path1, index=False)

