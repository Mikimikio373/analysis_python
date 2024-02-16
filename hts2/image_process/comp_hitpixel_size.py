import os
import sys

import numpy as np
import cv2
import matplotlib.pyplot as plt


basepath = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png_thr_cubic/png_thr_cubic10_9_zfilt-0.40'
basepath_fake = 'Q:/minami/rand_img/cubic109'
basepath_fakepng = os.path.join(basepath_fake, 'test_png')
basepath_fakefig = os.path.join(basepath_fake, 'test_data')

picnum = 14
stepx = 27
stepy = 55
l = 0
picnum_real = stepx * stepy
nog = [[], []]
area = [[], []]
for vx in range(stepx):
    for vy in range(stepy):
        for area_pos, path in enumerate([basepath]):
            img_path = os.path.join(path, 'L0_VX{:04}_VY{:04}'.format(vx, vy), 'L0_VX{:04}_VY{:04}_{}.png'.format(vx, vy, picnum))
            img = cv2.imread(img_path, 0)
            ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
            retval, labels, stats, centor_ids = cv2.connectedComponentsWithStats(img)
            stats = np.asarray(np.delete(stats, 0, axis=0))
            nog[area_pos].append(cv2.countNonZero(img))
            area[area_pos] = np.hstack([area[area_pos], stats[:, 4]])  # hstack:横に結合  stats[:, 4]列の抽出(面積のとこだけ抜き出し)
    print('vx-{}/{} ended'.format(vx, stepx))

vnum = 50
npic = 16
picnum_fake = vnum * npic
for v in range(vnum):
    for p in range(npic):
        img_path = os.path.join(basepath_fakepng, '{}-{}.png'.format(v, p))
        img = cv2.imread(img_path, 0)
        nog[1].append(cv2.countNonZero(img))
        retval, lavels, stats, centor_ids = cv2.connectedComponentsWithStats(img)
        stats = np.asarray(np.delete(stats, 0, axis=0))
        area[1] = np.hstack([area[1], stats[:, 4]])
    print('fake {} / {} ended'.format(v, vnum))



print(np.sum(area[0]) / picnum_real)
print(np.sum(area[1]) / picnum_fake)
plt.figure(tight_layout=True)
factor_real = 1 / picnum_real
factor_fake = 1 / picnum_fake
plt.figure(tight_layout=True)
counts, bins = np.histogram(area[0], bins=30, range=(0.5, 30.5))
plt.hist(bins[:-1], bins, edgecolor='r', hatch='//', histtype='step', weights=factor_real*counts, label='Real Image', log=True)
counts, bins = np.histogram(area[1], bins=30, range=(0.5, 30.5))
plt.hist(bins[:-1], bins, edgecolor='b', hatch='\\\\', histtype='step', weights=factor_fake*counts, label='Fake Image', log=True)
plt.legend(fontsize=12)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(1, 10000)
plt.xlabel('Area of hitpixels', fontsize=18, loc='right')
plt.ylabel('Entries', fontsize=18, loc='top')
# plt.show()
savepath = os.path.join(basepath_fakefig, 'hitpixel_real-fake_comparea_log.png')
plt.savefig(savepath, dpi=300)
plt.clf()

counts, bins = np.histogram(area[0], bins=30, range=(0.5, 30.5))
plt.hist(bins[:-1], bins, edgecolor='r', hatch='//', histtype='step', weights=factor_real*counts, label='Real Image')
counts, bins = np.histogram(area[1], bins=30, range=(0.5, 30.5))
plt.hist(bins[:-1], bins, edgecolor='b', hatch='\\\\', histtype='step', weights=factor_fake*counts, label='Fake Image')
plt.legend(fontsize=12)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
# plt.ylim(1, 10000)
plt.xlabel('Area of hitpixels', fontsize=18, loc='right')
plt.ylabel('Entries', fontsize=18, loc='top')
# plt.show()
savepath = os.path.join(basepath_fakefig, 'hitpixel_real-fake_comparea.png')
plt.savefig(savepath, dpi=300)


