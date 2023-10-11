import json
import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import yaml
import math
import copy
from mpl_toolkits.axes_grid1 import make_axes_locatable
import itertools

step_x = 9.0
step_y = 4.95

def textbox(ax, flat_list, ax_x_max, ax_y_max):
    entries = len(flat_list)
    length = len(str(entries))
    mean = np.mean(flat_list)
    std_dev = np.std(flat_list)
    if len(str(mean)) > length:
        if str(mean)[0:length][-1] == '.':
            str_mean = 'Mean:     {}'.format(str(mean)[0:length - 1])
        else:
            str_mean = 'Mean:    {}'.format(str(mean)[0:length])
    else:
        str_mean = 'Mean:    {}'.format(str(mean).rjust(length))

    if len(str(std_dev)) > length:
        if str(std_dev)[0:length][-1] == '.':
            str_std = 'Std Dev:  {}'.format(str(std_dev)[0:length - 1])
        else:
            str_std = 'Std Dev: {}'.format(str(std_dev)[0:length])
    else:
        str_std = 'Std Dev: {}'.format(str(std_dev).rjust(length))

    text = 'Entries: {}\n{}\n{}'.format(entries, str_mean, str_std)
    ax.text(ax_x_max * 0.9, ax_y_max * 0.9, text, bbox=(dict(boxstyle='square', fc='w')))

if not len(sys.argv) == 2:
    sys.exit('please enter \"target path\"')

basepath = sys.argv[1]


out_path = os.path.join(basepath, 'GRAPH')
if not os.path.exists(out_path):
    os.makedirs(out_path)

# sensor_exposureをたたいているコマンドから、scan_chech_toolの場所を特定
pythonpath = os.path.split(sys.argv[0])[0]
# sensorの場所情報を書いてあるフォルダを読み込み
with open(os.path.join(pythonpath, 'sensor_pos.yml'), 'rb') as f:
    y_load = yaml.safe_load(f)
y_sorted = sorted(y_load, key=lambda x: x['pos'])

ScanAreaParam = os.path.join(basepath, 'ScanAreaParam.json')
with open(ScanAreaParam, 'rb') as sap:
    sap_json = json.load(sap)

with open(os.path.join(basepath, 'ValidViewHistory.json'), 'rb') as f:
    vvh_json = json.load(f)

sideX = sap_json['SideX']
sideY = sap_json['SideY']
layer = sap_json['Layer']
step_x_num = math.ceil(sideX / step_x)
step_y_num = math.ceil(sideY / step_y)
step_y_num3 = step_y_num * 3
one_third_view = step_x_num * step_y_num
half_view = step_y_num3 * step_x_num
view = half_view * layer

# 入れ物用意
ex_l0 = []
ex_l1 = []
# module数の判断はview数などからできるはず(1/3かhalfかfullか)
module = 2
sensor = 12
imager_num = module * sensor
for i in range(imager_num):
    ex_l0.append([])
    ex_l1.append([])

for view in range(len(vvh_json)):
    for i in range(imager_num):
        if vvh_json[view]['Layer'] == 0:
            ex_l0[i].append(vvh_json[view]['ImagerControllerParam']['ExposureCount'][i])
        else:
            ex_l1[i].append(vvh_json[view]['ImagerControllerParam']['ExposureCount'][i])


ex_array_l0 = np.zeros((step_y_num * 9, step_x_num * 8))
ex_array_l1 = np.zeros((step_y_num * 9, step_x_num * 8))

print('all scan area view num: {}'.format(half_view))
print('scaned area view num: {}'.format(len(ex_l0[0])))
for i in range(len(ex_l0[0])):
    # 1/3でY方向を3分割しているため何レーン目かを判断
    y_lane = math.floor(i / step_x_num) % 3
    for py in range(9):
        for px in range(8):
            pos = py * 8 + px

            id = y_sorted[pos]['id']
            if id > 23:
                continue
            tmp_l0 = ex_l0[id][i]
            tmp_l1 = ex_l1[id][i]
            #全pcolermesh座標系におけるx,yの計算
            array_x_l0 = (i % step_x_num) * 8 + px     # xはviewのx座標とpxで計算
            array_x_l1 = (step_x_num - 1 - (i % step_x_num)) * 8 + px   # l1側はviewの順序を反転
            array_y = math.floor(i / (step_x_num * 3)) * 9 + py + y_lane    # yはstep_x_numの三倍の商がフルセンサーのview_y + ３回のうち何回目か
            ex_array_l0[array_y][array_x_l0] = tmp_l0
            ex_array_l1[array_y][array_x_l1] = tmp_l1



cmap = copy.copy(plt.get_cmap("jet"))
cmap.set_under('w', 1)  # 下限以下の色を設定


x = np.arange(step_x_num * 8)
x = x * step_x / 8
y = np.arange(step_y_num * 9)
y = y * step_y / 9
x, y = np.meshgrid(x, y)

fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)

ax1 = plt.subplot(221, title='L0 exposure count')
z_ber0 = ax1.pcolormesh(x, y, ex_array_l0, cmap=cmap, vmin=1, vmax=1000)
divider0 = make_axes_locatable(ax1) #axに紐付いたAxesDividerを取得
cax0 = divider0.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)
ax1.set_aspect('equal')
ax1.set_xlabel('X [mm]')
ax1.set_ylabel('Y [mm]')

ax2 = plt.subplot(222, title='L1 exposure count')
z_ber1 = ax2.pcolormesh(x, y, ex_array_l1, cmap=cmap, vmin=1, vmax=1000)
divider1 = make_axes_locatable(ax2) #axに紐付いたAxesDividerを取得
cax1 = divider1.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp1 = fig.colorbar(z_ber1, orientation="vertical", cax=cax1)
ax2.set_aspect('equal')
ax2.set_xlabel('X [mm]')
ax2.set_ylabel('Y [mm]')

ax3 = plt.subplot(223, title='L0 exposure count')
flat_not_l0 = list(itertools.chain.from_iterable(ex_array_l0))
hist_return0 = ax3.hist(flat_not_l0, histtype='step', bins=100, range=(0, 1000), color='w', ec='r')
textbox(ax3, flat_not_l0, 1000, max(hist_return0[0]))

ax4 = plt.subplot(224, title='L1 exposure count')
flat_not_l1 = list(itertools.chain.from_iterable(ex_array_l1))
hist_return1 = ax4.hist(flat_not_l1, histtype='step', bins=100, range=(0, 1000), color='w', ec='b')
textbox(ax4, flat_not_l1, 1000, max(hist_return1[0]))

# plt.show()
plt.savefig(os.path.join(out_path, 'exposure_count_plot.png'), dpi=300)


