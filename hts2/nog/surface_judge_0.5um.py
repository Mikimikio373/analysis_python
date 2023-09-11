import math
import os
import sys
import json
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import heapq

def calc_z(nog_diff, z, num):
    min_list = heapq.nsmallest(num, nog_diff)
    sum_nog_z = 0
    weight_sum = 0
    for i in range(num):
        sum_nog_z += nog_diff[nog_diff.index(min_list[i])] * z[nog_diff.index(min_list[i])]
        weight_sum += nog_diff[nog_diff.index(min_list[i])]

    averge_z = sum_nog_z / weight_sum
    return averge_z



basepath = 'Q:/minami/20230911_nog_NRKR_tilt'
json_path = os.path.join(basepath, '0000', 'ValidViewHistory.json')
view_path = os.path.join(basepath, '0000', 'EachViewParam.json')
param_path = os.path.join(basepath, '0000', 'PARAMS', 'UserParam.json')
img_path = os.path.join(basepath, 'all_plots')
plot_mode = 0
if plot_mode == 1:
    os.makedirs(img_path, exist_ok=True)

with open(json_path, 'rb') as f:
    json_file = json.load(f)
print('{} loaded'.format(json_path))
with open(view_path, 'rb') as f:
    view_file = json.load(f)
print('{} loaded'.format(view_path))
with open(param_path, 'rb') as f:
    param_file = json.load(f)

print('json loaded')

gap = param_file['LayerParam']['CommonParamArray'][0]['ThickOfLayer'] / param_file['LayerParam']['CommonParamArray'][0]['NPicThickOfLayer']
npicnum = int(param_file['LayerParam']['CommonParamArray'][0]['NPicSnap'])

factor = 10


# sensor24個分の配列を用意
peak_list = []
for i in range(2):
    peak_list.append([])
for i in range(2):
    for j in range(12):
        peak_list[i].append([])

for view in range(len(json_file)):
    all_sensor_peak = []
    # z_begin = view_file[24 * view]['Z_begin'] * 1000
    z = np.arange(npicnum)
    # z = z * gap
    # z = z_begin - z
    z = -z * gap
    for i in range(len(json_file[view]['Nogs'])):



        nog_dff = []
        for j in range(len(json_file[view]['Nogs'][i]) - 1):
            nog_dff.append(json_file[view]['Nogs'][i][j - 1] - json_file[view]['Nogs'][i][j])

        nog_dff = [0 if abs(i) > 1700 else i for i in nog_dff]
        tar_z = calc_z(nog_dff[1:], z[1:-1], 10)
        all_sensor_peak.append(tar_z)
        if plot_mode == 1:
            fig = plt.figure(figsize=(factor, factor * math.sqrt(2)))
            fig.suptitle('V{:04}_M{}_S{:02}'.format(view, math.floor(i / 12), i % 12))
            ax1 = fig.add_subplot(211)
            ax1.scatter(z, json_file[view]['Nogs'][i], marker='x')
            ax1.axvline(x=tar_z, c='r')
            ax1.set_title('nog')
            ax1.set_ylabel('number of hit pixel')
            ax2 = fig.add_subplot(212)
            ax2.scatter(z[1:-1], nog_dff[1:], marker='x')
            ax2.axvline(x=tar_z, c='r')
            ax2.set_xlabel('z [um]')
            ax2.set_ylabel('nog difference')
            save_path = os.path.join(img_path, 'V{:04}_M{}_S{:02}.png'.format(view, math.floor(i / 12), i % 12))
            plt.savefig(save_path, dpi=150)
            plt.close(fig)

    # あまりにもぎりぎりのところはスキップ
    if abs(min(all_sensor_peak)) < 1.0 or abs(max(all_sensor_peak)) > 31.0:
        print('view: {} skipped'.format(view))
        continue
    for i in range(24):
        # 1-7(プログラム的には1-6)が18番目
        # peak_list[math.floor(i / 12)][i % 12].append(all_sensor_peak[i])
        peak_list[math.floor(i / 12)][i % 12].append(all_sensor_peak[i] - all_sensor_peak[18])


out_df = pd.DataFrame()
for i in range(24):
    out_df['{}-{}'.format(math.floor(i / 12), i % 12)] = peak_list[math.floor(i / 12)][i % 12]

out_path = os.path.join(basepath, 'peak_list.csv')
out_df.to_csv(out_path, index=False)

index_list = []
x_list = []
y_list = []
z_list = []
zerr_list = []
module_flag = []
x_width = 1.177
y_width = 0.572
for i in range(24):
    if math.floor(i /12) == 0:
        flag = 0
        if i % 4 == 0:
            x = x_width * 2.5
        elif i % 4 == 1:
            x = x_width * 0.5
        elif i % 4 == 2:
            x = -x_width * 1.5
        else:
            x = -x_width * 3.5
        if math.floor(i / 4) == 0:
            y = - y_width * 3
        elif math.floor(i / 4) == 1:
            y = 0
        else:
            y = y_width * 3
    else:
        flag = 1
        if i % 4 == 0:
            x = x_width * 3.5
        elif i % 4 == 1:
            x = x_width * 1.5
        elif i % 4 == 2:
            x = -x_width * 0.5
        else:
            x = -x_width * 2.5

        if math.floor((i - 12) / 4) == 0:
            y = y_width * 3
        elif math.floor((i - 12) / 4) == 1:
            y = 0
        else:
            y = -y_width * 3

    index_list.append('{}-{}'.format(math.floor(i / 12), i % 12))
    x_list.append(x)
    y_list.append(y)
    peak_z = np.mean(peak_list[math.floor(i / 12)][i % 12])
    peak_z_err = np.std(peak_list[math.floor(i / 12)][i % 12]) / math.sqrt(len(peak_list[math.floor(i / 12)][i % 12]))
    z_list.append(peak_z)
    zerr_list.append(peak_z_err)
    module_flag.append(flag)

xyz_df = pd.DataFrame()
xyz_df['index'] = index_list
xyz_df['x'] = x_list
xyz_df['y'] = y_list
xyz_df['z'] = z_list
xyz_df['z_err'] = zerr_list
xyz_df['flag'] = module_flag
out_path2 = os.path.join(basepath, 'xyz.csv')
xyz_df.to_csv(out_path2, index=False)
