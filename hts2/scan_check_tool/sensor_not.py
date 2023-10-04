import math
import os
import sys
import statistics
import json
import numpy as np
import matplotlib.pyplot as plt

step_x = 9.0
step_y = 4.95

if not len(sys.argv) == 2:
    sys.exit('please enter \"target path\"')

basepath = sys.argv[1]

out_path = os.path.join(basepath, 'GRAPH')
if not os.path.exists(out_path):
    os.makedirs(out_path)

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

fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)

ax1 = fig.add_subplot(221)
ax1.scatter(x, not_average_L0, marker='x')
ax1.set_title('L0 NOT (absolute)')
ax1.set_xticks(x)
ax1.set_ylim(0, 10000)
ax1.grid()

ax2 = fig.add_subplot(222)
ax2.scatter(x, not_average_L1, marker='x')
ax2.set_title('L1 NOT (absolute)')
ax2.set_xticks(x)
ax2.set_ylim(0, 10000)
ax2.grid()

ax1 = fig.add_subplot(223)
ax1.scatter(x, not_average_L0_relative, marker='x')
ax1.set_title('L0 NOT (relative)')
ax1.set_xticks(x)
ax1.set_ylim(0.7, 1)
ax1.grid()

ax2 = fig.add_subplot(224)
ax2.scatter(x, not_average_L1_relative, marker='x')
ax2.set_title('L1 NOT (relative)')
ax2.set_xticks(x)
ax2.set_ylim(0.7, 1)
ax2.grid()

plt.savefig(os.path.join(out_path, 'check_not.png'), dpi=300)
