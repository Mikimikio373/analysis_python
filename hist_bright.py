import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

pngpath = '../IMAGE00_AREA-1/png_test/L0_VX0001_VY0000/L0_VX0001_VY0000_0.png'

if os.path.exists(pngpath) == False:
    print('png path error')
    sys.exit()

img_ori = cv2.imread(pngpath, 0)
ori_bright = img_ori.flatten()
img_gauss = cv2.GaussianBlur(img_ori, (15, 15), 0)
img_highpass = cv2.subtract(img_gauss, img_ori)
highpass_bright = img_highpass.flatten()
img_resize = cv2.resize(img_highpass, (3072, 1632), interpolation=cv2.INTER_CUBIC)
resize_bright = img_resize.flatten()

# img[top : bottom, left : right]
img_ori_cut1 = img_ori[402 : 408, 753 : 759]
img_ori_cut2 = img_ori[394:400, 695:701]
# cv2.imshow('widow', img_cut1)
# cv2.waitKey(0)
cv2.imwrite('cut1.png', img_ori_cut1)
cv2.imwrite('cut2.png', img_ori_cut2)

img_highpass_cut1 = img_highpass[402:408, 753:759]
img_highpass_cut2 = img_highpass[394:400, 695:701]
img_resize_cut1 = cv2.resize(img_highpass_cut1, (9, 9), interpolation=cv2.INTER_CUBIC)
img_resize_cut2 = cv2.resize(img_highpass_cut2, (9, 9), interpolation=cv2.INTER_CUBIC)


# plt.hist(ori_bright, bins=255, range=(0, 255))

# plt.hist(highpass_bright, bins=100, range=(0, 100), log=True, alpha=0.3, histtype='stepfilled', color='r', label='original')
# plt.hist(resize_bright, bins=100, range=(0, 100), log=True, alpha=0.3, histtype='stepfilled', color='b', label='cubic')
# plt.legend(loc='upper right')
# plt.xlabel('brightness')
# plt.ylabel('entries')\

width = 6
height = 6
X = np.arange(0, width)
Y = np.arange(0, height)
x, y = np.meshgrid(X, Y)
x = x.flatten()
y = y.flatten()
z = np.zeros_like(x)
dx = np.repeat(1, repeats=len(x))
dy = np.repeat(1, repeats=len(y))

dz = img_highpass_cut1.flatten()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.bar3d(x, y, z, dx, dy, dz)
ax.set_zlabel('brightness')
ax.set_zlim(0, 30)
plt.savefig('bright_highpass1.png', dpi=600)
print(max(dz))
plt.clf()

dz = img_highpass_cut2.flatten()
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.bar3d(x, y, z, dx, dy, dz)
ax.set_zlabel('brightness')
ax.set_zlim(0, 30)
plt.savefig('bright_highpass2.png', dpi=600)
print(max(dz))
plt.clf()


width = 9
height = 9
X = np.arange(0, width)
Y = np.arange(0, height)
x, y = np.meshgrid(X, Y)
x = x.flatten()
y = y.flatten()
z = np.zeros_like(x)
dx = np.repeat(1, repeats=len(x))
dy = np.repeat(1, repeats=len(y))

dz = img_resize_cut1.flatten()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.bar3d(x, y, z, dx, dy, dz)
ax.set_zlabel('brightness')
ax.set_zlim(0, 30)
plt.savefig('bright_resize1.png', dpi=600)
print(max(dz))
# plt.show()
plt.clf()

dz = img_resize_cut2.flatten()

ax = fig.add_subplot(projection='3d')
ax.bar3d(x, y, z, dx, dy, dz)
ax.set_zlabel('brightness')
ax.set_zlim(0, 30)
plt.savefig('bright_resize2.png', dpi=600)
print(max(dz))
# plt.show()
plt.clf()
