import json
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as mticker
from matplotlib.colors import Normalize # Normalizeをimport


basepath = 'Q:/minami/20230914_300mm240mm'
not_path = os.path.join(basepath, 'GRAPH', 'NOT')

df_not = pd.DataFrame()
for module in range(2):
    for sensor in range(12):
        txt_path = os.path.join(not_path, '{:02}_{:02}_TrackHit2_0_99999999_0_000.txt'.format(module, sensor))
        if not os.path.exists(txt_path):
            sys.exit('there are no file: {}'.format(txt_path))
        f = open(txt_path, 'r')
        data = f.readlines()
        df_not['{}-{:02}'.format(module, sensor)] = data

not_all = []
view = 0
for vy in range(48):
    not_line_l0_0 = []
    not_line_l0_1 = []
    not_line_l0_2 = []
    not_line_l1 = []
    for i in range(3):
        line_tmp0 = []
        line_tmp1 = []
        line_tmp2 = []
        for vx in range(33):
            line_tmp0.append(int(df_not['1-00'][view].split(' ')[9]))
            line_tmp0.append(int(df_not['0-08'][view].split(' ')[9]))
            line_tmp0.append(int(df_not['1-01'][view].split(' ')[9]))
            line_tmp0.append(int(df_not['0-09'][view].split(' ')[9]))
            line_tmp0.append(int(df_not['1-02'][view].split(' ')[9]))
            line_tmp0.append(int(df_not['0-10'][view].split(' ')[9]))
            line_tmp0.append(int(df_not['1-03'][view].split(' ')[9]))
            line_tmp0.append(int(df_not['0-11'][view].split(' ')[9]))

            line_tmp1.append(int(df_not['1-04'][view].split(' ')[9]))
            line_tmp1.append(int(df_not['0-04'][view].split(' ')[9]))
            line_tmp1.append(int(df_not['1-05'][view].split(' ')[9]))
            line_tmp1.append(int(df_not['0-05'][view].split(' ')[9]))
            line_tmp1.append(int(df_not['1-06'][view].split(' ')[9]))
            line_tmp1.append(int(df_not['0-06'][view].split(' ')[9]))
            line_tmp1.append(int(df_not['1-07'][view].split(' ')[9]))
            line_tmp1.append(int(df_not['0-07'][view].split(' ')[9]))

            line_tmp2.append(int(df_not['1-08'][view].split(' ')[9]))
            line_tmp2.append(int(df_not['0-00'][view].split(' ')[9]))
            line_tmp2.append(int(df_not['1-09'][view].split(' ')[9]))
            line_tmp2.append(int(df_not['0-01'][view].split(' ')[9]))
            line_tmp2.append(int(df_not['1-10'][view].split(' ')[9]))
            line_tmp2.append(int(df_not['0-02'][view].split(' ')[9]))
            line_tmp2.append(int(df_not['1-11'][view].split(' ')[9]))
            line_tmp2.append(int(df_not['0-03'][view].split(' ')[9]))

            view += 1
        not_line_l0_0.append(line_tmp0)
        not_line_l0_1.append(line_tmp1)
        not_line_l0_2.append(line_tmp2)
    for i in range(3):
        not_all.append(not_line_l0_0[i])
    for i in range(3):
        not_all.append(not_line_l0_1[i])
    for i in range(3):
        not_all.append(not_line_l0_2[i])

    for i in range(3):
        for vx in range(33):
            view += 1

x = np.arange(0, 297, 1.125)
y = np.arange(0, 237.6, 0.55)
# x, y = np.mgrid[:len(not_all), :len(not_all[0])]
# print(x)
# print(y)
# print(not_all)
# fig, ax = plt.subplots()
# z = ax.pcolormesh(x, y, not_all, cmap='jet', vmin=0, vmax=30000)
# pp = fig.colorbar(z, ax=ax, orientation="vertical")
# ax.set_xlabel('X [mm]')
# ax.set_ylabel('Y [mm]')
# ax.set_aspect('equal')
#
# plt.show()

df_not_list = pd.DataFrame()
not_list_sensor = []
for module in range(2):
    for sensor in range(12):
        nog_list = []
        for i in range(len(df_not['{}-{:02}'.format(module, sensor)])):
            nog_list.append(int(df_not['{}-{:02}'.format(module, sensor)][i].split(' ')[9]))

        df_not_list['{}-{:02}'.format(module, sensor)] = [np.average(nog_list)]
        not_list_sensor.append(np.average(nog_list))

x = np.arange(24)
plt.plot(x, not_list_sensor, 'x')
plt.ylim(0, 16000)
plt.xticks(np.arange(0,24))
plt.grid()
plt.xlabel('sensor ID')
plt.ylabel('average not')
# plt.show()
plt.clf()

json_path = 'X:/Project_v3/AdminParam/HTS2/SapEVMG/default_HTS.json'
with open(json_path, 'rb') as f:
    json_data = json.load(f)

tar_bright = []
for i in range(24):
    tar_bright.append(int(json_data['ImagerControllerParamList'][i]['TargetBrightness']))

plt.plot(tar_bright, not_list_sensor, 'x')
plt.xlabel('taget bright')
plt.ylabel('average not')
# plt.show()
plt.clf()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x, tar_bright, not_list_sensor)
# plt.show()

out_df = pd.DataFrame()
out_df['sensor'] = x + 1
out_df['not'] = not_list_sensor
out_df['tar_bright'] = tar_bright
out_df.to_csv(os.path.join(basepath, 'GRAPH', 'not_list.csv'), index=False)
