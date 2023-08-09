import os
import cv2
import sys
import yaml
import numpy as np
from matplotlib import pyplot as plt
import json
import pandas as pn

if len(sys.argv) != 2:
    exit('command line error. please \"basepath\"')

basepath = sys.argv[1]
if not os.path.exists(basepath):
    exit('there is no directory: {}'.format(basepath))

def plot_write(z_all, nog_all, thr):
    fig = plt.figure()
    ax = fig.add_subplot(111, xlabel='z [mm]', ylabel='nog')
    ax.scatter(z_all, nog_all, marker='x')
    max_nog_index = np.argmax(nog_all)
    ax.axvline(x=z_all[max_nog_index])
    ax.set_title('nog thr={}'.format(thr))
    savefig_path = os.path.join(basepath, 'nogplot_thr{}.png'.format(thr))
    fig.savefig(savefig_path, dpi=300)

    df = pn.DataFrame()
    df['nog'] = nog_all
    df['z'] = z_all
    out_csv = os.path.join(basepath, 'nog_thr{}.csv'.format(thr))
    df.to_csv(out_csv, index=False)

gaus_size = 15
thr = 14

yaml_path = os.path.join(basepath, 'AreaScan4Param.yml')
if not os.path.exists(yaml_path):
    exit('there are no file: {}'.format(yaml_path))

with open(yaml_path, 'rb') as yml:
    param = yaml.safe_load(yml)

npicture = param["NPictures"]


json_path = os.path.join(basepath, 'IMAGE00_AREA-1', 'V00000000_L0_VX0000_VY0000_0_{:03}.json'.format(npicture))
if not os.path.exists(json_path):
    exit('there are no file: {}'.format(json_path))
j_open = open(json_path, 'r')
j_load = json.load(j_open)

z_all = []
nog_all = []
for i in range(npicture):
    ##jsonからz軸の取得
    z = float(j_load['Images'][i]['z'])
    z_all.append(z)

    ##nogの計算
    png_path = os.path.join(basepath, 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000', 'L0_VX0000_VY0000_{}.png'.format(i))
    if not os.path.exists(png_path):
        exit('there are no file: {}'.format(png_path))

    img_ori = cv2.imread(png_path, 0)
    img_gaus = cv2.GaussianBlur(img_ori, (gaus_size, gaus_size), 0)
    img_sub = cv2.subtract(img_gaus, img_ori)
    ret, img_thr = cv2.threshold(img_sub, thr, 1, cv2.THRESH_BINARY)
    nog = cv2.countNonZero(img_thr)
    nog_all.append(nog)


plot_write(z_all, nog_all, thr)