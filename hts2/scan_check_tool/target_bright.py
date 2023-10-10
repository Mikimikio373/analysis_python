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
            ax.text(num_c, num_r, int(value), color=color, ha='center', va='center')


if not len(sys.argv) == 2:
    sys.exit('please enter \"target path\"')

target_path = sys.argv[1]

# sensor_exposureをたたいているコマンドから、scan_chech_toolの場所を特定
pythonpath = os.path.split(sys.argv[0])[0]
# sensorの場所情報を書いてあるフォルダを読み込み
with open(os.path.join(pythonpath, 'sensor_pos.yml'), 'rb') as f:
    y_load = yaml.safe_load(f)
y_sorted = sorted(y_load, key=lambda x: x['pos'])


with open(os.path.join(target_path, 'PARAMS', 'UserParam.json'), 'rb') as f:
    user_param = json.load(f)
EVMG_path = user_param['OtherPathParam']['ImagerControllerParamFilePath']
with open(EVMG_path, 'rb') as f:
    EVMG_param = json.load(f)

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
            z[py][px] = EVMG_param['ImagerControllerParamList'][id]['TargetBrightness']

fig = plt.figure(figsize=(8.27/1.5, 11.69/1.5), tight_layout=True)
fig.suptitle('target brightness')
ax1 = plt.subplot(211)
z_ber = ax1.pcolormesh(x, y, z, cmap=cmap, vmax=240, vmin=200, edgecolors="black")
text(z, ax1, 'black')
pp = fig.colorbar(z_ber, orientation="vertical")
ax1.set_aspect(1088/2024)

ax2 = plt.subplot(212)
x = np.arange(24)
y = []
for i in range(24):
    y.append(EVMG_param['ImagerControllerParamList'][i]['TargetBrightness'])
ax2.plot(x, y, marker='x', c='black')
ax2.set_ylim(200, 240)
ax2.set_xticks(x)
ax2.grid()
plt.savefig(os.path.join(target_path, 'GRAPH', 'target_bright.pdf'))