import cv2
import numpy as np

img_path = 'Q:/minami/graine_u4/PL089/L0_VX0009_VY0043_2d/fft/L0_VX0009_VY0043_10_2d.png'
out_path = 'Q:/minami/graine_u4/PL089/L0_VX0009_VY0043_2d/fft/L0_VX0009_VY0043_10_2d_edit.png'

img = cv2.imread(img_path, 0)

bright_max = np.max(img)

img_edit = (np.asarray(img).astype(np.float64) * 255 / bright_max).astype(np.uint8)
print(img_edit)
cv2.imwrite(out_path, img_edit)


