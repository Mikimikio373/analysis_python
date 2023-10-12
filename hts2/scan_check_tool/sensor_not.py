import math
import os
import sys
import statistics
import json
import numpy as np
import matplotlib.pyplot as plt
import yaml
import copy

step_x = 9.0
step_y = 4.95
absolute_max = 20000
relative_min = 0.7
def text(array: np.ndarray, ax, color: str):
    for num_r, row in enumerate(array):
        for num_c, value in enumerate(array[num_r]):
            ax.text(num_c, num_r, '{:.2f}'.format(value), color=color, ha='center', va='center')


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

sideX = sap_json['SideX']
step_x_num = math.ceil(sideX / step_x)

module_num = 2
sensor_num = 12
not_average_L0 = []
not_average_L1 = []
for module in range(module_num):
    for sensor in range(sensor_num):
        not_tmp_L0 = []
        not_tmp_L1 = []
        nottxt_path = os.path.join(basepath, 'DATA', '{:02}_{:02}'.format(module, sensor), 'TrackHit2_0_99999999_0_000.txt')
        if not os.path.exists(nottxt_path):
            sys.exit('there is no file: {}'.format(nottxt_path))

        f = open(nottxt_path, 'r')
        data_line = f.readlines()
        for i in range(len(data_line)):
            # L0, L1の判断
            if i % (step_x_num * 2) < step_x_num:   #L0側
                not_tmp_L0.append(int(data_line[i].split(' ')[-2]))
            else:
                not_tmp_L1.append(int(data_line[i].split(' ')[-2]))
        not_average_L0.append(statistics.mean(not_tmp_L0))
        not_average_L1.append(statistics.mean(not_tmp_L1))


x = range(1, module_num*sensor_num + 1)
max_not_L0 = max(not_average_L0)
max_not_L1 = max(not_average_L1)
not_average_L0_relative = np.asarray(not_average_L0) / max_not_L0
not_average_L1_relative = np.asarray(not_average_L1) / max_not_L1

cmap = copy.copy(plt.get_cmap("copper"))
cmap.set_under('w', 1)  # 下限以下の色を設定

z0 = np.zeros((9, 8))
z1 = np.zeros((9, 8))
for py in range(9):
    for px in range(8):
        id = y_sorted[py*8+px]['id']
        if id >23:
            z0[py][px] = 0
            z1[py][px] = 0
        else:
            z0[py][px] = not_average_L0_relative[id]
            z1[py][px] = not_average_L1_relative[id]

fig = plt.figure(figsize=(8.27*1.3, 11.69*1.3), tight_layout=True)
x = np.arange(24)
ax1 = fig.add_subplot(321)
ax1.plot(x, not_average_L0, marker='x', c='r')
ax1.set_title('L0 NOT (absolute)')
ax1.set_xticks(x)
ax1.set_xlabel('Imager ID')
ax1.set_ylim(0, absolute_max)
ax1.grid()

ax2 = fig.add_subplot(322)
ax2.plot(x, not_average_L1, marker='x', c='b')
ax2.set_title('L1 NOT (absolute)')
ax2.set_xticks(x)
ax2.set_xlabel('Imager ID')
ax2.set_ylim(0, absolute_max)
ax2.grid()

x = np.arange(8)
y = np.arange(9)
x, y = np.meshgrid(x, y)
ax3 = plt.subplot(323, title='L0 NOT (relative, sensor array)')
z_ber0 = ax3.pcolormesh(x, y, z0, cmap=cmap, vmax=1, vmin=relative_min, edgecolors="black")
text(z0, ax3, 'black')
pp0 = fig.colorbar(z_ber0, orientation="vertical")
ax3.set_aspect(1088/2024)

ax4 = plt.subplot(324, title='L1 NOT (relative, sensor array)')
z_ber1 = ax4.pcolormesh(x, y, z1, cmap=cmap, vmax=1, vmin=relative_min, edgecolors="black")
text(z1, ax4, 'black')
pp1 = fig.colorbar(z_ber1, orientation="vertical")
ax4.set_aspect(1088/2024)

x = np.arange(24)
ax5 = fig.add_subplot(325)
ax5.plot(x, not_average_L0_relative, marker='x', c='r', label='L0 NOT (relative)')
ax5.plot(x, not_average_L1_relative, marker='x', c='b', label='L1 NOT (relative)')
ax5.set_title('NOT (relative)')
ax5.set_xticks(x)
ax5.set_xlabel('Imager ID')
ax5.set_ylim(relative_min, 1)
ax5.legend()
ax5.grid()

# plt.show()
plt.savefig(os.path.join(out_path, 'sensor_not.png'), dpi=300)
