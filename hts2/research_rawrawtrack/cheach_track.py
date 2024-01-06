import os
import csv
import statistics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def ssv2csv(filename: str):
    print(filename + ' open')
    outname = os.path.splitext(filename)[0] + '.csv'
    with open(filename, 'r') as i, open(outname, 'w') as o:
        reader = csv.reader(i, delimiter=' ', skipinitialspace=True)
        writer = csv.writer(o)
        writer.writerows(reader)
    print(outname + ' written')
    return outname


def plot_ref(ax, x, y, guide, width):
    ax.quiver(x, y, guide * factor, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=width)
    ax.quiver(x, y, 0, guide * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=width)
    ax.text(x, y, f" {guide} tanθ", va="bottom", ha="left")


def plot_vec(pdf, ax, rawtrack: pd.DataFrame, ref_track: list, *, factor: float = 10, width: float = 0.05,
             alpha: float = 0.3):
    ax.quiver(rawtrack['x'], rawtrack['y'], rawtrack['ax'] * factor, rawtrack['ay'] * factor, angles='xy',
              scale_units='xy', scale=1, units='xy', width=width, alpha=alpha)
    ax.quiver(ref_track[2], ref_track[3], ref_track[0] * factor, ref_track[1] * factor, color='r', angles='xy',
              scale_units='xy', scale=1, units='xy', width=width)
    ax.set_aspect(1)

    refpos_x = ref_track[2] - 5 + 10 * 0.05
    refpos_y = ref_track[3] - 5 + 10 * 0.05
    plot_ref(ax, refpos_x, refpos_y, guide, width)
    ax.set_xlim(ref_track[2] - 5, ref_track[2] + 5)
    ax.set_ylim(ref_track[3] - 5, ref_track[3] + 5)
    ax.set_xlabel("Stage X [um]", fontsize=16)
    ax.set_ylabel("Stage Y [um]", fontsize=16)
    pdf.savefig()
    plt.clf()


def plot_dhist(pdf, X: list, Xrange: float, factorX: float, factorY: float, xlabel: str, *, color='y'):
    hist_return = plt.hist(X, bins=100, range=(-Xrange, Xrange), histtype='stepfilled', color=color, lw=1, ec='black')
    plt.xlabel(xlabel)
    entries = sum(-Xrange < v < Xrange for v in X)
    mean = statistics.mean(X)
    std_dev = statistics.stdev(X)
    under = sum(v < -Xrange for v in X)
    over = sum(v > Xrange for v in X)
    text = 'Entries: {:d}\nMean: {:4g}\nStd_dev: {:4g}\nUnderflow: {:d}\nOverflow: {:d}'.format(entries, mean, std_dev,
                                                                                                under, over)
    plt.text(Xrange * factorX, max(hist_return[0]) * factorY, text, bbox=(dict(boxstyle='square', fc='w')))
    pdf.savefig()
    plt.clf()


factor = 1
guide = 1
width = 0.05
alpha = 0.3

fname_ori = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/tracking_cubic10_9_zfilt-0.40_180_0_0/mt2f/test2.txt'
fname_text = os.path.splitext(fname_ori)[0]
out_path = os.path.dirname(fname_ori)
fname = ssv2csv(fname_ori)

header_fvxxdump = ['pos', 'zone', 'rawid', 'isg', 'ph', 'ax', 'ay', 'x', 'y', 'z', 'z1', 'z2', 'px', 'py', 'col', 'row',
                   'f']
df = pd.read_csv(fname, header=None)
df = df.rename(columns={'0': 'pos'})
dict_fvxxdump = dict()
for i in range(len(header_fvxxdump)):
    dict_fvxxdump[i] = header_fvxxdump[i]
df = df.rename(columns=dict_fvxxdump)
# ref_track = [0.0229, 0.0206, 9143.4, 57.3]
ref_track = [-0.1215, 0.7470, 9956.9, -164.3]

outpdf = PdfPages(fname_text + '.pdf')

fig = plt.figure()
ax = fig.add_subplot(111)
plot_vec(outpdf, ax, df, ref_track, factor=factor, width=width, alpha=alpha)

Xrange = 5
factorX = 0.7
factorY = 0.9
X = df['x'] - ref_track[2]
plot_dhist(outpdf, X, Xrange, factorX, factorY, 'dx [um]', color='r')
Y = df['y'] - ref_track[3]
plot_dhist(outpdf, Y, Xrange, factorX, factorY, 'dy [um]', color='b')

Xrange = 0.3
dax = df['ax'] - ref_track[0]
plot_dhist(outpdf, dax, Xrange, factorX, factorY, 'dax (tanθ)', color='r')
day = df['ay'] - ref_track[1]
plot_dhist(outpdf, day, Xrange, factorX, factorY, 'day (tanθ)', color='b')


outpdf.close()
