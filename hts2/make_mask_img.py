import numpy as np
import cv2

height = 1088
width = 2048

img = np.ones((height, width)) * 255

cv2.imwrite('A:\\nonmask.png', img)