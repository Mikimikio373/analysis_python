import os.path

import cv2
import numpy as np
import json

basepath = 'A:/Test/0035'
imager_id = 0
deadpixel_json_path = 'X:/Project_v3/AdminParam/HTS2/DeadPixel.json'
with open(deadpixel_json_path, 'rb') as f:
    deadpixel_json = json.load(f)

with open(os.path.join(basepath, 'CameraParamList.json'), 'rb') as f:
    camera_param = json.load(f)

print(camera_param[imager_id])
print(deadpixel_json[imager_id])

# for pic in range(24):
#     img_path = os.path.join(basepath, 'IMAGE', '00_{:02}'.format(imager_id), 'ImageFilterWithInterpolation_GPU_0_00000000_0_{:03}.bmp'.format(pic))
#     img = cv2.imread(img_path, 0)
#
#     for i in range(len(deadpixel_json[imager_id]['DeadPixel'])):
#         x = int(deadpixel_json[imager_id]['DeadPixel'][i][0])
#         y = int(deadpixel_json[imager_id]['DeadPixel'][i][1])
#         print(img[y, x], x, y)

img_path = os.path.join(basepath, 'IMAGE', '00_{:02}'.format(imager_id), 'ImageFilterWithInterpolation_GPU_0_00000000_0_{:03}.bmp'.format(0))
img = cv2.imread(img_path, 0)

for i in range(len(deadpixel_json[imager_id]['DeadPixel'])):
    x = int(deadpixel_json[imager_id]['DeadPixel'][i][0])
    y = int(deadpixel_json[imager_id]['DeadPixel'][i][1])
    print(img[y, x], x, y)