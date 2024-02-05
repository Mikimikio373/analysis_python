import os.path
import random

import cv2
import numpy as np


def rand_ints_nodup(a: int, b: int, k:int):
    '''
    重複なしでa~bからランダムに数字を抽出して返す関数
    :param a: 最小値
    :param b: 最大値
    :param k: 配列のサイズ
    :return: list
    '''
    out = []
    while len(out) < k:
        n = random.randint(a, b)
        if not n in out:
            out.append(n)
    return out


png_path = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1/png_thr_cubic/png_thr_cubic11_10_zfilt-0.40_dilate'
out_path = 'Q:/minami/rand_img'

vx = 0
vy = 0
npicture = 12
layer = 0
width = 2896
height = 1538
elirate = 0.3253


img_path = os.path.join(png_path, 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy), 'L{}_VX{:04}_VY{:04}_{}.png'.format(layer, vx, vy, npicture))
img = cv2.imread(img_path, 0)
print(cv2.countNonZero(img))
cv2.imwrite(os.path.join(out_path, 'ori.png'), img)
n, label = cv2.connectedComponents(img)

print(n)
elinum = int(n * elirate)
print(elinum)
elinum_list = sorted(rand_ints_nodup(0, n, elinum))
print(len(elinum_list))


for y in range(height):
    for x in range(width):
        if label[y, x] in elinum_list:
            img[y, x] = 0
    print('{} / {}'.format(y, height))

cv2.imwrite(os.path.join(out_path, 'test.png'), img)
print(cv2.countNonZero(img))
n, label = cv2.connectedComponents(img)


# cv2.imshow('test', img)
# cv2.waitKey(0)
