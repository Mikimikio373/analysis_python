import os
import cv2
import sys
import yaml
import numpy as np
from matplotlib import pyplot as plt
import json
import pandas as pd

if len(sys.argv) == 2:
    basepath = sys.argv[1]
    starskip = 0
    endskip = 0
elif len(sys.argv) == 4:
    basepath = sys.argv[1]
    starskip = int(sys.argv[2])
    endskip = int(sys.argv[3])
else:
    sys.exit('use error. please input \"basepath\", (\"start skip num\", \"end skip num\")')


if not os.path.exists(basepath):
    exit('there is no directory: {}'.format(basepath))

print('calc for: {}'.format(basepath))
def plot_write(z_all, nog_all, thr):
    fig = plt.figure()
    ax = fig.add_subplot(111, xlabel='z [mm]', ylabel='nog')
    ax.scatter(z_all, nog_all, marker='x')
    max_nog_index = np.argmax(nog_all)
    ax.axvline(x=z_all[max_nog_index])
    ax.set_title('nog thr={}'.format(thr))
    savefig_path = os.path.join(basepath, 'nogplot.png')
    fig.savefig(savefig_path, dpi=300)

    df = pd.DataFrame()
    df['nog'] = nog_all
    df['z'] = z_all
    out_csv = os.path.join(basepath, 'nog.csv')
    df.to_csv(out_csv, index=False)

gaus_size = 15
thr = 14
a = -0.50911432 / 1000

json_path = os.path.join(basepath, 'image.json')
if not os.path.exists(json_path):
    sys.exit('there are no file: {}'.format(json_path))
with open(json_path, 'r') as f:
    j = json.load(f)

npicture = len(j['Images'])

z = np.arange(starskip, npicture - endskip)
fit_csv = os.path.join(basepath, 'fitdata.csv')
df_fit = pd.read_csv(fit_csv, header=None)
b = df_fit[1][1] / 1000
stage_z = j['Images'][0]['stagez']
z = z * a + b + stage_z

nog_all = []
for i in range(starskip, npicture - endskip):
    ##nogの計算
    png_path = os.path.join(basepath, '{:04}.png'.format(i))
    if not os.path.exists(png_path):
        exit('there are no file: {}'.format(png_path))

    img_ori = cv2.imread(png_path, 0)
    img_gaus = cv2.GaussianBlur(img_ori, (gaus_size, gaus_size), 0)
    img_sub = cv2.subtract(img_gaus, img_ori)
    ret, img_thr = cv2.threshold(img_sub, thr, 1, cv2.THRESH_BINARY)
    nog = cv2.countNonZero(img_thr)
    nog_all.append(nog)



plot_write(z, nog_all, thr)
