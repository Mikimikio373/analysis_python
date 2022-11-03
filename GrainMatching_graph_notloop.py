import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pn
import matplotlib.cm as cm

basepath = '../GrainMatching_distX_100um'
savepath = 'fig'
os.makedirs(os.path.join(basepath, savepath), exist_ok=True)
xrange = (150, 165)
yrange = (-5, 5)
# xrange = None
# yrange = None
# entryrange0 = (0, 150)
# entryrange1 = (0, 500)
flg0 = os.path.join(basepath, savepath, 'flg0')
flg1 = os.path.join(basepath, savepath, 'flg1')
os.makedirs(flg0, exist_ok=True)
os.makedirs(flg1, exist_ok=True)

csv_path0 = os.path.join(basepath, 'dist_0001_0002_flg0.csv')
csv_path1 = os.path.join(basepath, 'dist_0001_0002_flg1.csv')
csv_input0 = pn.read_csv(csv_path0, header=0, dtype=float)
csv_input1 = pn.read_csv(csv_path1, header=0, dtype=float)
distX0 = csv_input0['distX'].to_numpy(dtype=float)
distY0 = csv_input0['distY'].to_numpy(dtype=float)
distX1 = csv_input1['distX'].to_numpy(dtype=float)
distY1 = csv_input1['distY'].to_numpy(dtype=float)

fig = plt.figure(figsize=(12, 9), tight_layout=True)

settitle0 = 'pixel distance VX1 vs VX2 size non 0'
settitle1 = 'pixel distance VX1 vs VX2 size 2'
binnumX = 150
binnumY = 100

ax1 = fig.add_subplot(221, title=settitle0)
H = ax1.hist2d(distX0, distY0, range=(xrange, yrange), bins=[binnumX, binnumY], cmap=cm.jet)
# fig.colorbar(H[3], ax=ax1)
# top right
ax2 = fig.add_subplot(222, ylabel='distance y [pixel]')
ax2.hist(distY0, range=yrange, bins=binnumY, color='blue', orientation="horizontal")

# bottom left
ax3 = fig.add_subplot(223, xlabel='distance x [pixel]')
ax3.hist(distX0, range=xrange, bins=binnumX, color='red')
figpath = os.path.join(basepath, savepath, 'dist_0001_0002.png')
fig.savefig(figpath, dpi=600)
fig.clf()

ax1 = fig.add_subplot(221, title=settitle0, xlim=xrange, ylim=yrange)
ax1.scatter(distX0, distY0, s=5)
# top right
ax2 = fig.add_subplot(222, ylabel='distance y [pixel]')
ax2.hist(distY0, range=yrange, bins=binnumY, color='blue', orientation="horizontal")

# bottom left
ax3 = fig.add_subplot(223, xlabel='distance x [pixel]')
ax3.hist(distX0, range=xrange, bins=binnumX, color='red')

figpath = os.path.join(flg0, 'dist_0001_0002.png')
fig.savefig(figpath, dpi=300)
fig.clf()

ax1 = fig.add_subplot(221, title=settitle1, xlim=xrange, ylim=yrange)
ax1.scatter(distX1, distY1, s=5)

# top right
ax2 = fig.add_subplot(222, ylabel='distance y [pixel]')
ax2.hist(distY1, range=yrange, bins=binnumY, color='blue', orientation="horizontal")

# bottom left
ax3 = fig.add_subplot(223, xlabel='distance x [pixel]')
ax3.hist(distX1, range=xrange, bins=binnumX, color='red')

figpath = os.path.join(flg1, 'dist_0001_0002.png')
fig.savefig(figpath, dpi=300)
fig.clf()







