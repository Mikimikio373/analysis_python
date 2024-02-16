import copy
import json
import csv

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages

import check_stage_module as mymod


def read_fitparam(path: str):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    coef = [[], []]
    for j in range(len(coef)):
        for i in range(len(l[2 * j + 1])):
            coef[j].append(float(l[2 * j + 1][i]))

    dx, dy = coef
    return dx, dy


def quadratic_2var(x, y, coef):
    a, b, c, d, e, f = coef
    z = a * x * x + b * y * y + c * x * y + d * x + e * y + f
    return z


def cubic_2var(x, y, coef):
    a, b, c, d, e, f, g, h, i, j = coef
    z = a * x * x * x + b * y * y * y + c * x * x * y + d * x * y * y + e * x * x + f * y * y + g * x * y + h * x + i * y + j
    return z

def fit_cubic_2var(xy_array, a, b, c, d, e, f, g, h, i, j):
    x, y = xy_array
    z = a * x * x * x + b * y * y * y + c * x * x * y + d * x * y * y + e * x * x + f * y * y + g * x * y + h * x + i * y + j
    return z.ravel()


def fit_linear_2var(xy_array, a, b, c):
    x, y = xy_array
    z = a * x + b * y + c
    return z.ravel()


tar_dir = 'A:/Test/check_FASER/m222-pl002_30cm-1'
fit_param_path = 'A:/Test/check_FASER/m222-pl002_30cm-1/fit_stage_ycut_cubic_scale/ali_stage_fittig-data.csv'

coef_dx, coef_dy = read_fitparam(fit_param_path)
ali_stage = mymod.read_ali_stage_raw('ali.json')
step_x = 9
step_y = 5
xmin = 0
xmax = 288
ymin = 0
ymax = 245
# ymax = 210
print(xmin, xmax, ymin, ymax)
x = np.arange(xmin, xmax + 1, step_x)
y = np.arange(ymin, ymax + 1, step_y)
# vector map書く用のリストを初期化
x, y = np.meshgrid(x, y)
u = np.zeros((len(x), len(x[0])))
v = np.zeros((len(x), len(x[0])))

# layer1で絞る
ali_stage = ali_stage[ali_stage['layer'] == 0].reset_index(drop=True)

for i in range(int((xmax - xmin) / step_x) + 1):
    print('{} / {}'.format(i, int((xmax - xmin) / step_x)))
    for j in range(int((ymax - ymin) / step_y) + 1):
        sx2 = x[j][i] - cubic_2var(x[j][i], y[j][i], coef_dx)
        sy2 = y[j][i] - cubic_2var(x[j][i], y[j][i], coef_dy)
        sx2_minus = sx2 - 0.001
        sx2_plus = sx2 + 0.001
        sy2_minus = sy2 - 0.001
        sy2_plus = sy2 + 0.001
        if i == 0 and j == 0:
            u[j][i] = 0
            v[j][i] = 0
        elif i == 0:  # xが左端の時
            # Yoverlap
            sx1 = x[j][i] - cubic_2var(x[j][i], y[j-1][i], coef_dx)
            sy1 = y[j - 1][i] - cubic_2var(x[j][i], y[j - 1][i], coef_dy)
            sx1_minus = sx1 - 0.001
            sx1_plus = sx1 + 0.001
            sy1_minus = sy1 - 0.001
            sy1_plus = sy1 + 0.001
            shift_x = \
            ali_stage.query('stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')['shift_x'].values
            shift_y = \
            ali_stage.query('stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')['shift_y'].values

            # データがなかった時の対処
            if len(shift_x) == 0:
                sx2_minus = sx1_minus
                sx2_plus = sx1_plus
                sy2_minus = sy1_minus
                sy2_plus = sy1_plus
                sx1 = x[j][i] - cubic_2var(x[j][i], y[j - 2][i], coef_dx)
                sy1 = y[j - 2][i] - cubic_2var(x[j][i], y[j - 2][i], coef_dy)
                sx1_minus = sx1 - 0.001
                sx1_plus = sx1 + 0.001
                sy1_minus = sy1 - 0.001
                sy1_plus = sy1 + 0.001
                shift_x = \
                    ali_stage.query(
                        'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                        'shift_x'].values
                shift_y = \
                    ali_stage.query(
                        'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                        'shift_y'].values
            u[j][i] = u[j - 1][i] + shift_x[0] * abs(sy2 - sy1) / 5.0
            v[j][i] = v[j - 1][i] + shift_y[0] * abs(sy2 - sy1) / 5.0
        elif j == 0:  # yが下端の時(ただし原点は除く)
            # Xoverlap
            sx1 = x[j][i - 1] - cubic_2var(x[j][i-1], y[j][i], coef_dx)
            sy1 = y[j][i] - cubic_2var(x[j][i-1], y[j][i], coef_dy)
            sx1_minus = sx1 - 0.001
            sx1_plus = sx1 + 0.001
            sy1_minus = sy1 - 0.001
            sy1_plus = sy1 + 0.001
            shift_x = \
                ali_stage.query(
                    'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                    'shift_x'].values
            shift_y = \
                ali_stage.query(
                    'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                    'shift_y'].values
            # データがなかった時の対処
            if len(shift_x) == 0:
                if i == 1:
                    continue
                sx2_minus = sx1_minus
                sx2_plus = sx1_plus
                sy2_minus = sy1_minus
                sy2_plus = sy1_plus
                sx1 = x[j][i - 2] - cubic_2var(x[j][i - 2], y[j][i], coef_dx)
                sy1 = y[j][i] - cubic_2var(x[j][i - 2], y[j][i], coef_dy)
                sx1_minus = sx1 - 0.001
                sx1_plus = sx1 + 0.001
                sy1_minus = sy1 - 0.001
                sy1_plus = sy1 + 0.001
                shift_x = \
                    ali_stage.query(
                        'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                        'shift_x'].values
                shift_y = \
                    ali_stage.query(
                        'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                        'shift_y'].values
            u[j][i] = u[j][i - 1] + shift_x * abs(sx2 - sx1) / 9.0
            v[j][i] = v[j][i - 1] + shift_y * abs(sx2 - sx1) / 9.0
        else:
            # Yoverlap
            sx1 = x[j][i] - cubic_2var(x[j][i], y[j - 1][i], coef_dx)
            sy1 = y[j - 1][i] - cubic_2var(x[j][i], y[j - 1][i], coef_dy)
            sx1_minus = sx1 - 0.001
            sx1_plus = sx1 + 0.001
            sy1_minus = sy1 - 0.001
            sy1_plus = sy1 + 0.001
            shift_x1 = \
                ali_stage.query(
                    'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                    'shift_x'].values
            shift_y1 = \
                ali_stage.query(
                    'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                    'shift_y'].values
            # Xoverlap
            sx1 = x[j][i - 1] - cubic_2var(x[j][i - 1], y[j][i], coef_dx)
            sy1 = y[j][i] - cubic_2var(x[j][i - 1], y[j][i], coef_dy)
            sx1_minus = sx1 - 0.001
            sx1_plus = sx1 + 0.001
            sy1_minus = sy1 - 0.001
            sy1_plus = sy1 + 0.001
            shift_x2 = \
                ali_stage.query(
                    'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                    'shift_x'].values
            shift_y2 = \
                ali_stage.query(
                    'stage_x1>@sx1_minus & stage_x1<@sx1_plus & stage_x2>@sx2_minus & stage_x2<@sx2_plus & stage_y1>@sy1_minus & stage_y1<@sy1_plus & stage_y2>@sy2_minus & stage_y2<@sy2_plus')[
                    'shift_y'].values
            if len(shift_x1) == 0 or len(shift_x2) == 0 or len(shift_y1) == 0 or len(shift_y2) == 0:
                u[j][i] = (u[j - 1][i] + u[j][i]) / 2.0
                v[j][i] = (v[j - 1][i] + v[j][i]) / 2.0
                continue
            u[j][i] = ((u[j - 1][i] + shift_x1[0] * abs(sy2 - sy1) / 5.0) + (u[j][i - 1] + shift_x2[0] * abs(sx2 - sx1) / 9.0)) / 2.0  # (Yoverlap + Xoverlap) /2
            v[j][i] = ((v[j - 1][i] + shift_y1[0] * abs(sy2 - sy1) / 5.0) + (v[j][i - 1] + shift_y2[0] * abs(sx2 - sx1) / 9.0)) / 2.0  # (Yoverlap + Xoverlap) /2

pdf = PdfPages('A:/Test/check_FASER/m222-pl002_30cm-1/ali_stage_integ_after.pdf')
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
plt.title('edit data')
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
plt.title('edit data')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(x, v * 1000, c=y, s=1, cmap=cmap, marker='x', vmin=ymin, vmax=ymax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageY [mm]')
plt.xlabel('StageX [mm]')
plt.ylabel('dy [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('edit data')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(y, u * 1000, c=x, s=1, cmap=cmap, marker='x', vmin=xmin, vmax=xmax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageX [mm]')
plt.xlabel('StageY [mm]')
plt.ylabel('dx [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('edit data')
pdf.savefig()
plt.clf()

cmap = plt.get_cmap('jet')
im = plt.scatter(y, v * 1000, c=x, s=1, cmap=cmap, marker='x', vmin=xmin, vmax=xmax)
plt.ylim(-shift_range, shift_range)
plt.colorbar(im, label='StageX [mm]')
plt.xlabel('StageY [mm]')
plt.ylabel('dy [um]  (origin X=0, Y=0)')
plt.grid()
plt.title('edit data')
pdf.savefig()
plt.clf()

xy = np.array([x, y])
u_flat = u.ravel()
popt_u, pcov_u = curve_fit(fit_cubic_2var, xy, u_flat)  # param_initを指定することもできる
perr_u = np.sqrt(np.diag(pcov_u))
u_fit = cubic_2var(x, y, popt_u)

v_flat = v.ravel()
popt_v, pcov_v = curve_fit(fit_cubic_2var, xy, v_flat)
perr_v = np.sqrt(np.diag(pcov_v))
v_fit = cubic_2var(x, y, popt_v)

plt.quiver(x.ravel(), y.ravel(), u_fit * factor, v_fit * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
# 凡例を描画
guide_x = np.min(x) - (np.max(x) - np.min(x)) * 0.05
guide_y = np.min(y) - (np.max(y) - np.min(y)) * 0.05
plt.quiver(guide_x, guide_y, guide * factor, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
plt.quiver(guide_x, guide_y, 0, guide * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=0.4)
plt.text(guide_x, guide_y, f" {guide * 1000} um", va="bottom", ha="left")

plt.gca().set_aspect('equal')
plt.xlabel("Stage X [mm]")
plt.ylabel("Stage Y [mm]")
plt.title('liner fit')
pdf.savefig()
plt.clf()

pdf.close()

fit_csv = 'A:/Test/check_FASER/m222-pl002_30cm-1/ali_stage_integ_fit.csv'
fit_index_cubic = 'xxx,yyy,xxy,xyy,xx,yy,xy,x,y,const'
with open(fit_csv, 'w') as f:
    f.write(fit_index_cubic+'\n')
    for i in range(len(popt_u)):
        if i == len(popt_u) - 1:
            f.write('{}\n'.format(popt_u[i]))
        else:
            f.write('{},'.format(popt_u[i]))
    # f.write(fit_index_square + '\n')
    f.write(fit_index_cubic+'\n')
    for i in range(len(popt_v)):
        if i == len(popt_v) - 1:
            f.write('{}\n'.format(popt_v[i]))
        else:
            f.write('{},'.format(popt_v[i]))
print(popt_u)
print(popt_v)
