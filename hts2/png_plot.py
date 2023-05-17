import sys
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

img = Image.open('../16bit_search7.png')
print(img)
print(img.getextrema())
numpy_img = np.array(img)
print(numpy_img)
# x_size = 2048     # x方向の大きさ
# y_size = 1088     # y方向の大きさ
# x = np.arange(x_size + 1)
# y = np.arange(y_size + 1)
#
# plt.pcolormesh(x, y, numpy_img, cmap=cm.jet)
# pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
# pp.set_label("brightness", fontname="Arial", fontsize=16)  # カラーバーのラベル
# plt.title('dear pixel search', fontsize=20)
# plt.xlabel('X position', fontsize=16)
# plt.ylabel('Y position', fontsize=16)
# plt.axes().set_aspect('equal')
plt.savefig('../deadpixel_colormap7.png', dpi=1200)
plt.clf()
numpy_img_flat = np.ravel(numpy_img)
print(numpy_img_flat)
n = sum(x > 1133 for x in numpy_img_flat)
print(n)


bin_num = int((max(numpy_img_flat) - min(numpy_img_flat) + 1) / 2)

plt.hist(numpy_img_flat, bins=bin_num, log=True)
plt.title('Brightness value', fontsize=20)
plt.xlabel('Brightness value', fontsize=16)
plt.ylabel('Entries', fontsize=16)
plt.axvline(x=1134, color='red')
# plt.show()
plt.savefig('../deadpixel_hist.png', dpi=1200)
plt.clf()

# plt.show()
