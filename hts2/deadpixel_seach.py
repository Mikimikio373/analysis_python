import sys

import cv2
import os
import yaml
import numpy as np

# basedir = 'R:\\minami\\20230213_Reversal\\1-7\\PL006'
basedir = 'R:\\minami\\20230213_Reversal\\4-6\\PL006'

yml_path = os.path.join(basedir, 'AreaScan4Param.yml')
if not os.path.exists(yml_path):
    exit('thre is no file: {}'.format(yml_path))
with open(yml_path, 'rb') as yml:
    param = yaml.safe_load(yml)
x_size = param['Area'][0]['NViewX']  # x方向の大きさ
y_size = param["Area"][0]["NViewY"]  # y方向の大きさ
layer = param["Area"][0]["NLayer"]
npicture = param["NPictures"]
plate_sum = layer * x_size * y_size
picnum = 7

first_png = os.path.join(basedir, 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000', 'L0_VX0000_VY0000_0.png')
if not os.path.exists(first_png):
    exit('there is no file: {}'.format(first_png))
img_first = cv2.imread(first_png, 0)
height, width = img_first.shape[:2]
img_plus = np.zeros((height, width), np.uint16)



for layer in range(0, layer):
    for vx in range(0, x_size):
        for vy in range(0, y_size):
            path = os.path.join(basedir, 'IMAGE00_AREA-1', 'png', 'L{}_VX{:04d}_VY{:04d}'.format(layer, vx, vy), 'L{}_VX{:04d}_VY{:04d}_{}.png'.format(layer, vx, vy, picnum))
            if not os.path.exists(path):
                exit('there is no file: {}'.format(path))
            img_read = cv2.imread(path, 0)
            img_read = cv2.adaptiveThreshold(img_read, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 14)
            # img_read = cv2.adaptiveThreshold(img_read, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 14)
            # cv2.imshow('test', img_read)
            # cv2.waitKey(0)
            # sys.exit()
            img_plus += np.array(img_read)
            if vy == y_size - 1:
                print(path, 'ended')

print(img_plus)
write_path = os.path.join(basedir, 'deadpixel_test.tif')
cv2.imwrite(write_path, img_plus)
