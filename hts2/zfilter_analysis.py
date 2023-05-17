import cv2
import numpy as np
import json
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize

vx = 12
vy = 30
layer = 0
cut_width = 16
cut_height = 17
plot_width = np.arange(cut_width + 1)
plot_height = np.arange(cut_height + 1)[::-1]
width = 2048
height = 1088
x_step = int(width / cut_width)
y_step = int(height / cut_height)

save_folder = '../original_data/png/cut'
os.makedirs(save_folder, exist_ok=True)

folder_path = '../original_data/png/L{}_VX{:04}_VY{:04}'.format(layer, vx, vy)
img_mask = cv2.imread('../deadpixelmask2.png', 0)
ret, img_mask = cv2.threshold(img_mask, 1, 1, cv2.THRESH_BINARY)

img_all = []


for i in range(0, 16):
    png_name = 'L{}_VX{:04}_VY{:04}_{}.png'.format(layer, vx, vy, i)
    png_name_not = 'L{}_VX{:04}_VY{:04}_bitnot_{}.png'.format(layer, vx, vy, i)
    png_name_highpath = 'L{}_VX{:04}_VY{:04}_map_{}.png'.format(layer, vx, vy, i)
    png_name_highpathColor = 'L{}_VX{:04}_VY{:04}_mapColor_{}.png'.format(layer, vx, vy, i)
    png_name_thresh = 'L{}_VX{:04}_VY{:04}_thresh_{}.png'.format(layer, vx, vy, i)
    png_path = os.path.join(folder_path, png_name)

    img = cv2.imread(png_path, 0)

    img_not = cv2.bitwise_not(img)
    img_gauss = cv2.GaussianBlur(img, ksize=(15, 15), sigmaX=0)
    img_highpath = cv2.subtract(img_gauss, img)
    img_highpath = cv2.multiply(img_highpath, img_mask)
    print(max(np.ravel(img_highpath)))
    ret, img_thresh = cv2.threshold(img_highpath, 20, 255, cv2.THRESH_BINARY)

    for j in range(0, x_step):
        for k in range(0, y_step):
            firstX = int(cut_width * j)
            firstY = int(cut_height * k)
            lastX = firstX + cut_width
            lastY = firstY + cut_height
            print('img{}'.format(i), firstX, lastX, firstY, lastY)
            cut_folder = 'FX{:04}_LX{:04}_FY{:04}_LY{:04}'.format(firstX, lastX, firstY, lastY)
            path = os.path.join(save_folder, cut_folder)
            os.makedirs(path, exist_ok=True)


            img_cut = img[firstY:lastY, firstX:lastX]
            img_not_cut = img_not[firstY:lastY, firstX:lastX]
            img_highpath_cut = img_highpath[firstY:lastY, firstX:lastX]
            img_thresh_cut = img_thresh[firstY:lastY, firstX:lastX]

            cut_png_path = os.path.join(path, png_name)
            cut_not_path = os.path.join(path, png_name_not)
            cut_highpath_path = os.path.join(path, png_name_highpath)
            cut_highpath_pathColor = os.path.join(path, png_name_highpathColor)
            cut_thresh_path = os.path.join(path, png_name_thresh)

            plt.pcolormesh(plot_width, plot_height, img_highpath_cut, cmap=cm.jet, norm=Normalize(vmin=0, vmax=70))
            pp1 = plt.colorbar(orientation="vertical")  # カラーバーの表示
            plt.savefig(cut_highpath_pathColor)
            plt.clf()

            plt.pcolormesh(plot_width, plot_height, img_highpath_cut, cmap=cm.gray, norm=Normalize(vmin=0, vmax=70))
            pp2 = plt.colorbar(orientation="vertical")  # カラーバーの表示
            plt.savefig(cut_highpath_path)
            plt.clf()
            # plt.show()

            # cv2.imwrite(cut_png_path, img_cut)
            # cv2.imwrite(cut_not_path, img_not_cut)
            # cv2.imwrite(cut_thresh_path, img_thresh_cut)



