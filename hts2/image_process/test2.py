import copy
import os.path

import cv2

png_path = 'B:/data/powerpoint/HTS2_data/4master_theisis/GRAINE2023_u4_gap4.8/L0_VX0000_VY0014_ori/L0_VX0000_VY0014_11.png'
out_path = 'B:/data/powerpoint/master_presen/fig/resize2'
os.makedirs(out_path, exist_ok=True)
img = cv2.imread(png_path, 0)
roi = copy.deepcopy(img[410:450, 470:510])

cv2.imwrite(os.path.join(out_path, 'ori.png'), roi)
cv2.imwrite(os.path.join(out_path, 'roi.png'), cv2.resize(roi, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
roi_roi = roi[5:10, 14:19]
cv2.imwrite(os.path.join(out_path, 'roi_roi.png'), cv2.resize(roi_roi, None, fx=16, fy=16, interpolation=cv2.INTER_NEAREST))
resize = cv2.resize(roi, None, fx=1.4, fy=1.4, interpolation=cv2.INTER_CUBIC)
resize_roi = resize[7:14, 20:27]
cv2.imwrite(os.path.join(out_path, 'roi_resize1.4_ori.png'), resize)
cv2.imwrite(os.path.join(out_path, 'roi_resize1.4_roi.png'), cv2.resize(resize_roi, None, fx=16, fy=16, interpolation=cv2.INTER_NEAREST))
cv2.imwrite(os.path.join(out_path, 'roi_resize1.4.png'), cv2.resize(resize, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))

