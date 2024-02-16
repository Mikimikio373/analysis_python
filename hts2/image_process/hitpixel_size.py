import os
import sys
import json

import numpy as np
import cv2
import matplotlib.pyplot as plt

# basepath = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-0.06/png/L0_VX0000_VY0000'
# basepath = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_nondilate/png_thr10_9'
# basepath_cubic = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_nondilate/png_thr_cubic10_9_zfilt-0.15'
# basepath = 'Q:/minami/20220429_suganami/006/IMAGE00_AREA-1/png_thr_nolilate/png_thr10_9/L0_VX0000_VY0000'

# basepath = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png_thr_cubic/png_thr_cubic11_10_zfilt-0.40'
basepath = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png_thr_noncubic_freq0.08_z0.3/png_thr14_13'
json_path = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1'
rand_img_path  = 'Q:/minami/rand_img/noncubic1413'
basepath_fake = os.path.join(rand_img_path, 'IMAGE00_AREA-1', 'png')
out_path = os.path.join(rand_img_path, 'create_data')


picnum = 27
stepx = 27
stepy = 55
l = 0
all_step = stepx * stepy * 16

area = [[], []]
for vx in range(stepx):
    for vy in range(stepy):
        # view = vx + stepx * l + stepx * 2 * vy
        view = vx + 27 * l + 27 * 2 * vy
        json_file = os.path.join(json_path, 'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view, l, vx, vy, picnum))
        with open(json_file, 'rb') as f:
            j = json.load(f)

        if l == 0:
            last = j['Last'] - 1
            first = last - 15
        else:
            first = j['First']
            last = first + 15

        for area_pos, path in enumerate([basepath, basepath_fake]):
            if area_pos == 1:
                first = 0
                last = 15
            for i in range(first, last + 1):
                img_path = os.path.join(path, 'L{}_VX{:04}_VY{:04}'.format(l, vx, vy), 'L{}_VX{:04}_VY{:04}_{}.png'.format(l, vx, vy, i))
                img = cv2.imread(img_path, 0)
                ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
                retval, labels, stats, centor_ids = cv2.connectedComponentsWithStats(img)
                stats = np.asarray(np.delete(stats, 0, axis=0))
                area[area_pos] = np.hstack([area[area_pos], stats[:, 4]])  # hstack:横に結合  stats[:, 4]列の抽出(面積のとこだけ抜き出し)
    print('vx-{}/{} ended'.format(vx, stepx))


print(np.sum(area[0]) / all_step)
print(np.sum(area[1]) / all_step)
plt.figure(tight_layout=True)
factor = 1 / all_step
plt.figure(tight_layout=True)
counts, bins = np.histogram(area[0], bins=30, range=(0.5, 30.5))
plt.hist(bins[:-1], bins, edgecolor='r', hatch='//', histtype='step', weights=factor*counts, label='Real Image', log=True)
counts, bins = np.histogram(area[1], bins=30, range=(0.5, 30.5))
plt.hist(bins[:-1], bins, edgecolor='b', hatch='\\\\', histtype='step', weights=factor*counts, label='Fake Image', log=True)
plt.legend(fontsize=12)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(1, 10000)
plt.xlabel('Area of hitpixels', fontsize=18, loc='right')
plt.ylabel('Entries', fontsize=18, loc='top')
# plt.show()
savepath = os.path.join(out_path, 'comp_hitpixelsize_log.png')
plt.savefig(savepath, dpi=300)
plt.clf()

counts, bins = np.histogram(area[0], bins=30, range=(0.5, 30.5))
plt.hist(bins[:-1], bins, edgecolor='r', hatch='//', histtype='step', weights=factor*counts, label='Real Image')
counts, bins = np.histogram(area[1], bins=30, range=(0.5, 30.5))
plt.hist(bins[:-1], bins, edgecolor='b', hatch='\\\\', histtype='step', weights=factor*counts, label='Fake Image')
plt.legend(fontsize=12)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Area of hitpixels', fontsize=18, loc='right')
plt.ylabel('Entries', fontsize=18, loc='top')
# plt.show()
savepath = os.path.join(out_path, 'comp_hitpixelsize.png')
plt.savefig(savepath, dpi=300)


