import json
import math
import os.path
import sys

import cv2
import yaml
import numpy as np


def calc_inv(aff: list):
    a = np.array([[aff[0], aff[1]], [aff[2], aff[3]]])
    a_inv = np.linalg.inv(a)
    return [a_inv[0][0], a_inv[0][1], a_inv[1][0], a_inv[1][1]]


basepath = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1'

# read AreaScanParam
with open(os.path.join(basepath, '../AreaScan4Param.yml'), 'rb') as f:
    param = yaml.safe_load(f)

firstX = param['Area'][0]['FirstPositionX']
firstY = param['Area'][0]['FirstPositionY']
stepX = param['Area'][0]['ViewWidthX']
stepY = param['Area'][0]['ViewWidthY']
stepnumX = param['Area'][0]['NViewX']
stepnumY = param['Area'][0]['NViewY']
layer = param['Area'][0]['NLayer']
npic = param['NPictures']
print(firstX, stepnumX, firstY, stepnumY, stepX, stepY, layer)

aff = [0.000632183, -0.00000101362, -0.000000123625, -0.000631895]
aff_inv = calc_inv(aff)
print(aff_inv)
width = 2048
height = 1088
resize_w = 2896
resize_h = 1538
topbottom = 47
rightleft = 88
scale_w = resize_w / width
scale_h = resize_h / height
print(scale_w, scale_h)
aff_resize = [0.000632183/scale_w, -0.00000101362/scale_h, -0.000000123625/scale_w, -0.000631895/scale_h]
aff_inv_resize = calc_inv(aff_resize)
print(aff_inv_resize)

# ref_track = [0.0229, 0.0206, 9143.35, 57.3073]
ref_track = [-0.1215, 0.7470, 9956.9, -164.3]
l = 1
ref_track[2] = ref_track[2] / 1000  # um2mm
ref_track[3] = ref_track[3] / 1000  # um2mm
tarnumX = math.floor((ref_track[2] - firstX) / stepX)
tarnumY = math.floor((ref_track[3] - firstY) / stepY)
if tarnumY < 0:
    tarnumY = 0
tarnumX = 1
print(tarnumX, tarnumY)
view = int(tarnumX + tarnumY * stepnumX * layer + stepnumX * l)
tarjsonname = 'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view, l, tarnumX, tarnumY, npic)
with open(os.path.join(basepath, tarjsonname), 'rb') as f:
    j = json.load(f)
sx = j['Images'][0]['x']
sy = j['Images'][0]['y']
first = j['First']
last = first + 16
px_bf = ref_track[2] - sx
py_bf = ref_track[3] - sy
print(px_bf, py_bf)
px = aff_inv[0] * px_bf + aff_inv[1] * py_bf + (width / 2)
py = aff_inv[2] * px_bf + aff_inv[3] * py_bf + (height / 2)
print(px, py)
px_resize = aff_inv_resize[0] * px_bf + aff_inv_resize[1] * py_bf + (resize_w / 2)
py_resize = aff_inv_resize[2] * px_bf + aff_inv_resize[3] * py_bf + (resize_h / 2)
print(px_resize, py_resize)

cnt = 0
outpng_folder = os.path.join(basepath, 'roi_png')
if not os.path.exists(outpng_folder):
    os.makedirs(outpng_folder)
for i in range(first, last):
    img_path = os.path.join(basepath, 'png',
                            'L{0}_VX{1:04}_VY{2:04}/L{0}_VX{1:04}_VY{2:04}_{3}.png'.format(l, tarnumX, tarnumY, i))

    resize_path = os.path.join(basepath, 'png_thr_cubic10_9_zfilt-0.40', 'L{0}_VX{1:04}_VY{2:04}/L{0}_VX{1:04}_VY{2:04}_{3}.png'.format(l, tarnumX, tarnumY, i))
    if not os.path.exists(img_path):
        sys.exit('there is no file {}'.format(img_path))
    img = cv2.imread(img_path, 0)
    resize = cv2.imread(resize_path, 0)
    img_roi = img[int(py-45):int(py+45), int(px-45):int(px+45)]
    img_roi = cv2.resize(img_roi, None, fx=20, fy=20, interpolation=cv2.INTER_NEAREST)
    resize_roi = resize[int(py_resize - 63):int(py_resize + 63), int(px_resize - 63):int(px_resize + 63)]
    resize_roi = cv2.resize(resize_roi, None, fx=20, fy=20, interpolation=cv2.INTER_NEAREST)
    pngname = os.path.join(outpng_folder, 'L{}_VX{:04}_VY{:04}_{}_{}_{}.png'.format(l, tarnumX, tarnumY, int(px), int(py), i))
    resizepngname = os.path.join(outpng_folder, 'L{}_VX{:04}_VY{:04}_{}_{}_{}_thr.png'.format(l, tarnumX, tarnumY, int(px_resize), int(py_resize), i))
    cv2.imwrite(pngname, img_roi)
    cv2.imwrite(resizepngname, resize_roi)
    # cv2.imshow('test', resize_roi)
    # cv2.waitKey(0)
