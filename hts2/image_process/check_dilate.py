import cv2
import numpy as np

img = np.zeros((8, 8), np.uint8)
print(img)

for i in range(2, 3):
    for j in range(2, 3):
        img[i][j] = 1
# img[2][2] = 255
print(img)
# cv2.imshow('test', img)
# cv2.waitKey(0)

img_dilate = cv2.dilate(img, np.ones((3, 3), np.uint8))
print(img_dilate)
img_erode = cv2.erode(img_dilate, np.ones((3, 3), np.uint8))
print(img_erode)
