import os.path

import cv2

img_path = 'B:/data/powerpoint/master_presen/fig/show_interpolate/graine2023_flight.png'

outpath = os.path.split(img_path)[0]

img = cv2.imread(img_path)
img_roi = img[960:1005, 1275:1355]
cv2.imwrite(os.path.join(outpath, 'graine2023_fligt_roi.png'), img_roi)
img_nearest = cv2.resize(img_roi, None, fx=6, fy=6, interpolation=cv2.INTER_NEAREST)
cv2.imwrite(os.path.join(outpath, 'graine2023_flight_nearest6.png'), img_nearest)
img_cubic = cv2.resize(img_roi, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
cv2.imwrite(os.path.join(outpath, 'graine2023_flight_cubic6.png'), img_cubic)
img_cubic15 = cv2.resize(img_roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
img_cubic15 = cv2.resize(img_cubic15, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
cv2.imwrite(os.path.join(outpath, 'graine2023_flight_cubic15.png'), img_cubic15)
# cv2.imshow('test', img_nearest)
# cv2.waitKey(0)
