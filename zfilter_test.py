import numpy as np
import cv2
import sys
import os
import pandas as pn

work_dir = '../zfilter_test'
orifinal_path = 'original'
save_path = '3dfilter_gauss'
save_path1 = '3dfilter_gauss_sub'
os.makedirs(os.path.join(work_dir, save_path), exist_ok=True)
os.makedirs(os.path.join(work_dir, save_path1), exist_ok=True)

layer = 0
vx = 11
vy = 33
first = 4
last = 21
zfilter = -0.15
img_ori = []
img_dog = []
img_2d = []

for i in range(first, last):
    photo_name = 'L{}_VX{:04}_VY{:04}_{}.png'.format(layer, vx, vy, i)
    file_path = os.path.join(work_dir, orifinal_path, photo_name)
    img = cv2.imread(file_path, 0)
    img2 = cv2.GaussianBlur(img, (15, 15), 0)
    img3 = cv2.subtract(img2, img)
    img_ori.append(img)
    img_dog.append(img2)
    img_2d.append(img3)


n = first

for i in range(0, last - first):
    print(i, n)
    photo_name = 'L{}_VX{:04}_VY{:04}_{}.png'.format(layer, vx, vy, n)
    a = i - 1
    b = i + 1
    if i == 0:
        img_b = cv2.GaussianBlur(img_2d[b], (3, 3), sigmaX=2, sigmaY=2)
        img_save = cv2.scaleAdd(img_b, zfilter, img_2d[i])
    elif i == 16:
        img_a = cv2.GaussianBlur(img_2d[a], (3, 3), sigmaX=2, sigmaY=2)
        img_save = cv2.scaleAdd(img_a, zfilter, img_2d[i])
    else:
        img_a = cv2.GaussianBlur(img_2d[a], (3, 3), sigmaX=2, sigmaY=2)
        img_b = cv2.GaussianBlur(img_2d[b], (3, 3), sigmaX=2, sigmaY=2)
        img_add = cv2.add(img_a, img_b)
        img_save = cv2.scaleAdd(img_add, zfilter, img_2d[i])

    # print(img_2d[i])
    max_bright = np.amax(img_save)
    img_sub = cv2.subtract(img_2d[i], img_save)
    # print(max_bright)
    img_save = 255 / max_bright * img_save
    cv2.imwrite(os.path.join(work_dir, save_path, photo_name), img_save)
    max_bright = np.amax(img_sub)
    img_sub = 255 / max_bright * img_sub
    cv2.imwrite(os.path.join(work_dir, save_path1, photo_name), img_sub)

    n += 1


    # sys.exit()
