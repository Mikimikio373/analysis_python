import os.path
import numpy as np
import cv2

basepath ='R:\\minami\\20221228_ali'


# f = open(os.path.join('Y:\\Mikio\\mine\\powerpoint\\F2F\\20230106\\data\\test.csv'), 'w')
# f.write(',brightness1,sigma1,brightness2,sigma2\n')
# for n_m in range(0, 2):
#     for n_s in range(2, 13):
#         imgpath1 = os.path.join(basepath, 'Module{}'.format(n_m), 'sensor-1_{}'.format(n_s), '001', 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_4_0.png')
#         img1 = cv2.imread(imgpath1, 0)
#         imgpath2 = os.path.join(basepath, 'Module{}'.format(n_m), 'sensor-1_{}'.format(n_s), '{:03}'.format(n_s), 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_4_0.png')
#         img2 = cv2.imread(imgpath2, 0)
#
#         img1_mean = img1.mean()
#         img2_mean = img2.mean()
#         f.write('sensor1-{},{},{},{},{}\n'.format(n_s, img1.mean(),np.std(img1), img2.mean(), np.std(img2)))

img0_9 = cv2.imread('R:\\minami\\20221229_ali-m\\1-0\\Module0\\sensor-9-2\\IMAGE00_AREA-1\\png\\L0_VX0000_VY0000_4_0.png')
img1_1 = cv2.imread('R:\\minami\\20221229_ali-m\\1-0\\Module1\\sensor-1\\IMAGE00_AREA-1\\png\\L0_VX0000_VY0000_4_0.png')

print('{},{},{},{}'.format(img1_1.mean(),np.std(img1_1),img0_9.mean(),np.std(img0_9)))