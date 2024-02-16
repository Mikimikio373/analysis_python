import math
import os
import copy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib.cm as cm


def rms(rms_list: list):
    square = [i**2 for i in rms_list]
    return math.sqrt(sum(square))


basepath = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8'
out_path = 'B:/data/powerpoint/master_presen/fig/eff-not_micro'
area = 3.0 * 2.4

width_list = [2252, 2458, 2662, 2896, 3072]
height_list = [1196, 1306, 1414, 1538, 1632]
thr_s_list = [10, 10, 10, 9, 9]
thr_e_list = [12, 12, 12, 11, 11]
maker_styles = ['o', 'v', '^', 's', 'x']


# width_list = [2252]
# height_list = [1196]
# thr_s_list = [9]
# thr_e_list = [13]

# resizeのデータ取得
enties = []
eff = []
eff_err = []
for i in range(len(width_list)):
    enties.append([])
    eff.append([])
    eff_err.append([])

for n, (width, height, thr_s, thr_e) in enumerate(zip(width_list, height_list, thr_s_list, thr_e_list)):
    dirname = 'cubic_{}-{}'.format(width, height)

    # basepathへ移動
    os.chdir(basepath)
    # current_dir = os.getcwd()
    # print('current directory: {}'.format(current_dir))


    for i in range(thr_s, thr_e + 1):
        os.chdir(os.path.join(basepath, dirname))
        # current_dir = os.getcwd()
        # print('current directory: {}'.format(current_dir))

        # pl088に移動
        thr_name = '{}{}'.format(i, i - 1)
        os.chdir(os.path.join(thr_name, 'area1', 'PL088'))
        # current_dir = os.getcwd()
        # print('current directory: {}'.format(current_dir))

        # csvファイルの読み取り
        eff_csv = 'eff_data.csv'
        eff_data = pd.read_csv(eff_csv, header=None)
        eff[n].append(np.average(eff_data[0][0:10].values))
        eff_err[n].append(rms(eff_data[1][0:10].values))

        # txtからentriesの読み取り
        txt1 = 'f0881_entries.txt'
        txt2 = 'f0882_entries.txt'
        enties_data1 = pd.read_csv(txt1, header=None)
        enties_data2 = pd.read_csv(txt2, header=None)
        density = (enties_data1[0][0] + enties_data2[0][0]) / (2 * area)
        enties[n].append(density)

# 画素補間なしのデータ取得
enties_non = []
eff_non = []
eff_err_non = []
dirname = 'noncubic'

# basepathへ移動
os.chdir(basepath)
# current_dir = os.getcwd()
# print('current directory: {}'.format(current_dir))

non_vphcut_microtrack = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/ph7_noncubic'

for i in range(13, 17):
    os.chdir(os.path.join(basepath, dirname))
    # current_dir = os.getcwd()
    # print('current directory: {}'.format(current_dir))

    # pl088に移動
    thr_name = '{}{}ph7_vph2'.format(i, i - 1)
    os.chdir(os.path.join(thr_name, 'area1', 'PL088'))
    # current_dir = os.getcwd()
    # print('current directory: {}'.format(current_dir))

    # csvファイルの読み取り
    eff_csv = 'eff_data.csv'
    eff_data = pd.read_csv(eff_csv, header=None)
    eff_non.append(np.average(eff_data[0][0:10].values))
    eff_err_non.append(rms(eff_data[1][0:10].values))

    # txtからentriesの読み取り
    txt1 = os.path.join(non_vphcut_microtrack, 'tracking{}_{}_zfilt-0.30_180_5_6_0'.format(i, i-1), 'mt2f', 'f0881_clust_entries.txt')
    txt2 = os.path.join(non_vphcut_microtrack, 'tracking{}_{}_zfilt-0.30_180_5_6_0'.format(i, i-1), 'mt2f', 'f0882_clust_entries.txt')
    enties_data1 = pd.read_csv(txt1, header=None)
    enties_data2 = pd.read_csv(txt2, header=None)
    density = (enties_data1[0][0] + enties_data2[0][0]) / (2 * area)
    enties_non.append(density)


# plot
cmap = copy.copy(plt.get_cmap("jet"))
size_list = [0.63, 0.57, 0.53, 0.48, 0.45, 0.42]
z_max = 0.65
z_min = 0.4
z_range = z_max - z_min
pixelsize_ori = 0.63
fig = plt.figure(tight_layout=True)
ax = fig.add_subplot(111)
# ax.errorbar(484254, 0.977407, yerr=0.00197, c=cm.tab10(0), lw=1.2, marker='p', mfc='None', ms=8, mew=1.2, label='HTS (GRAINE2018)')
ax.errorbar(enties_non, eff_non, yerr=eff_err_non, c=cmap((0.63 - z_min) / z_range), lw=1.2, marker='d', mfc='None', ms=8, mew=1.2, label=r'pixel size: 0.63 [$\mu$m]')
for i in range(len(enties)):
# for i in range(3, 4):
    ax.errorbar(enties[i], eff[i], yerr=eff_err[i], c=cmap((size_list[i+1] - z_min) / z_range), lw=1.2, marker=maker_styles[i], mfc='None', ms=8, mew=1.2, label=r'pixel size: {} [$\mu$m]'.format(size_list[i+1]))

ax.set_xlim(0, 2000000)
ax.set_ylim(0.9, 1.0)
ax.set_yticks(np.arange(0.9, 1.0001, 0.01))
ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(style="sci",  axis="x", scilimits=(5, 5))
ax.yaxis.offsetText.set_fontsize(15)
# ax.set_xlabel('micro track density [/cm^2]', fontsize=15)
# ax.set_ylabel('efficiency (base track)', fontsize=15)
plt.tick_params(labelsize=15)
plt.legend(fontsize=10, loc='lower right')
bar = ax.scatter(size_list, size_list, c=size_list, cmap=cmap, vmin=z_min, vmax=z_max)
plt.colorbar(bar)
plt.grid()
# plt.show()
plt.savefig(os.path.join(out_path, 'eff-not_micro_color.png'), dpi=300)
