import math
import os.path
import statistics
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np


width = 2048
height = 1088
gcd = math.gcd(width, height)
print(width, height, gcd)
mesh_w = int(width / gcd)
mesh_h = int(height / gcd)
print(mesh_w, mesh_h)
mesh_num_w = int(width / mesh_w)
mesh_num_h = int(height / mesh_h)
print(mesh_num_w, mesh_num_w)

# basepath = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_dilate/png_thr10_9'
basepath = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_nondilate/png_thr10_9'
# basepath = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-0.015_dilate/png'
# basepath = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-0.06/png'

hit_num = []
for vx in range(10):
    for vy in range(10):
        img_path = os.path.join(basepath, 'L0_VX{0:04}_VY{1:04}/L0_VX{0:04}_VY{1:04}_13.png'.format(vx, vy))
        if not os.path.exists(img_path):
            print('there is no file: {}'.format(img_path))
            continue
        img = cv2.imread(img_path, 0)

        for x in range(mesh_num_w):
            for y in range(mesh_num_h):
                left = x * mesh_w
                top = y * mesh_h
                right = left + mesh_w
                bottom = top + mesh_h
                roi = img[top:bottom, left:right]
                hit_num.append(np.count_nonzero(roi))

print(len(hit_num))
bins = 150
entries = len(hit_num)
ave = statistics.mean(hit_num)
stdev = statistics.stdev(hit_num)
histreturn = plt.hist(hit_num, bins=bins, histtype='stepfilled', range=(0, bins),
             facecolor='yellow',
             linewidth=0.5, edgecolor='black')
factor = 0.9
text = 'Entries: {:d}\nMean: {:4g}\nStd_dev: {:4g}'.format(entries, ave, stdev)
plt.text(max(histreturn[1]) * factor, max(histreturn[0]) * factor, text, bbox=(dict(boxstyle='square', fc='w')))
# plt.show()
plt.savefig('B:/data/powerpoint/HTS2_meeting/20231214/graine_nondilate_mesh_{}-{}.png'.format(mesh_w, mesh_h), dpi=300)
