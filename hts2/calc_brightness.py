import os.path
import sys

import numpy as np
import cv2
import itertools
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.backends.backend_pdf import PdfPages

basepath ='R:\\minami\\20231020_kondensator_check'

outpath = os.path.join(basepath, "brightness_data.pdf")
out_pdf = PdfPages(outpath)

for m in range(0, 2):
    for s in range(1, 13):
        if s == 1:
            img_path = os.path.join(basepath, 'Module{}'.format(m), 'sensor-1_2'.format(s), '001',
                                    'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_4_0.png')
        else:
            img_path = os.path.join(basepath, 'Module{}'.format(m), 'sensor-1_{}'.format(s), '{:03}'.format(s), 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_4_0.png')
        print(img_path)
        img = cv2.imread(img_path, 0)
        # img = cv2.imread(os.path.join(basepath, '{}-{}'.format(m, s), '1.jpg'), 0)

        print(len(img[0]), len(img))
        projectionX = np.zeros(len(img[0]))
        projectionY = np.zeros(len(img))
        x_axis = np.arange(0, len(img[0]), 1)
        y_axis = np.arange(0, len(img), 1)
        for py in range(0, len(img)):
            for px in range(0, len(img[0])):
                projectionX[px] += img[py][px]
                projectionY[py] += img[py][px]

        print('append ended')
        fig = plt.figure(figsize=(12, 9), dpi=72, tight_layout=True)
        fig.suptitle('module:{}, sensor:{}'.format(m, s), size=20)
        ax1 = fig.add_subplot(221)
        cbar = ax1.imshow(img, cmap="gray", vmin=0, vmax=255)
        ax1.set_aspect('equal')
        ax1.set_title('image')
        fig.colorbar(cbar, ax=ax1, label='brightness')

        ax2 = fig.add_subplot(222)
        ax2.barh(y_axis, projectionY, 1, fc='b')
        ax2.invert_yaxis()
        ax2.set_title('projectin y')

        ax3 = fig.add_subplot(223)
        ax3.bar(x_axis, projectionX, 1, fc='r')
        ax3.set_title('projection x')

        flat_img = itertools.chain.from_iterable(img)
        ax4 = fig.add_subplot(224)
        ax4.hist(list(flat_img), bins=255, range=(0, 255), facecolor='limegreen')
        ax4.set_title('brightness')
        ax4.set_xlabel('average={:.1f}, std={:.1f}'.format(img.mean(), np.std(img)))

        out_pdf.savefig()
        # plt.show()
        plt.close()
        print('Module{}, sensor-{} ended'.format(m, s))

out_pdf.close()
