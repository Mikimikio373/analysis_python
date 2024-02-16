import json
import os.path
import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt

# basepath = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png_thr_noncubic_freq0.08_z0.3/png_thr14_13'
# basepath = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png_thr_cubic9_8_zfilt-0.40'
# basepath = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png_thr_noncubic_freq0.08_z0.3/png_thr16_15'
# basepath = 'Q:/minami/20231204_fakeimg/noncubic1514/IMAGE00_AREA-1/png'

if len(sys.argv) != 2:
    sys.exit('error. [basepath]')
basepath = sys.argv[1]

json_base = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1'

nx = 27
ny = 55
npicture = 27
z_relation = []
json_mode = True
erode_mode = False
l = 0

for vy in range(ny):
    for vx in range(nx):
        view = vx + nx * l + nx * 2 * vy

        json_file = os.path.join(json_base, 'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view, l, vx, vy, npicture))
        with open(json_file, 'rb') as f:
            j = json.load(f)

        first = 0
        last = 15
        if json_mode:
            if l == 0:
                last = j['Last'] - 1
                first = last - 15
            else:
                first = j['First']
                last = first + 15

        for i in range(first, last):
            png0 = os.path.join(basepath, 'L{}_VX{:04}_VY{:04}'.format(l, vx, vy), 'L{}_VX{:04}_VY{:04}_{}.png'.format(l ,vx, vy, i))
            png1 = os.path.join(basepath, 'L{}_VX{:04}_VY{:04}'.format(l, vx, vy), 'L{}_VX{:04}_VY{:04}_{}.png'.format(l ,vx, vy, i + 1))
            if not os.path.exists(png0):
                print('there is no file: {}'.format(png0))
                continue
            if not os.path.exists(png1):
                print('there is no file: {}'.format(png1))
                continue
            img0 = cv2.imread(png0, 0)
            if erode_mode:
                img0 = cv2.erode(img0, np.ones((2, 2), np.uint8))
            img1 = cv2.imread(png1, 0)
            if erode_mode:
                img1 = cv2.erode(img1, np.ones((2, 2), np.uint8))
            img_and = cv2.bitwise_and(img0, img1)
            z_relation.append(float(cv2.countNonZero(img_and) / cv2.countNonZero(img0)))

    print('{} / {} ended'.format(vy, ny))

print(np.average(z_relation), np.std(z_relation))
entries = len(z_relation)
ave = np.average(z_relation)
std_dev = np.std(z_relation)
x_min = ave - std_dev*5
x_max = ave + std_dev*5
histreturn = plt.hist(z_relation, bins=100, histtype='stepfilled',
                      range=(x_min, x_max),
                        facecolor='yellow',
                        linewidth=1, edgecolor='black')

factor = 0.9

text = 'Entries: {:d}\nMean: {:.4f}\nStd_dev: {:.4f}'.format(entries, ave, std_dev)
plt.text(histreturn[1][-10], max(histreturn[0]) * factor, text, bbox=(dict(boxstyle='square', fc='w')))
# plt.show()
if erode_mode:
    out_png = os.path.join(basepath, 'z-relation_L{}_erode.png'.format(l))
else:
    out_png = os.path.join(basepath, 'z-relation_L{}.png'.format(l))
plt.savefig(out_png, dpi=300)
if erode_mode:
    out_txt = os.path.join(basepath, 'z-relation_L{}_erode.txt'.format(l))
else:
    out_txt = os.path.join(basepath, 'z-relation_L{}.txt'.format(l))
with open(out_txt, 'w') as f:
    f.write('entries,average,std\n{},{},{}'.format(entries, ave, std_dev))

