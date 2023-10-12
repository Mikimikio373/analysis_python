import json
import os
import sys
import math
import numpy as np
import copy
import matplotlib.pyplot as plt
import yaml
from mpl_toolkits.axes_grid1 import make_axes_locatable
import itertools


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


module = 2
sensor = 12
step_x = 9.0
step_y = 4.95
imager_num = module * sensor
nog_max = 60000
nog_min = 1
nog_top_bottom_max = 100000
nog_top_bottom_min = 1

if not len(sys.argv) == 2:
    sys.exit('please enter \"target path\"')

basepath = sys.argv[1]


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

with open(os.path.join(basepath, 'ScanControllParam.json') , 'rb') as f:
    scan_cont_json = json.load(f)

npicture = int(scan_cont_json['LayerParam']['CommonParamArray'][0]['NPicSnap'])

sideX = sap_json['SideX']
sideY = sap_json['SideY']
layer = sap_json['Layer']
step_x_num = math.ceil(sideX / step_x)
step_y_num = math.ceil(sideY / step_y)
step_y_num3 = step_y_num * 3
one_third_view = step_x_num * step_y_num
half_view = step_y_num3 * step_x_num
view = half_view * layer

# imager idごとのすべてのnog　list all_nog[id][viex][picture num]
all_nog_l0 = []
all_nog_l1 = []
nog_over_thr_l0 = []
nog_over_thr_l1 = []
top_l0 = []
top_l1 = []
bottom_l0 = []
bottom_l1 = []
for i in range(imager_num):
    all_nog_l0.append([])
    all_nog_l1.append([])
    nog_over_thr_l0.append([])
    nog_over_thr_l1.append([])
    top_l0.append([])
    top_l1.append([])
    bottom_l0.append([])
    bottom_l1.append([])

for view in range(len(vvh_json)):
    for id in range(imager_num):
        if vvh_json[view]['Layer'] == 0:
            bottom = int(vvh_json[view]['SurfaceDetail'][id]['Bottom']) - 1
            if bottom < 15:
                bottom = 15
            top = bottom - 15
            all_nog_l0[id].append(vvh_json[view]['Nogs'][id])
            nog_over_thr_l0[id].append(vvh_json[view]['SurfaceDetail'][id]['NogOverThr'])
            top_l0[id].append(int(vvh_json[view]['Nogs'][id][top]))
            bottom_l0[id].append(int(vvh_json[view]['Nogs'][id][bottom]))
        else:
            top = int(vvh_json[view]['SurfaceDetail'][id]['Top'])
            if top > npicture - 16:
                top = npicture - 16
            bottom = top + 15
            all_nog_l1[id].append(vvh_json[view]['Nogs'][id])
            nog_over_thr_l1[id].append(vvh_json[view]['SurfaceDetail'][id]['NogOverThr'])
            top_l1[id].append(int(vvh_json[view]['Nogs'][id][top]))
            bottom_l1[id].append(int(vvh_json[view]['Nogs'][id][bottom]))

cmap = copy.copy(plt.get_cmap("jet"))
cmap.set_under('w', 1)  # 下限以下の色を設定


scan_array_l0 = np.zeros((step_y_num * 9, step_x_num * 8))
scan_array_l1 = np.zeros((step_y_num * 9, step_x_num * 8))

print('all scan area view num: {}'.format(half_view))
print('scaned area view num: {}'.format(len(nog_over_thr_l0[0])))
for i in range(len(nog_over_thr_l0[0])):
    # 1/3でY方向を3分割しているため何レーン目かを判断
    y_lane = math.floor(i / step_x_num) % 3
    for py in range(9):
        for px in range(8):
            pos = py * 8 + px

            id = y_sorted[pos]['id']
            if id > 23:
                continue
            tmp_l0 = nog_over_thr_l0[id][i]
            tmp_l1 = nog_over_thr_l1[id][i]
            #全pcolermesh座標系におけるx,yの計算
            array_x_l0 = (i % step_x_num) * 8 + px     # xはviewのx座標とpxで計算
            array_x_l1 = (step_x_num - 1 - (i % step_x_num)) * 8 + px   # l1側はviewの順序を反転
            array_y = math.floor(i / (step_x_num * 3)) * 9 + py + y_lane    # yはstep_x_numの三倍の商がフルセンサーのview_y + ３回のうち何回目か
            scan_array_l0[array_y][array_x_l0] = tmp_l0
            scan_array_l1[array_y][array_x_l1] = tmp_l1

x = np.arange(step_x_num * 8)
x = x * step_x / 8
y = np.arange(step_y_num * 9)
y = y * step_y / 9
x, y = np.meshgrid(x, y)

fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
fig.suptitle('Nogs (over threshold average)', fontsize=20)
ax1 = plt.subplot(221, title='Layer0')
z_ber0 = ax1.pcolormesh(x, y, scan_array_l0, cmap=cmap, vmin=nog_min, vmax=nog_max)
divider0 = make_axes_locatable(ax1) #axに紐付いたAxesDividerを取得
cax0 = divider0.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)
ax1.set_aspect('equal')
ax1.set_xlabel('X [mm]')
ax1.set_ylabel('Y [mm]')

ax2 = plt.subplot(222, title='Layer1')
z_ber1 = ax2.pcolormesh(x, y, scan_array_l1, cmap=cmap, vmin=nog_min, vmax=nog_max)
divider1 = make_axes_locatable(ax2) #axに紐付いたAxesDividerを取得
cax1 = divider1.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp1 = fig.colorbar(z_ber1, orientation="vertical", cax=cax1)
ax2.set_aspect('equal')
ax2.set_xlabel('X [mm]')
ax2.set_ylabel('Y [mm]')

ax3 = plt.subplot(223, title='Layer0')
flat_not_l0 = list(itertools.chain.from_iterable(scan_array_l0))
hist_return0 = ax3.hist(flat_not_l0, histtype='step', bins=100, range=(nog_min, nog_max), color='w', ec='r')
textbox(ax3, flat_not_l0, nog_max, max(hist_return0[0]))

ax4 = plt.subplot(224, title='Layer1')
flat_not_l1 = list(itertools.chain.from_iterable(scan_array_l1))
hist_return1 = ax4.hist(flat_not_l1, histtype='step', bins=100, range=(nog_min, nog_max), color='w', ec='b')
textbox(ax4, flat_not_l1, nog_max, max(hist_return1[0]))

# plt.show()
plt.savefig(os.path.join(basepath, 'GRAPH', 'scan_area_nog.png'), dpi=300)
plt.clf()

for i in range(len(top_l0[0])):
    # 1/3でY方向を3分割しているため何レーン目かを判断
    y_lane = math.floor(i / step_x_num) % 3
    for py in range(9):
        for px in range(8):
            pos = py * 8 + px

            id = y_sorted[pos]['id']
            if id > 23:
                continue
            tmp_l0 = top_l0[id][i]
            tmp_l1 = top_l1[id][i]
            #全pcolermesh座標系におけるx,yの計算
            array_x_l0 = (i % step_x_num) * 8 + px     # xはviewのx座標とpxで計算
            array_x_l1 = (step_x_num - 1 - (i % step_x_num)) * 8 + px   # l1側はviewの順序を反転
            array_y = math.floor(i / (step_x_num * 3)) * 9 + py + y_lane    # yはstep_x_numの三倍の商がフルセンサーのview_y + ３回のうち何回目か
            scan_array_l0[array_y][array_x_l0] = tmp_l0
            scan_array_l1[array_y][array_x_l1] = tmp_l1

x = np.arange(step_x_num * 8)
x = x * step_x / 8
y = np.arange(step_y_num * 9)
y = y * step_y / 9
x, y = np.meshgrid(x, y)

fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
fig.suptitle('Nogs picnum0', fontsize=20)
ax1 = plt.subplot(221, title='Layer0')
z_ber0 = ax1.pcolormesh(x, y, scan_array_l0, cmap=cmap, vmin=nog_top_bottom_min, vmax=nog_top_bottom_max)
divider0 = make_axes_locatable(ax1) #axに紐付いたAxesDividerを取得
cax0 = divider0.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)
ax1.set_aspect('equal')
ax1.set_xlabel('X [mm]')
ax1.set_ylabel('Y [mm]')

ax2 = plt.subplot(222, title='Layer1')
z_ber1 = ax2.pcolormesh(x, y, scan_array_l1, cmap=cmap, vmin=nog_top_bottom_min, vmax=nog_top_bottom_max)
divider1 = make_axes_locatable(ax2) #axに紐付いたAxesDividerを取得
cax1 = divider1.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp1 = fig.colorbar(z_ber1, orientation="vertical", cax=cax1)
ax2.set_aspect('equal')
ax2.set_xlabel('X [mm]')
ax2.set_ylabel('Y [mm]')

ax3 = plt.subplot(223, title='Layer0')
flat_not_l0 = list(itertools.chain.from_iterable(scan_array_l0))
hist_return0 = ax3.hist(flat_not_l0, histtype='step', bins=100, range=(nog_top_bottom_min, nog_top_bottom_max), color='w', ec='r')
textbox(ax3, flat_not_l0, nog_top_bottom_max, max(hist_return0[0]))

ax4 = plt.subplot(224, title='Layer1')
flat_not_l1 = list(itertools.chain.from_iterable(scan_array_l1))
hist_return1 = ax4.hist(flat_not_l1, histtype='step', bins=100, range=(nog_top_bottom_min, nog_top_bottom_max), color='w', ec='b')
textbox(ax4, flat_not_l1, nog_top_bottom_max, max(hist_return1[0]))

# plt.show()
plt.savefig(os.path.join(basepath, 'GRAPH', 'scan_area_nog0.png'), dpi=300)
plt.clf()

for i in range(len(bottom_l0[0])):
    # 1/3でY方向を3分割しているため何レーン目かを判断
    y_lane = math.floor(i / step_x_num) % 3
    for py in range(9):
        for px in range(8):
            pos = py * 8 + px

            id = y_sorted[pos]['id']
            if id > 23:
                continue
            tmp_l0 = bottom_l0[id][i]
            tmp_l1 = bottom_l1[id][i]
            #全pcolermesh座標系におけるx,yの計算
            array_x_l0 = (i % step_x_num) * 8 + px     # xはviewのx座標とpxで計算
            array_x_l1 = (step_x_num - 1 - (i % step_x_num)) * 8 + px   # l1側はviewの順序を反転
            array_y = math.floor(i / (step_x_num * 3)) * 9 + py + y_lane    # yはstep_x_numの三倍の商がフルセンサーのview_y + ３回のうち何回目か
            scan_array_l0[array_y][array_x_l0] = tmp_l0
            scan_array_l1[array_y][array_x_l1] = tmp_l1

x = np.arange(step_x_num * 8)
x = x * step_x / 8
y = np.arange(step_y_num * 9)
y = y * step_y / 9
x, y = np.meshgrid(x, y)

fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
fig.suptitle('Nogs picnum15', fontsize=20)
ax1 = plt.subplot(221, title='Layer0')
z_ber0 = ax1.pcolormesh(x, y, scan_array_l0, cmap=cmap, vmin=nog_top_bottom_min, vmax=nog_top_bottom_max)
divider0 = make_axes_locatable(ax1) #axに紐付いたAxesDividerを取得
cax0 = divider0.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)
ax1.set_aspect('equal')
ax1.set_xlabel('X [mm]')
ax1.set_ylabel('Y [mm]')

ax2 = plt.subplot(222, title='Layer1')
z_ber1 = ax2.pcolormesh(x, y, scan_array_l1, cmap=cmap, vmin=nog_top_bottom_min, vmax=nog_top_bottom_max)
divider1 = make_axes_locatable(ax2) #axに紐付いたAxesDividerを取得
cax1 = divider1.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp1 = fig.colorbar(z_ber1, orientation="vertical", cax=cax1)
ax2.set_aspect('equal')
ax2.set_xlabel('X [mm]')
ax2.set_ylabel('Y [mm]')

ax3 = plt.subplot(223, title='Layer0')
flat_not_l0 = list(itertools.chain.from_iterable(scan_array_l0))
hist_return0 = ax3.hist(flat_not_l0, histtype='step', bins=100, range=(nog_top_bottom_min, nog_top_bottom_max), color='w', ec='r')
textbox(ax3, flat_not_l0, nog_top_bottom_max, max(hist_return0[0]))

ax4 = plt.subplot(224, title='Layer1')
flat_not_l1 = list(itertools.chain.from_iterable(scan_array_l1))
hist_return1 = ax4.hist(flat_not_l1, histtype='step', bins=100, range=(nog_top_bottom_min, nog_top_bottom_max), color='w', ec='b')
textbox(ax4, flat_not_l1, nog_top_bottom_max, max(hist_return1[0]))

# plt.show()
plt.savefig(os.path.join(basepath, 'GRAPH', 'scan_area_nog15.png'), dpi=300)
plt.clf()
