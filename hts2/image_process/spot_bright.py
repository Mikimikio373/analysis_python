import os
import sys

import cv2
import numpy as np
from matplotlib import pyplot as plt


if not len(sys.argv) == 4:
    sys.exit('command line error, please input \"basepath\"')
basepath = sys.argv[1]
x = int(sys.argv[2])
y = int(sys.argv[3])

out_dir = os.path.join(basepath, 'bright_chech')
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


cut_w = 3
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
    sys.exit('max_bright - min_bright < 60')
dir = os.path.join(out_dir, 'cut_x{}_y{}.png'.format(x, y))
os.makedirs(dir, exist_ok=True)
z = np.arange(64)

plt.plot(z, bright, 'x')
plt.xlim(0, 63)
plt.xticks(np.arange(0, 64, 4))
plt.minorticks_on()
plt.grid()
plt.xlabel('number of picture [1um/picture]')
plt.ylabel('brightness')
plt.ylim(min_bright - 5, min_bright + 75)
plt_path = os.path.join(dir, 'bright_plot_spot.png')
plt.savefig(plt_path, dpi=300)
plt.clf()

print('x:{}, y:{}, saved'.format(x, y))

