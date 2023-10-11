import json
import os
import sys
import numpy as np
import copy
import matplotlib.pyplot as plt
import math
import yaml

def text(array: np.ndarray, ax, color: str):
    for num_r, row in enumerate(array):
        for num_c, value in enumerate(array[num_r]):
            ax.text(num_c, num_r, '{:d}'.format(int(value)), color=color, ha='center', va='center')

module = 2
sensor = 12
imager_num = module * sensor
ex_max = 1000
ex_min = 1

if not len(sys.argv) == 2:
    sys.exit('please enter \"target path\"')

target_path = sys.argv[1]
# sensor_exposureをたたいているコマンドから、scan_chech_toolの場所を特定
pythonpath = os.path.split(sys.argv[0])[0]
# sensorの場所情報を書いてあるフォルダを読み込み
with open(os.path.join(pythonpath, 'sensor_pos.yml'), 'rb') as f:
    y_load = yaml.safe_load(f)
y_sorted = sorted(y_load, key=lambda x: x['pos'])

with open(os.path.join(target_path, 'ValidViewHistory.json'), 'rb') as f:
    params = json.load(f)

all_exposure_l0 = []
all_exposure_l1 = []
for i in range(imager_num):
    all_exposure_l0.append([])
    all_exposure_l1.append([])

for view in range(len(params)):
    for i in range(imager_num):
        if params[view]['Layer'] == 0:
            all_exposure_l0[i].append(params[view]['ImagerControllerParam']['ExposureCount'][i])
        else:
            all_exposure_l1[i].append(params[view]['ImagerControllerParam']['ExposureCount'][i])

ave_exposure_l0 = []
ave_exposure_l1 = []
for i in range(imager_num):
    ave_exposure_l0.append(np.average(all_exposure_l0[i]))
    ave_exposure_l1.append(np.average(all_exposure_l1[i]))

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
            z0[py][px] = ave_exposure_l0[id]
            z1[py][px] = ave_exposure_l1[id]

fig = plt.figure(figsize=(10, 8), tight_layout=True)
fig.suptitle('exposure count', fontsize=20)
ax0 = plt.subplot(221, title='L0 array')
z_ber0 = ax0.pcolormesh(x, y, z0, cmap=cmap, vmax=ex_min, vmin=ex_max, edgecolors="black")
text(z0, ax0, 'black')
pp0 = fig.colorbar(z_ber0, orientation="vertical")
ax0.set_aspect(1088/2024)

ax1 = plt.subplot(222, title='L1 array')
z_ber1 = ax1.pcolormesh(x, y, z1, cmap=cmap, vmax=ex_min, vmin=ex_max, edgecolors="black")
text(z1, ax1, 'black')
pp1 = fig.colorbar(z_ber1, orientation="vertical")
ax1.set_aspect(1088/2024)

ax2 = plt.subplot(223, title='L0')
x = np.arange(24)
ax2.plot(x, ave_exposure_l0, marker='x', c='r')
ax2.set_ylim(ex_min, ex_max)
ax2.set_xticks(x)
ax2.grid()

ax3 = plt.subplot(224, title='L1')
x = np.arange(24)
ax3.plot(x, ave_exposure_l1, marker='x', c='b')
ax3.set_ylim(ex_min, ex_max)
ax3.set_xticks(x)
ax3.grid()

plt.savefig(os.path.join(target_path, 'GRAPH', 'exposure_count.png'), dpi=300)