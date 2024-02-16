import os.path
import random

import cv2
import numpy as np
import matplotlib.pyplot as plt


def rand_ints_nodup(rand_min, rand_max, num):
  ns = []
  while len(ns) < num:
    n = random.randint(rand_min, rand_max)
    if not n in ns:
      ns.append(n)
  return ns


def plot_hist(in_list: list, output_path: str, factor: float = 0.9, dpi: int = 300):
    histreturn = plt.hist(in_list, bins=100, histtype='stepfilled', facecolor='yellow', linewidth=1, edgecolor='black')
    text = 'Entries: {:d}\nMean: {:.4f}\nStd_dev: {:.4f}'.format(len(in_list), np.average(in_list), np.std(in_list))
    plt.text(histreturn[1][-10], max(histreturn[0]) * factor, text, bbox=(dict(boxstyle='square', fc='w')))
    plt.savefig(output_path, dpi=dpi)
    plt.clf()

# width = 2896
# height = 1538
width = 2048
height = 1088
width_max = 3072
height_max = 1632
toptottom = int((height_max - height) / 2)
lefttoright = int((width_max - width) / 2)

algo_name = 'noncubic1312'
delete_z_path = 'Q:/minami/rand_img/{}/not-z'.format(algo_name)
z_and_path = 'Q:/minami/rand_img/{}/z_and'.format(algo_name)
out_path = 'Q:/minami/rand_img/{}'.format(algo_name)

testmode = False

delz_num = 27 * 55 * 16
z_and_num = 27 * 55 * 16

nog_list = []
nog_delz = []
nog_and = []
nog_and2 = []
all_and_ratio = []
obj_list = []
z_relate = []
if testmode:
    out_fig = os.path.join(out_path, 'test_data')
    test_png_path = os.path.join(out_path, 'test_png')
    os.makedirs(test_png_path, exist_ok=True)
    for i in range(50):
        img_and_tmp = []
        img_tmp = []
        for j in range(17):
            img_and_tmp.append(cv2.imread(os.path.join(z_and_path, '{}.png'.format(random.randint(0, z_and_num - 1))), 0))

        for j in range(16):
            z_or = img_and_tmp[j] + img_and_tmp[j+1]
            nog_and.append(cv2.countNonZero(z_or))
            delz = cv2.imread(os.path.join(delete_z_path, '{}.png'.format(random.randint(0, delz_num - 1))), 0)
            nog_delz.append(cv2.countNonZero(delz))
            all_or = z_or + delz
            all_and_ratio.append(float(cv2.countNonZero(z_or) / cv2.countNonZero(all_or)))
            nog_list.append(cv2.countNonZero(all_or))
            n, labels = cv2.connectedComponents(all_or)
            obj_list.append(n)
            img_tmp.append(all_or)
            cv2.imwrite(os.path.join(test_png_path, '{}-{}.png'.format(i, j)), all_or)

        for j in range(15):
            img_and = cv2.bitwise_and(img_tmp[j], img_tmp[j+1])
            nog_and2.append(cv2.countNonZero(img_and))
            z_relate.append(float(cv2.countNonZero(img_and) / cv2.countNonZero(img_tmp[j])))

        print('\r{} ended'.format(i), end='')

else:
    out_fig = os.path.join(out_path, 'create_data')
    nx = 27
    ny = 55
    layer = 2
    # png pathの生成
    png_path = os.path.join(out_path, 'IMAGE00_AREA-1', 'png')
    os.makedirs(png_path, exist_ok=True)

    for vy in range(ny):
        for l in range(layer):
            for vx in range(nx):
                # pathの生成
                view_name = 'L{}_VX{:04}_VY{:04}'.format(l, vx, vy)
                os.makedirs(os.path.join(png_path, view_name), exist_ok=True)

                img_and_tmp = []
                img_tmp = []
                # z相関の17枚
                for j in range(17):
                    img_and_tmp.append(cv2.imread(os.path.join(z_and_path, '{}.png'.format(random.randint(0, z_and_num - 1))), 0))

                # 画像生成
                for j in range(16):
                    # z相関のor
                    z_or = img_and_tmp[j] + img_and_tmp[j + 1]
                    nog_and.append(cv2.countNonZero(z_or))
                    # 足し合わせるランダム成分
                    delz = cv2.imread(os.path.join(delete_z_path, '{}.png'.format(random.randint(0, delz_num - 1))), 0)
                    nog_delz.append(cv2.countNonZero(delz))
                    # 足し算
                    all_or = z_or + delz
                    all_and_ratio.append(float(cv2.countNonZero(z_or) / cv2.countNonZero(all_or)))
                    # nogの計算
                    nog_list.append(cv2.countNonZero(all_or))
                    n, labels = cv2.connectedComponents(all_or)
                    # obj数の計算
                    obj_list.append(n)
                    # 3072*1632に調整
                    all_or = cv2.copyMakeBorder(all_or, toptottom, toptottom, lefttoright, lefttoright,
                                                       cv2.BORDER_CONSTANT, value=0)
                    img_tmp.append(all_or)
                    cv2.imwrite(os.path.join(png_path, view_name, view_name + '_{}.png'.format(j)), all_or)

                for j in range(15):
                    img_and = cv2.bitwise_and(img_tmp[j], img_tmp[j + 1])
                    nog_and2.append(cv2.countNonZero(img_and))
                    z_relate.append(float(cv2.countNonZero(img_and) / cv2.countNonZero(img_tmp[j])))

                print(os.path.join(png_path, view_name) + ' written')

print('\npicture generated')
os.makedirs(out_fig, exist_ok=True)
nog_path = os.path.join(out_fig, 'hitpixelnum.png')
plot_hist(nog_list, nog_path)
nog_and_path = os.path.join(out_fig, 'hitpixel_and.png')
plot_hist(nog_and, nog_and_path)
nog_and2_path = os.path.join(out_fig, 'create_and.png')
plot_hist(nog_and2, nog_and2_path)
nog_delz_path = os.path.join(out_fig, 'hitpixel_delz.png')
plot_hist(nog_delz, nog_delz_path)
obj_path = os.path.join(out_fig, 'objnum.png')
plot_hist(obj_list, obj_path)
z_relate_path = os.path.join(out_fig, 'z-relate.png')
plot_hist(z_relate, z_relate_path)
all_and_ratio_path = os.path.join(out_fig, 'all_and_ratio.png')
plot_hist(all_and_ratio, all_and_ratio_path)

