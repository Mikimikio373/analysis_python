import os.path
import sys
from statistics import mean, stdev
import pandas as pd
import matplotlib.pyplot as plt

# path = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-0.03/tracking_ph7/entries.csv'
# path = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-0.015_dilate/tracking_ph7/entries.csv'
# path = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-0.0075_dilate_1.4/tracking_ph7/entries.csv'
# path = 'Q:/minami/20231205_rand_grain2023/graine2023_thr11-10_cubic/tracking_ph7/entries.csv'
path = 'Q:/minami/20231205_rand_grain2023/graine2023_noncubic_freq0.1_z0.3-thr14_13/tracking_ph7/entries.csv'
basepath, filename = os.path.split(path)
filename = filename.split('.')[0]
# index = 'Entries'
index = 'vphcut1'

df = pd.read_csv(path)

# print(df)

entries = len(df[index])
ave = mean(df[index])
std_dev = stdev(df[index])
histreturn = plt.hist(df[index], bins=100, histtype='stepfilled',
             facecolor='yellow',
             linewidth=1, edgecolor='black')
# histreturn = plt.hist(df[index], bins=100, histtype='stepfilled', range=(ave-70000, ave+70000),
#              facecolor='yellow',
#              linewidth=1, edgecolor='black')

factor = 0.95

text = 'Entries: {:d}\nMean: {:4g}\nStd_dev: {:4g}'.format(entries, ave, std_dev)
plt.text(max(histreturn[1]) * factor, max(histreturn[0]) * factor, text, bbox=(dict(boxstyle='square', fc='w')))
# plt.show()
outpaht = basepath + '/' + filename + '_' + index + '.png'
plt.savefig(outpaht, dpi=300)
