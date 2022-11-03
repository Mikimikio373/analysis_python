import cv2
import numpy as np
import json
import sys
import os
from PIL import Image


x_size = 18     # x方向の大きさ
y_size = 72     # y方向の大きさ

img_plus = cv2.imread('../original_data/png/L0_VX0000_VY0000/L0_VX0000_VY0000_0.png', 0)
# img_mask = cv2.imread('../deadpixel_search_inv.png', 0)
ret, img_plus = cv2.threshold(img_plus, 0, 0, cv2.THRESH_BINARY)

for layer in range(0, 2):
    for vx in range(0, x_size):
        for vy in range(0, y_size):
            path = '../original_data/png/L{0}_VX{1:04}_VY{2:04}/L{0}_VX{1:04}_VY{2:04}_8.png'.format(layer, vx, vy)
            img_read = cv2.imread(path, 0)
            # cv2.imshow('test', img_read)
            # cv2.waitKey(0)
            img_read = cv2.adaptiveThreshold(img_read, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 7)
            # cv2.imshow('test', img_read)
            # cv2.waitKey(0)
            # img_read = cv2.multiply(img_read, img_mask, 1)
            img_plus = cv2.add(img_plus, img_read)
            print(path, 'ended')

working_directory = '../'
os.chdir(working_directory)
directory = os.getcwd()
print('directory changed, current directory =', directory)
cv2.imshow('test', img_plus)
cv2.waitKey(0)
cv2.imwrite('deadpixel_test.png', img_plus)

# img = Image.open('../16bit_search.png')
# print(img)
# print(img.getextrema())
# numpy_img = np.array(img)
# print(numpy_img)
# nLabels, labelImages, data, center = cv2.connectedComponentsWithStats(img)
# print(data)