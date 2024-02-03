import math
import os.path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calc_rot(a, b, c, d):
    value = (abs(b) + abs(c)) / (abs(a) + abs(d))
    pm = - c / abs(c)
    return value * pm


def calc_rot_err(a, b, c, d, a_err, b_err, c_err, d_err):
    out = math.sqrt(((b+c)/(a+d))*((b+c)/(a+d)) * (a_err*a_err + d_err*d_err) + b_err*b_err + c_err*c_err) / (a+d)
    return out


basepath = 'Q:/minami/affine_param'
rot = []
rot_err = []
module = 0
sensor = 0
for module in range(2):
    for sensor in range(12):
        tar_csv = os.path.join(basepath, '{}-{:02}_aff.csv'.format(module, sensor))

        df = pd.read_csv(tar_csv)
        rot.append(calc_rot(df['a'][0], df['b'][0], df['c'][0], df['d'][0]))
        rot_err.append(calc_rot_err(abs(df['a'][0]), abs(df['b'][0]), abs(df['c'][0]), abs(df['d'][0]), abs(df['a_err'][0]), abs(df['b_err'][0]), abs(df['c_err'][0]), abs(df['d_err'][0])))

print(np.array(rot_err)*1000)
plt.figure(tight_layout=True)
x = np.arange(1, len(rot)+1)
plt.errorbar(x, np.array(rot)*1000, yerr=np.array(rot_err)*1000, ls='None', marker='x', ms=8, mew=2)
plt.xticks(x, fontsize=12)
plt.yticks(range(-6, 7), fontsize=12)
plt.xlabel('Imager ID', fontsize=16)
plt.ylabel('回転量 [mrad]', fontsize=16, fontname="MS Gothic")
plt.grid()
# print(np.average(rot[:12])*1000, np.average(rot[12:])*1000)
plt.show()