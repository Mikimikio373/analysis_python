import json
import os
import sys
import numpy as np
import copy
import matplotlib.pyplot as plt
import yaml
from mpl_toolkits.axes_grid1 import make_axes_locatable

def text(array: np.ndarray, ax, color: str):
    for num_r, row in enumerate(array):
        for num_c, value in enumerate(array[num_r]):
            ax.text(num_c, num_r, '{:d}'.format(int(value)), color=color, ha='center', va='center')

module = 2
sensor = 12
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

with open(os.path.join(basepath, 'ValidViewHistory.json'), 'rb') as f:
    vvh_json = json.load(f)

with open(os.path.join(basepath, 'ScanControllParam.json') , 'rb') as f:
    scan_cont_json = json.load(f)

npicture = int(scan_cont_json['LayerParam']['CommonParamArray'][0]['NPicSnap'])

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
                top = npicture + 16
            bottom = top + 15
            all_nog_l1[id].append(vvh_json[view]['Nogs'][id])
            nog_over_thr_l1[id].append(vvh_json[view]['SurfaceDetail'][id]['NogOverThr'])
            top_l1[id].append(int(vvh_json[view]['Nogs'][id][top]))
            bottom_l1[id].append(int(vvh_json[view]['Nogs'][id][bottom]))

ave_nog_over_thr_l0 = []
ave_nog_over_thr_l1 = []
ave_top_l0 = []
ave_top_l1 = []
ave_bottom_l0 = []
ave_bottom_l1 = []
for id in range(imager_num):
    ave_nog_over_thr_l0.append(np.average(nog_over_thr_l0[id]))
    ave_nog_over_thr_l1.append(np.average(nog_over_thr_l0[id]))
    ave_top_l0.append(np.average(top_l0[id]))
    ave_top_l1.append(np.average(top_l1[id]))
    ave_bottom_l0.append(np.average(bottom_l0[id]))
    ave_bottom_l1.append(np.average(bottom_l1[id]))

cmap = copy.copy(plt.get_cmap("jet"))
cmap.set_under('w', 1) # 下限以下の色を設定
x = np.arange(8)
y = np.arange(9)
x, y = np.meshgrid(x, y)
z0 = np.zeros((9, 8))
z1 = np.zeros((9, 8))
for py in range(9):
    for px in range(8):
        id = y_sorted[py*8+px]['id']
        if id >23:
            z0[py][px] = 0
            z1[py][px] = 0
        else:
            z0[py][px] = ave_nog_over_thr_l0[id]
            z1[py][px] = ave_nog_over_thr_l1[id]

fig1 = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
fig1.suptitle('Nogs Threshold over average', fontsize=20)
ax0 = plt.subplot(221, title='Layer0 array')
z_ber0 = ax0.pcolormesh(x, y, z0, cmap=cmap, vmax=nog_min, vmin=nog_max, edgecolors="black")
text(z0, ax0, 'black')
divider0 = make_axes_locatable(ax0) #axに紐付いたAxesDividerを取得
cax0 = divider0.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp0 = fig1.colorbar(z_ber0, orientation="vertical", cax=cax0)

ax1 = plt.subplot(222, title='Layer1 array')
z_ber1 = ax1.pcolormesh(x, y, z1, cmap=cmap, vmax=nog_min, vmin=nog_max, edgecolors="black")
text(z1, ax1, 'black')
divider1 = make_axes_locatable(ax1) #axに紐付いたAxesDividerを取得
cax1 = divider1.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp1 = fig1.colorbar(z_ber1, orientation="vertical", cax=cax1)

ax2 = plt.subplot(223, title='L0')
x = np.arange(24)
ax2.plot(x, ave_nog_over_thr_l0, marker='x', c='r')
ax2.set_ylim(nog_min, nog_max)
ax2.set_xticks(x)
ax2.grid()

ax3 = plt.subplot(224, title='L1')
x = np.arange(24)
ax3.plot(x, ave_nog_over_thr_l1, marker='x', c='b')
ax3.set_ylim(nog_min, nog_max)
ax3.set_xticks(x)
ax3.grid()

plt.savefig(os.path.join(basepath, 'GRAPH', 'sensor_nog.png'), dpi=300)
plt.clf()

x = np.arange(8)
y = np.arange(9)
x, y = np.meshgrid(x, y)
for py in range(9):
    for px in range(8):
        id = y_sorted[py*8+px]['id']
        if id >23:
            z0[py][px] = 0
            z1[py][px] = 0
        else:
            z0[py][px] = ave_top_l0[id]
            z1[py][px] = ave_top_l1[id]

fig2 = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
fig2.suptitle('Nogs Top', fontsize=20)
ax0 = plt.subplot(221, title='Layer0 array')
z_ber0 = ax0.pcolormesh(x, y, z0, cmap=cmap, vmax=nog_top_bottom_min, vmin=nog_top_bottom_max, edgecolors="black")
text(z0, ax0, 'black')
divider0 = make_axes_locatable(ax0) #axに紐付いたAxesDividerを取得
cax0 = divider0.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp0 = fig2.colorbar(z_ber0, orientation="vertical", cax=cax0)

ax1 = plt.subplot(222, title='Layer1 array')
z_ber1 = ax1.pcolormesh(x, y, z1, cmap=cmap, vmax=nog_top_bottom_min, vmin=nog_top_bottom_max, edgecolors="black")
text(z1, ax1, 'black')
divider1 = make_axes_locatable(ax1) #axに紐付いたAxesDividerを取得
cax1 = divider1.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp1 = fig2.colorbar(z_ber1, orientation="vertical", cax=cax1)

ax2 = plt.subplot(223, title='L0')
x = np.arange(24)
ax2.plot(x, ave_top_l0, marker='x', c='r')
ax2.set_ylim(nog_top_bottom_min, nog_top_bottom_max)
ax2.set_xticks(x)
ax2.grid()

ax3 = plt.subplot(224, title='L1')
x = np.arange(24)
ax3.plot(x, ave_top_l1, marker='x', c='b')
ax3.set_ylim(nog_top_bottom_min, nog_top_bottom_max)
ax3.set_xticks(x)
ax3.grid()

plt.savefig(os.path.join(basepath, 'GRAPH', 'sensor_nog0.png'), dpi=300)
plt.clf()

x = np.arange(8)
y = np.arange(9)
x, y = np.meshgrid(x, y)
for py in range(9):
    for px in range(8):
        id = y_sorted[py*8+px]['id']
        if id >23:
            z0[py][px] = 0
            z1[py][px] = 0
        else:
            z0[py][px] = ave_bottom_l0[id]
            z1[py][px] = ave_bottom_l1[id]

fig3 = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
fig3.suptitle('Nogs Bottom', fontsize=20)
ax0 = plt.subplot(221, title='Layer0 array')
z_ber0 = ax0.pcolormesh(x, y, z0, cmap=cmap, vmax=nog_top_bottom_min, vmin=nog_top_bottom_max, edgecolors="black")
text(z0, ax0, 'black')
divider0 = make_axes_locatable(ax0) #axに紐付いたAxesDividerを取得
cax0 = divider0.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp0 = fig3.colorbar(z_ber0, orientation="vertical", cax=cax0)

ax1 = plt.subplot(222, title='Layer1 array')
z_ber1 = ax1.pcolormesh(x, y, z1, cmap=cmap, vmax=nog_top_bottom_min, vmin=nog_top_bottom_max, edgecolors="black")
text(z1, ax1, 'black')
divider1 = make_axes_locatable(ax1) #axに紐付いたAxesDividerを取得
cax1 = divider1.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp1 = fig3.colorbar(z_ber1, orientation="vertical", cax=cax1)

ax2 = plt.subplot(223, title='L0')
x = np.arange(24)
ax2.plot(x, ave_bottom_l0, marker='x', c='r')
ax2.set_ylim(nog_top_bottom_min, nog_top_bottom_max)
ax2.set_xticks(x)
ax2.grid()

ax3 = plt.subplot(224, title='L1')
x = np.arange(24)
ax3.plot(x, ave_bottom_l1, marker='x', c='b')
ax3.set_ylim(nog_top_bottom_min, nog_top_bottom_max)
ax3.set_xticks(x)
ax3.grid()

plt.savefig(os.path.join(basepath, 'GRAPH', 'sensor_nog15.png'), dpi=300)