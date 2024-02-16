import json
import os.path
import sys

import yaml
import cv2
import pandas as pd


if not len(sys.argv) == 6:
    sys.exit('command line error. please input [basepath], [jsonpath], [AreaScanParam_path], [npicturenum], [fakeflag]')

basepath = sys.argv[1]
json_path = sys.argv[2]
yaml_path = sys.argv[3]
npic = int(sys.argv[4])
fakeflag = int(sys.argv[5])

with open(yaml_path, 'rb') as f:
    param = yaml.safe_load(f)

nx = param['Area'][0]['NViewX']
ny = param['Area'][0]['NViewY']
l = param['Area'][0]['NLayer']

nog_list = [[], []]
obj_num = [[], []]
view = 0
for vy in range(ny):
    for layer in range(l):
        for vx in range(nx):
            fname = 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy)
            if not fakeflag == 1:
                with open(os.path.join(json_path, 'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view, layer, vx, vy, npic)), 'rb') as f:
                    j = json.load(f)
                if layer == 1: # stage側
                    first = j['First'] - 1
                    last = first + 15
                else: # lens側
                    last = j['Last'] - 1
                    first = last - 15
            else:
                first = 0
                last = 15
            for picnum in range(first, last + 1):
                png_path = os.path.join(basepath, fname, fname + '_{}.png'.format(picnum))

                if not os.path.exists(png_path):
                    sys.exit('There is no file: {}'.format(png_path))

                img = cv2.imread(png_path, 0)
                nog = cv2.countNonZero(img)
                nog_list[layer].append(nog)
                ret, thr = cv2.threshold(img, 2, 255, cv2.THRESH_BINARY)
                retval, labels = cv2.connectedComponents(thr)
                obj_num[layer].append(retval - 1)

            view += 1
    print('vy: {} / {} ended'.format(vy, ny))

out_df = pd.DataFrame()
out_df['L0'] = nog_list[0]
out_df['L1'] = nog_list[1]
out_df['obj_L0'] = obj_num[0]
out_df['obj_L1'] = obj_num[1]
out_path = os.path.join(basepath, 'nog_list.csv')
out_df.to_csv(out_path, index=False)

