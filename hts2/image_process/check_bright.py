import os
import sys

import cv2
import numpy as np
from matplotlib import pyplot as plt

# basepath = 'Q:/minami/20230811_grain2023_focus/1um/1'
# basepath = 'Q:/minami/20230811_hts1_shot/1um'

if not len(sys.argv) == 2:
    sys.exit('command line error, please input \"basepath\"')
basepath = sys.argv[1]

out_dir = os.path.join(basepath, 'bright_chech')
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


# x = 0
# y = 0
cut_w = 3
for x in range(4, 2048, 16):
    for y in range(4, 1088, 16):
        bright = []
        print('calc for x:{}, y:{}'.format(x, y))
        for i in range(64):
            path = os.path.join(basepath, '{:04}.png'.format(i))
            img = cv2.imread(path, 0)
            bright.append(img[y, x])

        max_bright = np.max(bright)
        min_bright = np.min(bright)
        max_index = np.argmin(bright)

        if max_bright - min_bright < 60:
            continue
        dir = os.path.join(out_dir, 'cut_x{}_y{}.png'.format(x, y))
        os.makedirs(dir, exist_ok=True)
        left = x - cut_w
        if left < 0:
            left = 0
        right = x + cut_w + 1
        if right > 2048:
            right = 2048
        top = y - cut_w
        if top < 0:
            top = 0
        bottom = y + cut_w + 1
        if bottom > 1088:
            bottom = 1088
        z = np.arange(64)
        for i in range(64):
            path = os.path.join(basepath, '{:04}.png'.format(i))
            img = cv2.imread(path, 0)
            cut_img_path = os.path.join(dir, '{:04}.png'.format(i))
            cv2.imwrite(cut_img_path, img[top:bottom, left:right])


        plt.plot(z, bright, 'x')
        plt.xlim(0, 63)
        plt.xticks(np.arange(0, 64, 4))
        plt.minorticks_on()
        plt.grid()
        plt.xlabel('number of picture [1um/picture]')
        plt.ylabel('brightness')
        plt_path = os.path.join(dir, 'bright_plot.png')
        plt.savefig(plt_path, dpi=300)
        plt.clf()

        print('x:{}, y:{}, saved'.format(x, y))

