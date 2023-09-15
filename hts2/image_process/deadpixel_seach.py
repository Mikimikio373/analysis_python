import sys
import cv2
import os

import pandas as pd
import yaml
import numpy as np
import itertools
import matplotlib.pyplot as plt
import time

basedir = 'Q:/minami/202300912_aff'

if not len(sys.argv):
    sys.exit('please command number of module and number of sensor')
m = sys.argv[1]
s = sys.argv[2]
module = 'Module{}'.format(m)
sensor = 'sensor-{}'.format(s)

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

first_png = os.path.join(tar_dir, 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_{}_0.png'.format(npicture))
if not os.path.exists(first_png):
    exit('there is no file: {}'.format(first_png))
img_first = cv2.imread(first_png, 0)
height, width = img_first.shape[:2]
img_plus = np.zeros((height, width), np.uint16)


print('start binaly')
time_s = time.perf_counter()
for l in range(0, layer):
    for vx in range(0, x_size):
        for vy in range(0, y_size):
            if vx == 0 and vy == 0:
                continue
            path = os.path.join(tar_dir, 'IMAGE00_AREA-1', 'png', 'L{}_VX{:04d}_VY{:04d}_{}.png'.format(l, vx, vy, npicture))
            if not os.path.exists(path):
                exit('there is no file: {}'.format(path))
            img_read = cv2.imread(path, 0)
            img_read = cv2.adaptiveThreshold(img_read, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 14)
            img_plus += np.array(img_read)
            if vy == y_size - 1:
                print(path, 'ended')
time_e = time.perf_counter()
print('binaly ended {} [s]'.format(time_e - time_s))
print(img_plus)
write_path = os.path.join(tar_dir, 'deadpixel_list_img.tif')
cv2.imwrite(write_path, img_plus)


analysys_img = img_plus

img_flat = list(itertools.chain.from_iterable(analysys_img))

mean = np.average(img_flat)
dev = np.std(img_flat)

print(x_size, y_size, layer)
bins = x_size * y_size * layer
cut = bins * (7/16)
print('plot hist now')
time_s = time.perf_counter()
plt.hist(img_flat, bins=bins, range=(0, bins), log=True)
time_e = time.perf_counter()
print('plot eneded: {} [s]'.format(time_e - time_s))

plt.axvline(x=cut, c='r')
plt.title('{} {}'.format(module, sensor))
plt.xlabel('piles binary img / pixel')
plt.ylabel('entries')
# plt.show()
plt.savefig(os.path.join(tar_dir, 'deadpixel_seach.pdf'))

ret, binaly_img = cv2.threshold(analysys_img, cut, 255, cv2.THRESH_BINARY_INV)
binaly_img = binaly_img.astype(np.uint8)
cv2.imwrite(os.path.join(tar_dir, 'deadpixel_mask.png'), binaly_img)
binaly_img = np.asarray(binaly_img)
deadpixel_list = np.where(binaly_img == 0)
print(deadpixel_list[0], deadpixel_list[1])

out_df = pd.DataFrame()
out_df['px'] = deadpixel_list[1]
out_df['py'] = deadpixel_list[0]
out_csv = os.path.join(tar_dir, 'deadpixel_list.csv')
out_df.to_csv(out_csv, index=False)


