import copy
import json
import os.path

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages

import check_stage_module as mymod


def quadratic_2var(xy_array, a, b, c, d, e, f):
    x_data, y_data = xy_array
    z = a * x_data * x_data + b * y_data * y_data + c * x_data * y_data + d * x_data + e * y_data + f
    return z.ravel()


def cubic_2var(xy_array, a, b, c, d, e, f, g, h, i, j):
    x, y = xy_array
    z = a * x * x * x + b * y * y * y + c * x * x * y + d * x * y * y + e * x * x + f * y * y + g * x * y + h * x + i * y + j
    return z.ravel()


def gauss_2d(xy_array, A, sigma_x, sigma_y, mu_x, mu_y):
    x_data, y_data = xy_array
    z = A * np.exp(-(x_data - mu_x) ** 2 / (2 * sigma_x ** 2)) * np.exp(-(y_data - mu_y) ** 2 / (2 * sigma_y ** 2))
    return z.ravel()


fit_index_square = 'xx,yy,xy,x,y,const'
fit_index_cubic = 'xxx,yyy,xxy,xyy,xx,yy,xy,x,y,const'


taget_dir = 'A:/Test/check_FASER/m222-pl002_30cm-1'
jsonname = os.path.join(taget_dir, 'ali.json')

ali_stage = mymod.read_ali_stage_raw(jsonname)
step_x = 9
step_y = 5

# layer1で絞る
ali_stage = ali_stage[ali_stage['layer'] == 1].reset_index(drop=True)
xmin = min(ali_stage['stage_x1'])
xmax = max(ali_stage['stage_x2'])
ymin = min(ali_stage['stage_y1'])
# ymax = max(ali_stage['stage_y2'])
ymax = 210
print(xmin, xmax, ymin, ymax)
x = np.arange(xmin, xmax + 1, step_x)
y = np.arange(ymin, ymax + 1, step_y)

# vector map書く用のリストを初期化
x, y = np.meshgrid(x, y)
u = np.zeros((len(x), len(x[0])))
v = np.zeros((len(x), len(x[0])))

# stage_x1, stage_y1の順にソート
ali_stage = ali_stage.sort_values(['stage_x1', 'stage_x2', 'stage_y1']).reset_index(drop=True)

line = 0
# print(ali_stage)

print(np.max(x))

for i in range(int((xmax - xmin) / step_x) + 1):
    print('{} / {}'.format(i, int((xmax - xmin) / step_x)))
    for j in range(int((ymax - ymin) / step_y) + 1):
        sx = x[j][i]
        sy = y[j][i]
        # print(sx-9, sx, sy-5, sy)
        if i == 0 and j == 0:
            u[j][i] = 0
            v[j][i] = 0
        elif i == 0:  # xが左端の時
            sy_b = y[j - 1][i]
            # Yoverlap
            shift_x = \
            ali_stage.query('stage_x1==@sx & stage_x2==@sx & stage_y1==@sy_b &stage_y2==@sy')['shift_x'].values[0]
            shift_y = \
            ali_stage.query('stage_x1==@sx & stage_x2==@sx & stage_y1==@sy_b &stage_y2==@sy')['shift_y'].values[0]
            u[j][i] = u[j - 1][i] + shift_x
            v[j][i] = v[j - 1][i] + shift_y
        elif j == 0:  # yが下端の時(ただし原点は除く)
            sx_b = x[j][i - 1]
            # Xoverlap
            shift_x = \
            ali_stage.query('stage_x1==@sx_b & stage_x2==@sx & stage_y1==@sy &stage_y2==@sy')['shift_x'].values[0]
            shift_y = \
            ali_stage.query('stage_x1==@sx_b & stage_x2==@sx & stage_y1==@sy &stage_y2==@sy')['shift_y'].values[0]
            u[j][i] = u[j][i - 1] + shift_x
            v[j][i] = v[j][i - 1] + shift_y
        else:
            sx_b = x[j][i - 1]
            sy_b = y[j - 1][i]
            # Yoverlap
            shift_x1 = \
                ali_stage.query('stage_x1==@sx & stage_x2==@sx & stage_y1==@sy_b &stage_y2==@sy')['shift_x'].values
            shift_y1 = \
                ali_stage.query('stage_x1==@sx & stage_x2==@sx & stage_y1==@sy_b &stage_y2==@sy')['shift_y'].values
            # Xoverlap
            shift_x2 = \
                ali_stage.query('stage_x1==@sx_b & stage_x2==@sx & stage_y1==@sy &stage_y2==@sy')['shift_x'].values
            shift_y2 = \
                ali_stage.query('stage_x1==@sx_b & stage_x2==@sx & stage_y1==@sy &stage_y2==@sy')['shift_y'].values
            if len(shift_x1) == 0 or len(shift_x2) == 0 or len(shift_y1) == 0 or len(shift_y2) == 0:
                continue
            u[j][i] = ((u[j - 1][i] + shift_x1[0]) + (u[j][i - 1] + shift_x2[0])) / 2.0  # (Yoverlap + Xoverlap) /2
            v[j][i] = ((v[j - 1][i] + shift_y1[0]) + (v[j][i - 1] + shift_y2[0])) / 2.0  # (Yoverlap + Xoverlap) /2

out_pdf = os.path.join(taget_dir, 'ali_stage_dpos_fit.pdf')
pdf = PdfPages(out_pdf)

shift_range = 20
factor = 2000.0
guide = 0.005
plt.quiver(x, y, u * factor, v * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
# 凡例を描画
guide_x = np.min(x) - (np.max(x) - np.min(x)) * 0.05
guide_y = np.min(y) - (np.max(y) - np.min(y)) * 0.05
plt.quiver(guide_x, guide_y, guide * factor, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
plt.quiver(guide_x, guide_y, 0, guide * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
plt.text(guide_x, guide_y, f" {guide * 1000} um", va="bottom", ha="left")

plt.gca().set_aspect('equal')
plt.xlabel("Stage X [mm]")
plt.ylabel("Stage Y [mm]")
plt.title('data')
pdf.savefig()
plt.clf()
# plt.show()


cmap = plt.get_cmap('jet')
im = plt.scatter(x, u * 1000, c=y, s=1, cmap=cmap, marker='x', vmin=ymin, vmax=ymax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageY [mm]')
plt.xlabel('StageX [mm]')
plt.ylabel('dx [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('data')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(x, v * 1000, c=y, s=1, cmap=cmap, marker='x', vmin=ymin, vmax=ymax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageY [mm]')
plt.xlabel('StageX [mm]')
plt.ylabel('dy [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('data')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(y, u * 1000, c=x, s=1, cmap=cmap, marker='x', vmin=xmin, vmax=xmax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageX [mm]')
plt.xlabel('StageY [mm]')
plt.ylabel('dx [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('data')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(y, v * 1000, c=x, s=1, cmap=cmap, marker='x', vmin=xmin, vmax=xmax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageX [mm]')
plt.xlabel('StageY [mm]')
plt.ylabel('dy [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('data')
pdf.savefig()
plt.clf()

# fitting
xy = np.array([x, y])
u_flat = u.ravel()
popt_u, pcov_u = curve_fit(quadratic_2var, xy, u_flat)  # param_initを指定することもできる
perr_u = np.sqrt(np.diag(pcov_u))
u_fit = quadratic_2var(xy, popt_u[0], popt_u[1], popt_u[2], popt_u[3], popt_u[4], popt_u[5])

v_flat = v.ravel()
popt_v, pcov_v = curve_fit(quadratic_2var, xy, v_flat)
perr_v = np.sqrt(np.diag(pcov_v))
v_fit = quadratic_2var(xy, popt_v[0], popt_v[1], popt_v[2], popt_v[3], popt_v[4], popt_v[5])

# xy = np.array([x, y])
# u_flat = u.ravel()
# popt_u, pcov_u = curve_fit(cubic_2var, xy, u_flat)  # param_initを指定することもできる
# perr_u = np.sqrt(np.diag(pcov_u))
# u_fit = cubic_2var(xy, popt_u[0], popt_u[1], popt_u[2], popt_u[3], popt_u[4], popt_u[5], popt_u[6], popt_u[7], popt_u[8], popt_u[9])
#
# v_flat = v.ravel()
# popt_v, pcov_v = curve_fit(cubic_2var, xy, v_flat)
# perr_v = np.sqrt(np.diag(pcov_v))
# v_fit = cubic_2var(xy, popt_v[0], popt_v[1], popt_v[2], popt_v[3], popt_v[4], popt_v[5], popt_v[6], popt_v[7], popt_v[8], popt_v[9])

out_fit_txt = os.path.join(taget_dir, 'ali_stage_fittig-data.csv')
with open(out_fit_txt, 'w') as f:
    f.write(fit_index_square + '\n')
    # f.write(fit_index_cubic+'\n')
    for i in range(len(popt_u)):
        if i == len(popt_u) - 1:
            f.write('{}\n'.format(popt_u[i]))
        else:
            f.write('{},'.format(popt_u[i]))
    f.write(fit_index_square + '\n')
    # f.write(fit_index_cubic+'\n')
    for i in range(len(popt_v)):
        if i == len(popt_v) - 1:
            f.write('{}\n'.format(popt_v[i]))
        else:
            f.write('{},'.format(popt_v[i]))

x_flat = x.ravel()
y_flat = y.ravel()

# fitting plot
plt.quiver(x_flat, y_flat, u_fit * factor, v_fit * factor, angles='xy', scale_units='xy', scale=1, units='xy',
           width=0.4)
# 凡例を描画
guide_x = np.min(x) - (np.max(x) - np.min(x)) * 0.05
guide_y = np.min(y) - (np.max(y) - np.min(y)) * 0.05
plt.quiver(guide_x, guide_y, guide * factor, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
plt.quiver(guide_x, guide_y, 0, guide * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
plt.text(guide_x, guide_y, f" {guide * 1000} um", va="bottom", ha="left")

plt.gca().set_aspect('equal')
plt.xlabel("Stage X [mm]")
plt.ylabel("Stage Y [mm]")
plt.title('fitting data')
pdf.savefig()
plt.clf()

im = plt.scatter(x_flat, u_fit * 1000, c=y_flat, s=1, cmap=cmap, marker='x', vmin=ymin, vmax=ymax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageY [mm]')
plt.xlabel('StageX [mm]')
plt.ylabel('dx [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('fitting data')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(x_flat, v_fit * 1000, c=y_flat, s=1, cmap=cmap, marker='x', vmin=ymin, vmax=ymax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageY [mm]')
plt.xlabel('StageX [mm]')
plt.ylabel('dy [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('fitting data')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(y_flat, u_fit * 1000, c=x_flat, s=1, cmap=cmap, marker='x', vmin=xmin, vmax=xmax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageX [mm]')
plt.xlabel('StageY [mm]')
plt.ylabel('dx [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('fitting data')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(y_flat, v_fit * 1000, c=x_flat, s=1, cmap=cmap, marker='x', vmin=xmin, vmax=xmax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageX [mm]')
plt.xlabel('StageY [mm]')
plt.ylabel('dy [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('fitting data')
pdf.savefig()
plt.clf()

# data - fit
u_d_f = u_flat - u_fit
v_d_f = v_flat - v_fit

plt.quiver(x_flat, y_flat, u_d_f * factor, v_d_f * factor, angles='xy', scale_units='xy', scale=1, units='xy',
           width=0.4)
# 凡例を描画
guide_x = np.min(x) - (np.max(x) - np.min(x)) * 0.05
guide_y = np.min(y) - (np.max(y) - np.min(y)) * 0.05
plt.quiver(guide_x, guide_y, guide * factor, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
plt.quiver(guide_x, guide_y, 0, guide * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
plt.text(guide_x, guide_y, f" {guide * 1000} um", va="bottom", ha="left")

plt.gca().set_aspect('equal')
plt.xlabel("Stage X [mm]")
plt.ylabel("Stage Y [mm]")
plt.title('data - fitting')
pdf.savefig()
plt.clf()

im = plt.scatter(x_flat, u_d_f * 1000, c=y_flat, s=1, cmap=cmap, marker='x', vmin=ymin, vmax=ymax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageY [mm]')
plt.xlabel('StageX [mm]')
plt.ylabel('dx [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('data - fitting')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(x_flat, v_d_f * 1000, c=y_flat, s=1, cmap=cmap, marker='x', vmin=ymin, vmax=ymax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageY [mm]')
plt.xlabel('StageX [mm]')
plt.ylabel('dy [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('data - fitting')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(y_flat, u_d_f * 1000, c=x_flat, s=1, cmap=cmap, marker='x', vmin=xmin, vmax=xmax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageX [mm]')
plt.xlabel('StageY [mm]')
plt.ylabel('dx [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('data - fitting')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(y_flat, v_d_f * 1000, c=x_flat, s=1, cmap=cmap, marker='x', vmin=xmin, vmax=xmax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageX [mm]')
plt.xlabel('StageY [mm]')
plt.ylabel('dy [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('data - fitting')
pdf.savefig()
plt.clf()

pdf.close()
