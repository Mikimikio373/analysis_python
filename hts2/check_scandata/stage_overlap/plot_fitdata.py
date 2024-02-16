import csv
import os

import numpy as np
import matplotlib.pyplot as plt

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


def quad(x, y, coef):
    a, b, c, d, e, f, g, h, i, j, k, l ,m , n, o = coef
    z = a*x*x*x*x + b*y*y*y*y + c*x*x*x*y + d*x*x*y*y + e*x*y*y*y + f*x*x*x + g*y*y*y + h*x*x*y + i*x*y*y + j*x*x + k*y*y + l*x*y + m*x + n*y + o
    return z


tar_dir = 'A:/Test/check_FASER/m222-pl002_30cm-1'
fit_param_path = 'A:/Test/check_FASER/m222-pl002_30cm-1/fit_stage_quad/ali_stage_fittig-data.csv'

coef_dx, coef_dy = read_fitparam(fit_param_path)
print(coef_dx)
print(coef_dy)
x = np.arange(0, 289, 9)
# print(x)
y = np.arange(0, 251, 5)
# print(y)
x, y = np.meshgrid(x, y)
x = x.ravel()
y = y.ravel()
# u = cubic_2var(x, y, coef_dx)
# v = cubic_2var(x, y, coef_dy)
u = quad(x, y, coef_dx)
v = quad(x, y, coef_dx)

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
plt.title('Fitting result')
# plt.clf()
# plt.show()
out_png = 'A:/Test/check_FASER/m222-pl002_30cm-1/fitting_plot.png'
plt.savefig(out_png, dpi=300)

