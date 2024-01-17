import os
import sys

import numpy as np
import cv2
import matplotlib.pyplot as plt

# basepath = 'Q:/minami/20231204_fakeimg/IMAGE00_AREA-1-0.06/png/L0_VX0000_VY0000'
basepath = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_nondilate/png_thr10_9'
basepath_cubic = 'R:/usuda/GRAINE2023_u4/PL088_0904gap4/IMAGE00_AREA-1/png_thr_nondilate/png_thr_cubic10_9_zfilt-0.15'
# basepath = 'Q:/minami/20220429_suganami/006/IMAGE00_AREA-1/png_thr_nolilate/png_thr10_9/L0_VX0000_VY0000'

picnum = 11
stepx = 27
stepy = 55
all_step = stepx * stepy

area = [[], []]
for vx in range(stepx):
    for vy in range(stepy):
        for area_pos, path in enumerate([basepath, basepath_cubic]):
            img_path = os.path.join(path, 'L0_VX{:04}_VY{:04}'.format(vx, vy), 'L0_VX{:04}_VY{:04}_{}.png'.format(vx, vy, picnum))
            img = cv2.imread(img_path, 0)
            ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
            retval, labels, stats, centor_ids = cv2.connectedComponentsWithStats(img)
            stats = np.asarray(np.delete(stats, 0, axis=0))
            area[area_pos] = np.hstack([area[area_pos], stats[:, 4]])  # hstack:横に結合  stats[:, 4]列の抽出(面積のとこだけ抜き出し)
    print('vx-{}/{} ended'.format(vx, stepx))


print(np.sum(area[0]) / all_step)
print(np.sum(area[1]) / all_step)
factor = 1 / all_step
plt.figure(tight_layout=True)
counts, bins = np.histogram(area[0], bins=10, range=(0.5, 10.5))
plt.hist(bins[:-1], bins, edgecolor='r', hatch='//', histtype='step', weights=factor*counts, label='Used')
counts, bins = np.histogram(area[1], bins=10, range=(0.5, 10.5))
plt.hist(bins[:-1], bins, edgecolor='b', hatch='\\\\', histtype='step', weights=factor*counts, label='Not used')
plt.legend()
plt.xticks(range(1, 11), fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Area of hitpixels', fontsize=18, loc='right')
plt.ylabel('Entries', fontsize=18, loc='top')
# plt.show()
savepath = 'B:/data/powerpoint/HTS2_data/4master_theisis/hitpixel_area_comparea.png'
plt.savefig(savepath, dpi=300)


