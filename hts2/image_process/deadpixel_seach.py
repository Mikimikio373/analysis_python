import sys
import cv2
import os
import yaml
import numpy as np
import itertools
import matplotlib.pyplot as plt

basedir = 'Q:/minami/202300911_aff'
module = 'Module{}'.format(1)
sensor = 'sensor-{}'.format(7)

tar_dir = os.path.join(basedir, module, sensor)

yml_path = os.path.join(tar_dir, 'AreaScan4Param.yml')
if not os.path.exists(yml_path):
    exit('thre is no file: {}'.format(yml_path))
with open(yml_path, 'rb') as yml:
    param = yaml.safe_load(yml)
x_size = param['Area'][0]['NViewX']  # x方向の大きさ
y_size = param["Area"][0]["NViewY"]  # y方向の大きさ
layer = param["Area"][0]["NLayer"]
npicture = param["NPictures"] - 1

# first_png = os.path.join(tar_dir, 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_{}_0.png'.format(npicture))
# if not os.path.exists(first_png):
#     exit('there is no file: {}'.format(first_png))
# img_first = cv2.imread(first_png, 0)
# height, width = img_first.shape[:2]
# img_plus = np.zeros((height, width), np.uint16)
#
#
#
# for layer in range(0, layer):
#     for vx in range(0, x_size):
#         for vy in range(0, y_size):
#             if vx == 0 and vy == 0:
#                 continue
#             path = os.path.join(tar_dir, 'IMAGE00_AREA-1', 'png', 'L{}_VX{:04d}_VY{:04d}_{}.png'.format(layer, vx, vy, npicture))
#             if not os.path.exists(path):
#                 exit('there is no file: {}'.format(path))
#             img_read = cv2.imread(path, 0)
#             img_read = cv2.adaptiveThreshold(img_read, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 14)
#             img_plus += np.array(img_read)
#             if vy == y_size - 1:
#                 print(path, 'ended')
#
# print(img_plus)
# write_path = os.path.join(tar_dir, 'deadpixel_list_img.tif')
# cv2.imwrite(write_path, img_plus)


analysys_img = cv2.imread(os.path.join(tar_dir, 'deadpixel_list_img.tif'), -1)
img_flat = list(itertools.chain.from_iterable(analysys_img))
mean = np.average(img_flat)
dev = np.std(img_flat)
print(mean, dev)
bins = x_size * y_size * layer

plt.hist(img_flat, bins=bins, range=(0, bins), log=True)
plt.axvline(x=mean+dev*3, c='r')
plt.title('{} {}'.format(module, sensor))
plt.xlabel('piles binary img / pixel')
plt.ylabel('entries')
# plt.show()

ret, binaly_img = cv2.threshold(analysys_img, mean+dev*3, 255, cv2.THRESH_BINARY)
binaly_img = binaly_img.astype(np.uint8)
cv2.imwrite(os.path.join(tar_dir, 'deadpixel_mask.png'), binaly_img)
binaly_img = np.asarray(binaly_img)
deadpixel_list = np.where(binaly_img == 0)
print(deadpixel_list[0], deadpixel_list[1])


