import os.path
import pandas as pn
import cv2
import numpy as np
from matplotlib import pyplot as plt

basepath = 'R:\\minami\\20221228_aff'
bright_all = []
num = []
fit = []
entries = []
a = []
b = []
c = []
d = []
for i in range(0, 2):
    for j in range(1, 13):
        areapath = os.path.join(basepath, 'Module{}'.format(i), 'sensor-{}'.format(j))
        imgpath = os.path.join(areapath, 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_4_0.png')
        img = cv2.imread(imgpath, 0)
        bright_all.append(img.mean())
        csvpath = os.path.join(areapath, 'GrainMatching_loop', 'centerVX0000_VY0000_0_stats.csv')
        data = pn.read_csv(csvpath, header=0)
        print(len(data))
        num.append(len(data))
        fitcsvpath = os.path.join(areapath, 'aff_data.csv')
        data_fit = pn.read_csv(fitcsvpath)
        fit.append(data_fit["cut2"].values)
        aff_path = os.path.join(areapath, 'aff_data.csv')
        aff_pn = pn.read_csv(aff_path)
        entries.append(aff_pn['cut2'][0])
        a.append(aff_pn['a'][0])
        b.append(aff_pn['b'][0])
        c.append(aff_pn['c'][0])
        d.append(aff_pn['d'][0])

# plt.scatter(bright_all, num, marker='o', color='none', edgecolor="r")
# plt.title('brightness vx nog')
# plt.xlabel('brightness mean')
# plt.ylabel('number of hit grains')
# plt.show()

# plt.scatter(num, fit, marker='o', color='none', edgecolor="r")
# plt.title('nog vx fitting point')
# plt.xlabel('number of hit grains')
# plt.ylabel('number of fitting point')
# plt.show()

aff_data = pn.DataFrame()
aff_data['cut2'] = entries
aff_data['a'] = a
aff_data['b'] = b
aff_data['c'] = c
aff_data['d'] = d
aff_data.to_csv(os.path.join(basepath, 'aff_all.csv'))