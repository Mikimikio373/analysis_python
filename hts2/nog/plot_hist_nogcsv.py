import os.path
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def textbox(ax, flat_list, ax_x_max, ax_y_max, *, factor: float = 0.9):
    entries = len(flat_list)
    mean = np.mean(flat_list)
    std_dev = np.std(flat_list)

    text = 'Entries: {:d}\nMean: {:4g}\nStd_dev: {:4g}'.format(entries, mean, std_dev)
    ax.text(ax_x_max * factor, ax_y_max * factor, text, bbox=(dict(boxstyle='square', fc='w')))

# basepath = 'Q:/minami/20220429_suganami/006/IMAGE00_AREA-1/png_thr_dilate/png_thr10_9'
# basepath = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_dilate/png_thr10_9'

if not len(sys.argv) == 2:
    sys.exit('command line error. please input [basepath]')
basepath = sys.argv[1]

pd_path = os.path.join(basepath, 'nog_list.csv')
if not os.path.exists(pd_path):
    sys.exit('There in no file: {}'.format(pd_path))
df = pd.read_csv(pd_path)

for header in ['L0', 'L1', 'obj_L0', 'obj_L1']:
    mean = np.mean(df[header])
    dev = np.std(df[header])
    x_max = mean + 20000
    x_min = mean - 20000
    fig = plt.figure()
    ax = fig.add_subplot(111)
    histreturn = ax.hist(df[header], bins=100, histtype='stepfilled', facecolor='yellow', linewidth=1, edgecolor='black', range=(x_min, x_max))
    textbox(ax, df[header], x_max, max(histreturn[0]), factor=0.95)
    plt.savefig(os.path.join(basepath, 'nog_list_{}.png'.format(header)), dpi=300)
    plt.clf()
