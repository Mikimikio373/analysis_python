import os.path
import sys

import numpy as np
import cv2
import itertools
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.backends.backend_pdf import PdfPages

if not len(sys.argv) == 2:
    sys.exit('command error. \"basepath\"')

basepath = sys.argv[1]
module = 6
sensor = 12

outpath = os.path.join(basepath, "brightness_data.pdf")
out_pdf = PdfPages(outpath)

for m in range(module):
    for s in range(sensor):
        img_path = os.path.join(basepath, '{}-{}.jpg'.format(m, s))
        if not os.path.join(img_path):
            sys.exit('there are no file: {}'.format(img_path))
        print(img_path)
        img = cv2.imread(img_path, 0)

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
        fig.suptitle('module:{}, sensor:{}'.format(m, s+1), size=20)
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
        plt.clf()
        print('Module{}, sensor-{} ended'.format(m, s))

out_pdf.close()
