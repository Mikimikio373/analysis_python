import cv2
import numpy as np
import json
import sys
import os
import yaml

basedir = 'R:\\minami\\20230213_Reversal\\1-7\\PL006'

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
ret, img_plus = cv2.threshold(img_first, 0, 0, cv2.THRESH_BINARY)



for layer in range(0, layer):
    for vx in range(0, x_size):
        for vy in range(0, y_size):
            path = os.path.join(basedir, 'IMAGE00_AREA-1', 'png', 'L{}_VX{:04d}_VY{:04d}'.format(layer, vx, vy), 'L{}_VX{:04d}_VY{:04d}_{}.png'.format(layer, vx, vy, picnum))
            if not os.path.exists(path):
                exit('there is no file: {}'.format(path))
            img_read = cv2.imread(path, 0)
            img_read = cv2.adaptiveThreshold(img_read, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 7)
            img_plus = cv2.add(img_plus, img_read)
            print(path, 'ended')

cv2.imshow('test', img_plus)
cv2.waitKey(0)
write_path = os.path.join(basedir, 'deadpixel_test.png')
cv2.imwrite(write_path, img_plus)

# img = Image.open('../16bit_search.png')
# print(img)
# print(img.getextrema())
# numpy_img = np.array(img)
# print(numpy_img)
# nLabels, labelImages, data, center = cv2.connectedComponentsWithStats(img)
# print(data)