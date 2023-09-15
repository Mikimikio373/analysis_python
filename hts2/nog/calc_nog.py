import cv2
import numpy as np

ref_path = 'Q:/minami/20230913_Ali/Module0/sensor-3/IMAGE00_AREA-1/png/L0_VX0000_VY0001/L0_VX0000_VY0001_1.png'

ref_img = cv2.imread(ref_path, 0)
ref_binary = cv2.adaptiveThreshold(ref_img, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 14)
ref_num = np.count_nonzero(ref_binary)
print(ref_num)

nog_list = []
for i in range(64):
    com_path = 'Q:/minami/20230913_Ali/20230913_oneshot/IMAGE/00_03/ImageFilterWithStream_GPU_0_00000000_0_{:03}.bmp'.format(i)
    com_img = cv2.imread(com_path, 0)
    com_binary = cv2.adaptiveThreshold(com_img, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 14)
    tmp = np.count_nonzero(com_binary)
    nog_list.append(tmp)

print(nog_list)
