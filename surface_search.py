import numpy as np
import cv2
import sys
import os
import pandas as pn

vxrange = 18
vyrange = 72
nog_thr_hight = 10000
# nog_thr_dist = 1000
nog_data = pn.read_csv('../nog_data.csv', index_col=0)
# print(nog_data)
first = []
last = []

nog_data['first'] = -1
nog_data['last'] = -1

for layer in range(0, 2):
    for vx in range(0, vxrange):
        for vy in range(0, vyrange):
            index_name = 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy)
            print(index_name)
            if layer == 0:
                nog_thr_dist = max(nog_data.loc[index_name].values) / 4
                for i in reversed(range(0, 24)):
                    if i == 14:
                        print('could not detect surface')
                        sys.exit()
                    nog_dist = abs(nog_data.loc[index_name][i - 1]-nog_data.loc[index_name][i])
                    # print([i, nog_data[index_name][i], nog_dist])
                    if nog_data.loc[index_name][i] > nog_thr_hight and nog_dist < nog_thr_dist:
                        last = i
                        first = last - 15
                        break
                    else:
                        continue
            elif layer == 1:
                nog_thr_dist = max(nog_data.loc[index_name].values) / 4
                for i in range(0, 24):
                    if i == 9:
                        print('could not detect surface')
                        sys.exit()
                    nog_dist = abs(nog_data.loc[index_name][i+1] - nog_data.loc[index_name][i])
                    # print(nog_dist)
                    if nog_data.loc[index_name][i] > nog_thr_hight and nog_dist < nog_thr_dist:
                        first = i
                        last = first + 15
                        break
                    else:
                        continue
            nog_data.loc[index_name]['first'] = first
            nog_data.loc[index_name]['last'] = last
            # print(nog_data)
            # print('first, last: {},{}'.format(first, last))
            # sys.exit()

nog_data.to_csv('../nog_data_b3.csv')
