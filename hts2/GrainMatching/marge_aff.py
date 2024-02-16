import math
import os.path
import sys
import  copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

basepath = 'Q:/minami/affine_param'
shrink_all = []
shrink_x = []
shrink_y = []
rotation = []
shrink_err = []
rotation_err = []
id = np.arange(1, 25, 1)

for i in range(12):
    tar_dir = os.path.join(basepath, '{}-{:02}_aff.csv'.format(0, 4 * math.floor(i / 4) + 3 - (i % 4)))
    df = pd.read_csv(tar_dir)
    shrink_x.append(abs(df['a'][0])*1000)
    shrink_y.append(abs(df['d'][0])*1000)
    shrink = (abs(df['a'][0]) + abs(df['d'][0]))/2
    # cの符合で符合を決定
    rot = (abs(df['b'][0]) / shrink + abs(df['c'][0]) / shrink) / 2 * (df['c'][0] / abs(df['c'][0]))
    ad_error = (abs(df['a_err'][0]) + abs(df['d_err'][0])) / 2
    bc_error = (abs(df['b_err'][0]) + abs(df['c_err'][0])) / 2
    rot_err = rot * math.sqrt((ad_error / shrink) ** 2 + (bc_error / ((abs(df['b'][0]) + abs(df['c'][0])) / 2)) ** 2)
    shrink_all.append(shrink*1000)
    shrink_err.append(abs(ad_error)*1000)
    rotation.append(rot*1000)
    rotation_err.append(abs(rot_err)*1000)

    tar_dir = os.path.join(basepath, '{}-{:02}_aff.csv'.format(1, 11 - i))
    df = pd.read_csv(tar_dir)
    shrink = (abs(df['a'][0]) + abs(df['d'][0])) / 2
    shrink_x.append(abs(df['a'][0]) * 1000)
    shrink_y.append(abs(df['d'][0]) * 1000)
    # cの符合で符合を決定
    rot = (abs(df['b'][0]) / shrink + abs(df['c'][0]) / shrink) / 2 * (df['c'][0] / abs(df['c'][0]))
    ad_error = (abs(df['a_err'][0]) + abs(df['d_err'][0])) / 2
    bc_error = (abs(df['b_err'][0]) + abs(df['c_err'][0])) / 2
    rot_err = rot * math.sqrt((ad_error / shrink) ** 2 + (bc_error / ((abs(df['b'][0]) + abs(df['c'][0])) / 2)) ** 2)
    shrink_all.append(shrink * 1000)
    shrink_err.append(abs(ad_error) * 1000)
    rotation.append(rot * 1000)
    rotation_err.append(abs(rot_err) * 1000)


for i in range(3):
    x = np.arange(1, 9)
    plt.plot(x, shrink_x[i*8:i*8+8], 'x', label='line:{}'.format(i+1))
    plt.xticks(x)
plt.legend()
plt.grid()
# plt.savefig(os.path.join(basepath, 'shrink_x.png'), dpi=300)
plt.clf()

for i in range(8):
    line_y = []
    for j in range(3):
        line_y.append(shrink_y[i+j*8])
    y = np.arange(1, 4)
    plt.plot(y, line_y, 'x', label='line:{}'.format(i + 1))
    plt.xticks(y)
plt.legend()
plt.grid()
# plt.savefig(os.path.join(basepath, 'shrink_y.png'), dpi=300)

plt.errorbar(id, rotation, yerr=rotation_err, marker='x', linestyle='None')
plt.xticks(np.arange(1, 25))
plt.yticks(np.arange(-6, 7))
plt.xlabel('sensor ID')
plt.ylabel('回転量 [mrad]', fontname='MS Gothic')
plt.grid()
# plt.savefig(os.path.join(basepath, 'rotation_all.png'), dpi=300)
plt.clf()

#要汎用化
x = np.arange(1, 9)
y = np.arange(1, 10)
x, y = np.meshgrid(x, y)
z = np.zeros((9, 8))
cmap = copy.copy(plt.get_cmap("rainbow"))
cmap.set_under('w', 1) # 下限以下の色を設定
base_shrink_x = shrink_x[3+8*1]
base_shrink_y = shrink_y[3+8*1]
base_shrink = math.sqrt(shrink_x[11]**2 + shrink_y[11]**2)
for i in range(8):
    for j in range(9):
        if j % 3 == 2:
            z[j][i] = math.sqrt(shrink_x[i+8*math.floor(j/3)]**2 + shrink_y[i+8*math.floor(j/3)]**2) / base_shrink
            # z[j][i] = shrink_y[i + 8 * math.floor(j / 3)] / base_shrink_y
            # print(shrink_x[i + 8 * math.floor(j / 3)] / base_shrink_x)
z_ber = plt.pcolormesh(x, y, z, cmap=cmap, vmin=0.998, vmax=1.0, edgecolors="black")
# z_ber = plt.pcolormesh(x, y, z, cmap=cmap, vmin=0.6306, vmax=0.6324, edgecolors="black")
pp = plt.colorbar(z_ber, orientation="vertical")
# plt.axis([0, 8, 0, 9])
# plt.axes().set_aspect(2)
plt.show()
plt.clf()


for i in range(3):
    x = np.arange(1, 9)
    plt.errorbar(x, rotation[i*8:i*8+8], yerr=rotation_err[i*8:i*8+8], marker='x', linestyle='None')
    plt.xticks(np.arange(1, 9))
    plt.yticks(np.arange(-6, 7))
    # plt.xlabel('sensor ID')
    # plt.ylabel('回転量 [mrad]', fontname='MS Gothic')
plt.grid()
# plt.savefig(os.path.join(basepath, 'rotation_line.png'), dpi=300)
plt.clf()

rotation_module = []
for i in range(2):
    for j in range(12):
        rotation_module.append(rotation[j*2+i])
x = np.arange(1, 25)
plt.plot(x, rotation_module, 'x')
plt.xticks(x)
plt.yticks(np.arange(-6, 7))
plt.grid()
# plt.show()
