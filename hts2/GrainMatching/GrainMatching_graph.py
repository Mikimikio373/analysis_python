import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pn

# basepath = '../minus30'
basepath = os.getcwd()
savepath = 'plot'
npicture = 96
os.makedirs(os.path.join(basepath, savepath), exist_ok=True)
xrange = (-1.0, 1.0)
yrange = (-1.0, 1.0)
entryrange0 = (0, 100)
entryrange1 = (0, 500)
for i in range(0, 1):
    for j in range(i + 1, npicture):
        csv_path0 = os.path.join(basepath, 'dist_{:03}_{:03}.csv'.format(i, j))
        csv_input0 = pn.read_csv(csv_path0, header=0, dtype=float)
        distX0 = csv_input0['distX'].to_numpy(dtype=float)
        distY0 = csv_input0['distY'].to_numpy(dtype=float)

        fig = plt.figure(figsize=(9.6, 7.2), constrained_layout=True)

        settitle0 = 'pixel distance {:03} vs {:03}'.format(i, j)
        ax1 = fig.add_subplot(221, title=settitle0, xlim=xrange, ylim=yrange)
        ax1.scatter(distX0, distY0, s=5)

        # top right
        ax2 = fig.add_subplot(222, ylabel='distance y [pixel]', xlim=entryrange0)
        ax2.hist(distY0, range=yrange, bins=100, color='blue', orientation="horizontal")

        # bottom left
        ax3 = fig.add_subplot(223, xlabel='distance x [pixel]', ylim=entryrange0)
        ax3.hist(distX0, range=xrange, bins=100, color='red')

        figpath = os.path.join(basepath, savepath, 'dist_{:03}_{:03}.png'.format(i, j))
        fig.savefig(figpath, dpi=300)
        fig.clf()
        plt.close()

        print("{:03}_{:03} ended".format(i, j))






