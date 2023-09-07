import cv2
import numpy as np

# img_path = 'Q:/minami/graine_u4/PL089/L0_VX0009_VY0043_thr1211_dil/L0_VX0009_VY0043_2_thr2.png'
img_path = 'Q:/minami/graine_u4/PL089/L0_VX0009_VY0043_cubicthr1211_dil/L0_VX0009_VY0043_2_thr2.png'
# img_path = 'Q:/minami/graine_u4/PL089/L0_VX0009_VY0043_thr1211/L0_VX0009_VY0043_2_thr.png'
# img_path = 'Q:/minami/graine_u4/PL089/L0_VX0009_VY0043_cubicthr1211/L0_VX0009_VY0043_2_thr.png'

img = cv2.imread(img_path, 0)
num = np.count_nonzero(img)
print(num)

hit_per = num / (len(img) * len(img[0])) * 100
print(hit_per)