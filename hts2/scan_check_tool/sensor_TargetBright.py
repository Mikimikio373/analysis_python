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
z_max = 256
z_min = 200


with open('sensor_pos.yml', 'rb') as f:
    y_load = yaml.safe_load(f)
y_sorted = sorted(y_load, key=lambda x: x['pos'])

TargetBright_param_path = 'X:/Project_v3/AdminParam/HTS2/SapEVMG/default.json'
with open(TargetBright_param_path, 'rb') as f:
    param = json.load(f)

brightlist = []
for i in range(len(param['ImagerControllerParamList'])):
    brightlist.append(param['ImagerControllerParamList'][i]['TargetBrightness'])

cmap = copy.copy(plt.get_cmap("jet"))
cmap.set_under('w', 1) # 下限以下の色を設定
x = np.arange(8)
y = np.arange(9)
x, y = np.meshgrid(x, y)
z = np.zeros((9, 8))
for py in range(9):
    for px in range(8):
        id = y_sorted[py*8+px]['id']
        if id >23:
            z[py][px] = 0
        else:
            z[py][px] = brightlist[id]

fig = plt.figure()
ax0 = plt.subplot(title='Target brightness')
z_ber0 = ax0.pcolormesh(x, y, z, cmap=cmap, vmax=z_max, vmin=z_min, edgecolors="black")
text(z, ax0, 'black')
divider0 = make_axes_locatable(ax0) #axに紐付いたAxesDividerを取得
cax0 = divider0.append_axes("right", size="5%", pad=0.1) #append_axesで新しいaxesを作成
pp0 = fig.colorbar(z_ber0, orientation="vertical", cax=cax0)

plt.show()