import os.path
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import curve_fit

import check_stage_module as mylib


def linear_z(X, a, b, c):
    x, y = X
    z = a*x + b*y + c
    return z


path1 = 'A:/Test/check_FASER/m222-pl002_30cm-1/fit_stage_quad/ali.json'
basepath = os.path.split(path1)[0]
outpdf = os.path.join(basepath, 'ali_stage_xydivide.pdf')
mylib.plot_xydivide(path1, outpdf, 60, 10000)

# shif_data1, int_df1, stage1 = mylib.read_ali_stage(path1, 0)
# x_data = shif_data1[0].query('flag == 1')['X'].values
# y_data = shif_data1[0].query('flag == 1')['Y'].values
# dx_data = shif_data1[0].query('flag == 1')['U'].values * 1000
# dy_data = shif_data1[0].query('flag == 1')['V'].values * 1000
#
# x_min = min(x_data)
# x_max = max(x_data)
# x_step = int((x_max - x_min) / 9) + 1
# y_min = min(y_data)
# y_max = max(y_data)
# y_step = int((y_max - y_min) / 5) + 1
# print(x_step, y_step)
#
# flag1 = shif_data1[0].query('flag == 1')
# flag1 = flag1.reset_index(drop=True)
# test = test.query('Y == @y_min')
# print(len(test))

# # 微分値プロット(カラーをX/Y軸に)
# cmap = plt.get_cmap('jet')
# im1 = plt.scatter(flag1['X'].values, flag1['U'].values*1000, c=flag1['Y'], s=1, cmap=cmap, marker='x', vmin=y_min, vmax=y_max)
# plt.yticks(range(-5, 6))
# plt.colorbar(im1)
# plt.grid()
# plt.savefig(os.path.join(basepath, 'xdx_colorY.png'), dpi=300)
# plt.clf()
#
# im2 = plt.scatter(flag1['X'].values, flag1['V'].values*1000, c=flag1['Y'], s=1, cmap=cmap, marker='x', vmin=y_min, vmax=y_max)
# plt.yticks(range(-5, 6))
# plt.colorbar(im2)
# plt.grid()
# plt.savefig(os.path.join(basepath, 'xdy_colorY.png'), dpi=300)
# plt.clf()
#
# im3 = plt.scatter(flag1['Y'].values, flag1['U'].values*1000, c=flag1['X'], s=1, cmap=cmap, marker='x', vmin=x_min, vmax=x_max)
# plt.yticks(range(-5, 6))
# plt.colorbar(im3)
# plt.grid()
# # plt.savefig(os.path.join(basepath, 'ydx_colorX.png'), dpi=300)
# plt.clf()
#
# im4 = plt.scatter(flag1['Y'].values, flag1['V'].values*1000, c=flag1['X'], s=1, cmap=cmap, marker='x', vmin=x_min, vmax=x_max)
# plt.yticks(range(-5, 6))
# plt.colorbar(im4)
# plt.grid()
# # plt.savefig(os.path.join(basepath, 'ydy_colorX.png'), dpi=300)
# plt.clf()



# plt.show()
# 積分値プロット
# shift_range = 75
# X = []
# Y = []
# U = []
# V = []
# for i in range(y_step):
#     a = y_min + 5.0 * i
#     x = np.array(flag1.query('Y == @a')['X'].values)
#     # 端からは時まであるか確認
#     # if not len(x) == x_step:
#     #     continue
#     y = np.array(flag1.query('Y == @a')['Y'].values)
#     u = np.array(flag1.query('Y == @a')['U'].values)
#     u = np.cumsum(u)  # 累積和に変更
#     v = np.array(flag1.query('Y == @a')['V'].values)
#     v = np.cumsum(v)  # 累積和に変更
#     X = np.hstack([X, x])
#     Y = np.hstack([Y, y])
#     U = np.hstack([U, u])
#     V = np.hstack([V, v])
#
# cmap = plt.get_cmap('jet')
# im1 = plt.scatter(X, U*1000, c=Y, s=1, cmap=cmap, marker='x', vmin=y_min, vmax=y_max)
# plt.ylim(-shift_range, shift_range)
# plt.colorbar(im1)
# plt.grid()
# plt.savefig(os.path.join(basepath, 'xdx_colorY_integ.png'), dpi=300)
# plt.clf()
#
# im2 = plt.scatter(X, V*1000, c=Y, s=1, cmap=cmap, marker='x', vmin=y_min, vmax=y_max)
# plt.ylim(-shift_range, shift_range)
# plt.colorbar(im2)
# plt.grid()
# plt.savefig(os.path.join(basepath, 'xdy_colorY_integ.png'), dpi=300)
# plt.clf()
#
# flag2 = shif_data1[0].query('flag == 2')
# flag2 = flag2.reset_index(drop=True)
# y_min = min(flag2['Y'])
#
# im = plt.scatter(flag2['Y'].values, flag2['U'].values*1000, c=flag2['X'], s=1, cmap=cmap, marker='x', vmin=x_min, vmax=x_max)
# plt.yticks(range(-2, 2))
# plt.colorbar(im)
# plt.grid()
# plt.savefig(os.path.join(basepath, 'ydx_colorX.png'), dpi=300)
# plt.clf()
#
# im = plt.scatter(flag2['Y'].values, flag2['U'].values*1000, c=flag2['X'], s=1, cmap=cmap, marker='x', vmin=x_min, vmax=x_max)
# plt.yticks(range(-2, 2))
# plt.colorbar(im)
# plt.grid()
# plt.savefig(os.path.join(basepath, 'ydy_colorX.png'), dpi=300)
# plt.clf()
#
# X = []
# Y = []
# U = []
# V = []
# for i in range(y_step):
#     a = y_min + 5.0 * i
#     x = np.array(flag2.query('Y == @a')['X'].values)
#     # 端からは時まであるか確認
#     # if not len(x) < y_step - 1:
#     #     continue
#     y = np.array(flag2.query('Y == @a')['Y'].values)
#     u = np.array(flag2.query('Y == @a')['U'].values)
#     u = np.cumsum(u)  # 累積和に変更
#     v = np.array(flag2.query('Y == @a')['V'].values)
#     v = np.cumsum(v)  # 累積和に変更
#     X = np.hstack([X, x])
#     Y = np.hstack([Y, y])
#     U = np.hstack([U, u])
#     V = np.hstack([V, v])
# im1 = plt.scatter(Y, U*1000, c=X, s=1, cmap=cmap, marker='x', vmin=x_min, vmax=x_max)
# # plt.ylim(-shift_range, shift_range)
# plt.colorbar(im1)
# plt.grid()
# plt.savefig(os.path.join(basepath, 'ydx_colorX_integ.png'), dpi=300)
# plt.clf()
#
# im2 = plt.scatter(Y, V*1000, c=X, s=1, cmap=cmap, marker='x', vmin=x_min, vmax=x_max)
# # plt.ylim(-shift_range, shift_range)
# plt.colorbar(im2)
# plt.grid()
# plt.savefig(os.path.join(basepath, 'ydy_colorX_integ.png'), dpi=300)
# plt.clf()
# plt.show()

# x = []
# xdx = [[], [], []]  # average, std, integrate
# xdy = [[], [], []]  # average, std, integrate
# xdx_integ = 0
# xdy_integ = 0
# for i in range(x_step):
#     a = x_min + 9.0 * i
#     x.append(a)
#     xdx_ave = np.mean(dx_data[x_data == a])
#     xdx_std = np.std(dx_data[x_data == a])
#     xdx_integ += xdx_ave
#     xdx[0].append(xdx_ave)
#     xdx[1].append(xdx_std)
#     xdx[2].append(xdx_integ)
#
#     xdy_ave = np.mean(dy_data[x_data == a])
#     xdy_std = np.std(dy_data[x_data == a])
#     xdy_integ += xdy_ave
#     xdy[0].append(xdy_ave)
#     xdy[1].append(xdy_std)
#     xdy[2].append(xdy_integ)
# # plot ただし関数内でハードコーディングあり(x, yの目盛りなど)
# outname = os.path.join(basepath, 'xdx.png')
# mylib.plot_2dif(x, xdx[0], xdx[1], xdx[2], 'Stage X [mm]', 'dx [um]', outname)
# outname = os.path.join(basepath, 'xdy.png')
# mylib.plot_2dif(x, xdy[0], xdy[1], xdy[2], 'Stage X [mm]', 'dx [um]', outname)
#
# dataの取得
# y = []
# ydx = [[], [], []]  # average, std, integrate
# ydy = [[], [], []]  # average, std, integrate
# ydx_integ = 0
# ydy_integ = 0
# for i in range(y_step):
#     b = y_min + i * 5.0
#     y.append(b)
#     ydx_ave = np.mean(dx_data[y_data == b])
#     ydx_std = np.std(dx_data[y_data == b])
#     ydx_integ += ydx_ave
#     ydx[0].append(ydx_ave)
#     ydx[1].append(ydx_std)
#     ydx[2].append(ydx_integ)
#
#     ydy_ave = np.mean(dy_data[y_data == b])
#     ydy_std = np.std(dy_data[y_data == b])
#     ydy_integ += ydy_ave
#     ydy[0].append(ydy_ave)
#     ydy[1].append(ydy_std)
#     ydy[2].append(ydy_integ)
# # plot ただし関数内でハードコーディングあり(x, yの目盛りなど)
# outname = os.path.join(basepath, 'ydx.png')
# mylib.plot_2dif(y, ydx[0], ydx[1], ydx[2], 'Stage X [mm]', 'dx [um]', outname)
# outname = os.path.join(basepath, 'ydy.png')
# mylib.plot_2dif(y, ydy[0], ydy[1], ydy[2], 'Stage X [mm]', 'dx [um]', outname)







# fitting お試し
# X = np.array([x_data, y_data])
# popt, pcov = curve_fit(linear_z, X, dx_data)
# print(popt)



# 二つのスキャンデータを引き算する
# path1 = 'A:/Test/check_FASER/m222-pl002_30cm-1/ali.json'
# path2 = 'A:/Test/check_FASER/m222-pl002_30cm-2/ali.json'
# # path1 = 'A:/Test/check_stage/20231108_small_acrylic/ali.json'
# # path2 = 'A:/Test/check_stage/20231111_graine_acrylic/ali.json'
#
# shift_data1, int_df1, stage1 = mylib.read_ali_stage(path1)
# shift_data2, int_df2, stage2 = mylib.read_ali_stage(path2)
# # print(shift_data1[0][shift_data1[0]['V'] > 0.005])
#
# pdf = PdfPages('B:/data/powerpoint/HTS2_meeting/20231220/faser30-30_acrylicmove.pdf')
#
# # print(len(shift_data1[layer]), len(shift_data2[layer]))
# for layer in [0, 1]:
#     for flag, title in zip([1, 2], ['X overlap', 'Y overlap']):
#         marge = pd.merge(shift_data1[layer], shift_data2[layer], how="inner", on=["X", "Y"])
#         print(marge)
#
#         X = marge.query('flag_x == {}'.format(flag))['X']
#         Y = marge.query('flag_x == {}'.format(flag))['Y']
#         U = marge.query('flag_x == {}'.format(flag))['U_x'] - marge.query('flag_x == {}'.format(flag))['U_y']
#         V = marge.query('flag_x == {}'.format(flag))['V_x'] - marge.query('flag_x == {}'.format(flag))['V_y']
#         stage_x = sorted(list(set(stage1[layer]["stage_x"])))
#         stage_y = sorted(list(set(stage1[layer]["stage_y"])))
#
#         fig = plt.figure()
#         ax = fig.add_subplot(111)
#
#         mylib.plot_stage_shift_vec(ax, pdf, X, Y, U, V, stage_x, stage_y, 'layer = {} ({})'.format(layer, title))
#         mylib.plot_stage_shift_scatter(fig, pdf, X, Y, U, V, 'layer = {} ({})'.format(layer, title))
#         plt.clf()
# pdf.close()
