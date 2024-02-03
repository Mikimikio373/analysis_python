import os.path
import sys
from statistics import mean, stdev
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages


def bins2x(bins: list):
    out = []
    for i in range(len(bins) - 1):
        out.append((bins[i] + bins[i+1]) / 2)
    return out


def gaus_const(x, a, mu, sigma, c):
    return a * np.exp(-(x-mu)**2/(2*sigma**2)) + c

imager_list1 = []
for i in range(12, 24):
    imager_list1.append(i)
for i in range(9):
    if i < 3:
        imager_list1.append(i+8)
    elif i < 6:
        imager_list1.append(i+1)
    else:
        imager_list1.append(i-6)
imager_list2 = []
for i in range(12):
    if i < 4:
        imager_list2.append(i+8)
    elif i < 8:
        imager_list2.append(i)
    else:
        imager_list2.append(i-8)
for i in range(13, 24):
    if i%4==0:
        continue
    imager_list2.append(i)
print(imager_list1)
print(imager_list2)
print(len(imager_list1), len(imager_list2))


basepath = 'A:/Test/check_FASER/m222-pl002_30cm-1/TrackMatching/overlap'
pdf = PdfPages(os.path.join(basepath, 'fit.pdf'))
plot_range = 2

for imager1, imager2 in zip(imager_list1, imager_list2):
    print(imager1, imager2)
    csv = os.path.join(basepath, 'v5000-i{}_v5000-i{}.csv'.format(imager1, imager2))
    df = pd.read_csv(csv)



    dx = df['dx/D'].values*1000
    height, x, ret = plt.hist(dx, bins=50, range=(-plot_range, plot_range), color='r', lw=1, ec='black', histtype='stepfilled')
    initial = [max(height), 0, 0.15, 0]
    popt, pcov = curve_fit(gaus_const, bins2x(x), height, p0=initial, maxfev=20000)
    fitting = gaus_const(np.linspace(-plot_range, plot_range, 200), popt[0], popt[1], popt[2], popt[3])
    plt.plot(np.linspace(-plot_range, plot_range, 200), fitting, '-', color=('k'))
    text = 'Entries: {:d}\nMean: {:.4g}\nStd Dev: {:.4g}\nHeight: {:.4g}\nCenter: {:.4}\nsigma: {:.4g}\nconst.: {:g}'.format(int(np.sum(height)), mean(dx), stdev(dx), popt[0], popt[1], popt[2], popt[3])
    plt.text(plot_range*0.7, max(height)*0.8, text, bbox=(dict(boxstyle='square', fc='w')))
    plt.xlabel('dx [um]')
    plt.title('i{}-i{}'.format(imager1, imager2))
    pdf.savefig()
    plt.clf()

    dy = df['dy/D'].values*1000
    height, x, ret = plt.hist(dy, bins=50, range=(-plot_range, plot_range), color='b', lw=1, ec='black', histtype='stepfilled')
    initial = [max(height), 0, 0.15, 0]
    popt, pcov = curve_fit(gaus_const, bins2x(x), height, p0=initial, maxfev=20000)
    fitting = gaus_const(np.linspace(-plot_range, plot_range, 200), popt[0], popt[1], popt[2], popt[3])
    plt.plot(np.linspace(-plot_range, plot_range, 200), fitting, '-', color=('k'))
    text = 'Entries: {:d}\nMean: {:.4g}\nStd Dev: {:.4g}\nHeight: {:.4g}\nCenter: {:.4}\nsigma: {:.4g}\nconst.: {:g}'.format(int(np.sum(height)), mean(dx), stdev(dx), popt[0], popt[1], popt[2], popt[3])
    plt.text(plot_range*0.7, max(height)*0.8, text, bbox=(dict(boxstyle='square', fc='w')))
    plt.xlabel('dy [um]')
    plt.title('i{}-i{}'.format(imager1, imager2))
    pdf.savefig()
    plt.clf()
# plt.show()


pdf.close()
