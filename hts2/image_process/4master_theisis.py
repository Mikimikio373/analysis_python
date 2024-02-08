import math
import os.path

import cv2
import matplotlib.pyplot as plt
import numpy as np

png_path = 'B:/data/powerpoint/HTS2_data/4master_theisis/GRAINE2023_u4_gap4.8/L0_VX0000_VY0014_ori/L0_VX0000_VY0014_11.png'
png_pathup = 'B:/data/powerpoint/HTS2_data/4master_theisis/GRAINE2023_u4_gap4.8/L0_VX0000_VY0014_ori/L0_VX0000_VY0014_10.png'
png_pathdown = 'B:/data/powerpoint/HTS2_data/4master_theisis/GRAINE2023_u4_gap4.8/L0_VX0000_VY0014_ori/L0_VX0000_VY0014_12.png'
# outpath = 'B:/data/powerpoint/HTS2_data/4master_theisis/GRAINE2023_u4_gap4.8'
outpath = 'B:/data/powerpoint/HTS2_data/4master_theisis/GRAINE2023_u4_gap4.8_small'
img = cv2.imread(png_path, 0)
imgup = cv2.imread(png_pathup, 0)
imgdown = cv2.imread(png_pathdown, 0)

# roi = img[350:510, 420:580]
roi = img[410:450, 470:510]
roi_path = os.path.join(outpath, 'roi.png')
nearest15 = cv2.resize(roi, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_NEAREST)
cv2.imwrite(os.path.join(outpath, 'nearest.png'), cv2.resize(nearest15, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
linear15 = cv2.resize(roi, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
cv2.imwrite(os.path.join(outpath, 'linear.png'), cv2.resize(linear15, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
bicubic15 = cv2.resize(roi, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
cv2.imwrite(os.path.join(outpath, 'bicubic.png'), cv2.resize(bicubic15, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
cv2.imwrite(roi_path, cv2.resize(roi, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
# roiup = imgup[350:510, 420:580]
# roidown = imgdown[350:510, 420:580]
roiup = imgup[410:450, 470:510]
roidown = imgdown[410:450, 470:510]

resize = cv2.resize(roi, None, fx=math.sqrt(2), fy=math.sqrt(2), interpolation=cv2.INTER_CUBIC)
resize_path = os.path.join(outpath, 'resize1.4.png')
cv2.imwrite(resize_path, cv2.resize(resize, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
resize_bitwise = cv2.bitwise_not(resize)
resizeup = cv2.resize(roiup, None, fx=math.sqrt(2), fy=math.sqrt(2), interpolation=cv2.INTER_CUBIC)
resizedown = cv2.resize(roidown, None, fx=math.sqrt(2), fy=math.sqrt(2), interpolation=cv2.INTER_CUBIC)

ori_gauss = cv2.GaussianBlur(roi, (15, 15), 0)
ori_gauss_path = os.path.join(outpath, 'ori_gauss.png')
cv2.imwrite(ori_gauss_path, cv2.resize(ori_gauss, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
ori_gaussup = cv2.GaussianBlur(roiup, (15, 15), 0)
ori_gaussdown = cv2.GaussianBlur(roidown, (15, 15), 0)
resize_gaussup = cv2.GaussianBlur(resizeup, (15, 15), 0)
resize_gaussdown = cv2.GaussianBlur(resizedown, (15, 15), 0)

resize_gauss = cv2.GaussianBlur(resize, (15, 15), 0)
resize_gauss_path = os.path.join(outpath, 'resize_gauss.png')
cv2.imwrite(resize_gauss_path, cv2.resize(resize_gauss, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
resize_gauss_bitwise = cv2.bitwise_not(resize_gauss)

diff_ori = cv2.subtract(ori_gauss, roi)
diff_oriup = cv2.subtract(ori_gaussup, roiup)
diff_oridown = cv2.subtract(ori_gaussdown, roidown)
diff_resize = cv2.subtract(resize_gauss, resize)
diff_resizeup = cv2.subtract(resize_gaussup, resizeup)
diff_resizedown = cv2.subtract(resize_gaussdown, resizedown)

up_down = cv2.add(diff_oriup, diff_oridown)
resize_up_down = cv2.add(diff_resizeup, diff_resizedown)
diff_zdiff = cv2.scaleAdd(up_down, -0.4 / 2, diff_ori)
diff_resize_zdiff = cv2.scaleAdd(resize_up_down, -0.4 / 2, diff_resize)

ret0, thr = cv2.threshold(diff_zdiff, 13, 255, cv2.THRESH_BINARY)
thr_path = os.path.join(outpath, 'thr.png')
cv2.imwrite(thr_path, cv2.resize(thr, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))

dilate = cv2.dilate(thr, np.ones((2, 2), np.uint8))
dilate_path = os.path.join(outpath, 'dilate.png')
cv2.imwrite(dilate_path, cv2.resize(dilate, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))


ret, thr_resize = cv2.threshold(diff_resize_zdiff, 10, 255, cv2.THRESH_BINARY)
thr_resize_path = os.path.join(outpath, 'resize_thr.png')
cv2.imwrite(thr_resize_path, cv2.resize(thr_resize, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))

dilate_resize = cv2.dilate(thr_resize, np.ones((2, 2), np.uint8))
dilate_resize_path = os.path.join(outpath, 'resize_dilate.png')
cv2.imwrite(dilate_resize_path, cv2.resize(dilate_resize, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))

# plt.plot(roi[124][:30], 'x-')
# plt.plot(ori_gauss[124][:30], 'x-')
# plt.plot(diff_ori[124][:30], 'x-')
# plt.plot(diff_zdiff[124][:30], 'x-')
# plt.ylim(0, 40)
# plt.grid()
# plt.show()
# plt.clf()

# plt.figure(tight_layout=True)
# plt.plot(resize[176][:30], 'o-', mfc='w', label='original')
# plt.plot(resize_gauss[176][:30], 'x-', label='BG')
# plt.ylim(170, 225)
# plt.xlabel('Position [pixel]', fontsize=16, loc='right')
# plt.ylabel('Brightness', fontsize=16, loc='top')
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.grid()
# plt.legend()
# plot_2dfilter_bf = os.path.join(outpath, '2dfilter_bf.png')
# plt.savefig(plot_2dfilter_bf, dpi=300)
# plt.clf()
#
# plt.figure(tight_layout=True)
# plt.plot(resize_bitwise[176][:30], 'o-', mfc='w', label='original')
# plt.plot(resize_gauss_bitwise[176][:30], 'x-', label='BG')
# plt.ylim(30, 80)
# plt.xlabel('Position [pixel]', fontsize=16, loc='right')
# plt.ylabel('Brightness', fontsize=16, loc='top')
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.grid()
# plt.legend()
# plot_2dfilter_bf_bitwise = os.path.join(outpath, '2dfilter_bf_bitwise.png')
# plt.savefig(plot_2dfilter_bf_bitwise, dpi=300)
# plt.clf()
#
# plt.figure(tight_layout=True)
# plt.plot(diff_resize[176][:30], '^-', c='g', mec='g', mfc='w', label='original - BG (Signal)')
# # plt.plot(resize_gauss[176][:30], 'x-', label='BG')
# plt.ylim(0, 40)
# plt.xlabel('Position [pixel]', fontsize=16, loc='right')
# plt.ylabel('Brightness', fontsize=16, loc='top')
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.grid()
# plt.legend()
# plot_2dfilter_bf = os.path.join(outpath, '2dfilter_af.png')
# plt.savefig(plot_2dfilter_bf, dpi=300)
# plt.clf()
#
# plt.figure(tight_layout=True)
# plt.plot(diff_resize[176][:30], '^-', c='g', mec='g', mfc='w', label='original - BG (Signal)')
# plt.plot(diff_resize_zdiff[176][:30], 'D-', c='r', mec='r', mfc='w', label='original - BG - defocus (Signal)')
# plt.ylim(0, 40)
# plt.xlabel('Position [pixel]', fontsize=16, loc='right')
# plt.ylabel('Brightness', fontsize=16, loc='top')
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.grid()
# plt.legend()
# plot_zfilter_bf = os.path.join(outpath, 'zfilter.png')
# plt.savefig(plot_zfilter_bf, dpi=300)
# plt.clf()

# plt.plot(diff_resize[176][:42], 'x-')
# plt.plot(diff_resize_zdiff[176][:42], 'x-')
# plt.ylim(0, 40)
# plt.grid()
# plt.show()

