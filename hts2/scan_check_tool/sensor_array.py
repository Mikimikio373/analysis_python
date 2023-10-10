import json
import os
import sys
import numpy as np
import copy
import matplotlib.pyplot as plt
import math
import yaml

def text(array, ax):
    cmap = plt.get_cmap('tab10')
    for num_r, row in enumerate(array):
        for num_c, value in enumerate(array[num_r]):
            module = int(value.split('_')[0])
            ax.text(num_c, num_r, value, color=cmap(module), fontweight='bold', ha='center', va='center')


# sensor_exposureをたたいているコマンドから、scan_chech_toolの場所を特定
pythonpath = os.path.split(sys.argv[0])[0]
# sensorの場所情報を書いてあるフォルダを読み込み
with open(os.path.join(pythonpath, 'sensor_pos.yml'), 'rb') as f:
    y_load = yaml.safe_load(f)
y_sorted = sorted(y_load, key=lambda x: x['pos'])

cmap = copy.copy(plt.get_cmap("jet"))
cmap.set_under('w', 1) # 下限以下の色を設定
x = np.arange(8)
y = np.arange(9)
x, y = np.meshgrid(x, y)
z = np.zeros((9, 8))
sensor_name = []
for i in range(9):
    tmp = []
    for j in range(8):
        tmp.append([])
    sensor_name.append(tmp)

for py in range(9):
    for px in range(8):
        sensor_name[py][px] = '{}_{}_{}'.format(y_sorted[py*8+px]['module'], y_sorted[py*8+px]['sensor'], y_sorted[py*8+px]['id'])

fig = plt.figure(tight_layout=True)
fig.suptitle('sensor array', fontsize=20)
ax1 = plt.subplot()
z_ber = ax1.pcolormesh(x, y, z, cmap=cmap, vmax=10, vmin=1, edgecolors="black")
text(sensor_name, ax1)
ax1.set_aspect(1088/2024)
plt.show()
