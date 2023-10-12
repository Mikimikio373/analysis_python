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
            ax.text(num_c, num_r, '{:.3g}'.format(value), color=color, ha='center', va='center')

module = 2
sensor = 12
imager_num = module * sensor
plot_max = 25
plot_min = 10


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

# imager idごとのすべてのnog　list all_nog[id][viex][picture num]
topbottom_l0 = []
topbottom_l1 = []
for i in range(imager_num):
    topbottom_l0.append([])
    topbottom_l1.append([])

for view in range(len(vvh_json)):
    for id in range(imager_num):
        top = int(vvh_json[view]['SurfaceDetail'][id]['Top'])
        bottom = int(vvh_json[view]['SurfaceDetail'][id]['Bottom'])

        if vvh_json[view]['Layer'] == 0:
            topbottom_l0[id].append(bottom - top)
        else:
            topbottom_l1[id].append(bottom - top)

ave_topbottom_l0 = []
ave_topbottom_l1 = []
for id in range(imager_num):
    ave_topbottom_l0.append(np.average(topbottom_l0[id]))
    ave_topbottom_l1.append(np.average(topbottom_l1[id]))

cmap = copy.copy(plt.get_cmap("jet"))
cmap.set_under('w', 1) # 下限以下の色を設定
z0 = np.zeros((9, 8))
z1 = np.zeros((9, 8))
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
            z0[py][px] = ave_topbottom_l0[id]
            z1[py][px] = ave_topbottom_l1[id]

fig2 = plt.figure(figsize=(11.69, 8.27), tight_layout=True)
fig2.suptitle('Top to Bottom', fontsize=20)
ax0 = plt.subplot(221, title='L0 array')
z_ber20 = ax0.pcolormesh(x, y, z0, cmap=cmap, vmin=plot_min, vmax=plot_max, edgecolors="black")
divider20 = make_axes_locatable(ax0) #axに紐付いたAxesDividerを取得
cax20 = divider20.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp0 = fig2.colorbar(z_ber20, orientation="vertical", cax=cax20)
text(z0, ax0, 'black')

ax1 = plt.subplot(222, title='L1 array')
z_ber21 = ax1.pcolormesh(x, y, z1, cmap=cmap, vmin=plot_min, vmax=plot_max, edgecolors="black")
divider21 = make_axes_locatable(ax1) #axに紐付いたAxesDividerを取得
cax21 = divider21.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp1 = fig2.colorbar(z_ber20, orientation="vertical", cax=cax21)
text(z1, ax1, 'black')

ax2 = plt.subplot(223, title='L0')
x = np.arange(24)
ax2.plot(x, ave_topbottom_l0, marker='x', c='r')
ax2.set_ylim(plot_min, plot_max)
ax2.set_xticks(x)
ax2.grid()

ax3 = plt.subplot(224, title='L1')
x = np.arange(24)
ax3.plot(x, ave_topbottom_l1, marker='x', c='b')
ax3.set_ylim(plot_min, plot_max)
ax3.set_xticks(x)
ax3.grid()

plt.savefig(os.path.join(basepath, 'GRAPH', 'sensor_topbottom.png'), dpi=300)
plt.clf()

