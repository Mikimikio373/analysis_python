import os.path
import sys

import matplotlib.pyplot as plt
import numpy as np

basepath = 'R:/minami/HTS1_GRAINE2018_accuracy/accuracy_a5_B18-03_unit1'

radial_list = []
lateral_list = []
for i in range(13):
    radial_list.append([])
    lateral_list.append([])
for pl in range(50, 98):
    tarfile = os.path.join(basepath, '{:03}-{:03}'.format(pl, pl + 1), 'accdata_RL.dat')

    with open(tarfile, 'r') as f:
        txt = f.readlines()
    for i in range(2, len(txt)):
        line = txt[i][:-1].split(' ')
        radial_list[i-2].append(float(line[1]))
        lateral_list[i-2].append(float(line[2]))

print(len(radial_list[0]))
radial1 = []
lateral1 = []
for i in range(len(radial_list)):
    radial1.append(np.average(radial_list[i]))
    lateral1.append((np.average(lateral_list[i])))

print(radial1)
print(lateral1)
# sys.exit()


hts2file = 'R:/minami/HTS1_GRAINE2018_accuracy/accdata_RL_hts2.dat'
with open(hts2file, 'r') as f:
    txt = f.readlines()
x2 = []
radial2 = []
lateral2 = []
for i in range(2, len(txt)):
    line = txt[i][:-1].split(' ')
    x2.append(float(line[0]))
    radial2.append(float(line[1]))
    lateral2.append(float(line[2]))

plt.figure(tight_layout=True)
plt.plot(x2, radial1, marker='o', mfc='None', ms=8, label='GRAINE2018(HTS) radial', linestyle="None")
plt.plot(x2, lateral1, marker='s', mfc='None', ms=8, label='GRAINE2018(HTS) lateral', linestyle="None")

plt.plot(x2, radial2, marker='^', mfc='None', ms=8, label='GRAINE2023(HTS-2) radial', linestyle="None")
plt.plot(x2, lateral2, marker='v', mfc='None', ms=8, label='GRAINE2023(HTS-2) lateral', linestyle="None")
plt.title('Angler diffarence', fontsize=20)
plt.legend()
plt.grid()
plt.xlabel(r'track angle (tan$\theta$)', loc='right', fontsize=16)
plt.ylabel(r'$\sigma$($\delta$tan$\theta$)', fontsize=16)
plt.xticks(np.arange(0.0, 1.31, 0.1), fontsize=14)
plt.yticks(np.arange(0.0, 0.04, 0.005), fontsize=14)

outpath = 'B:/data/powerpoint/HTS2_data/4master_theisis/dRL_plot.png'
plt.savefig(outpath, dpi=300)
plt.clf()

rate_radial = np.array(radial2) / np.array(radial1)
rata_lateral = np.array(lateral2) / np.array(lateral1)
plt.plot(x2, rate_radial, marker='x', mfc='None', ms=8, label='radial_ratio (HTS2/HTS1)', linestyle="None")
plt.plot(x2, rata_lateral, marker='d', mfc='None', ms=8, label='lateral_rario (HTS2/HTS1)', linestyle="None")
plt.xlabel(r'track angle (tan$\theta$)', loc='right', fontsize=16)
plt.ylabel('accuracy ratio', fontsize=16)
plt.grid()
plt.legend()
outpath = 'B:/data/powerpoint/HTS2_data/4master_theisis/dRL-ratio_plot.png'
plt.savefig(outpath, dpi=300)
# plt.show()
