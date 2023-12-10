import copy
import json
import sys

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import yaml

import hts2_plot_module as mylib

json_path = 'A:/Test/check_FASER/0001/ValidViewHistory.json'

with open('sensor_pos.yml', 'rb') as f:
    sensor_y = yaml.safe_load(f)
y_sorted = sorted(sensor_y, key=lambda x: x['pos'])

with open(json_path, 'rb') as f:
    data = json.load(f)
imager_num = 24
StartNPic = []
ave = []
for i in range(imager_num):
    StartNPic.append([])
    ave.append([])

for i in range(len(data)):
    for s in range(24):
        if not data[i]['SurfaceDetail'][s]['Found']:
            continue
    for s in range(24):
        StartNPic[s].append(data[i]['StartAnalysisPicNo'][s])

for s in range(imager_num):
    ave[s] = np.mean(StartNPic[s])

thickness = 55.0 / 15
ave = np.asarray(ave) * thickness
minimum = np.min(ave)
print(ave)

z = np.zeros((9, 8))
for py in range(9):
    for px in range(8):
        id = y_sorted[py * 8 + px]['id']
        if id > 23:
            z[py][px] = 0
        else:
            z[py][px] = ave[id]
x = np.arange(8)
y = np.arange(9)
x, y = np.meshgrid(x, y)
cmap = copy.copy(plt.get_cmap("jet"))
cmap.set_under('w', 1)  # 下限以下の色を設定
fig = plt.figure()
ax0 = plt.subplot(title='Target brightness')
z_ber0 = ax0.pcolormesh(x, y, z, cmap=cmap, vmax=20, vmin=10, edgecolors="black")
mylib.text(z, ax0, 'black')
divider0 = make_axes_locatable(ax0)  # axに紐付いたAxesDividerを取得
cax0 = divider0.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)
plt.show()
plt.clf()

x = np.arange(imager_num)
plt.plot(x, ave, '-x', c='r')
plt.xticks(x)
plt.xlabel('Imager ID')
plt.ylim(0, 20)
plt.grid()
plt.show()
