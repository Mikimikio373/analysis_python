import os
import sys

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from io import BytesIO
from PIL import Image
from mpl_toolkits.mplot3d import axes3d

basepath = 'Q:/minami/20230911_nog_NRKR_tilt'
csv_path = os.path.join(basepath, 'xyz_fit.csv')
surf_fit = os.path.join(basepath, 'fit_surf.csv')

if not len(sys.argv) == 3:
    sys.exit('please input mode')
mode = int(sys.argv[1])
fit_mode = int(sys.argv[2])
if fit_mode != 0 and fit_mode != 1:
    sys.exit('fit mode must be 1/0')
if mode == 0:
    if fit_mode == 1:
        out_gif = os.path.join(basepath, 'z0_fix.gif')
    else:
        out_gif = os.path.join(basepath, 'z0.gif')
elif mode == 1:
    if fit_mode == 1:
        out_gif = os.path.join(basepath, 'z1_fix.gif')
    else:
        out_gif = os.path.join(basepath, 'z1.gif')
elif mode == 2:
    if fit_mode == 1:
        out_gif = os.path.join(basepath, 'z_fix.gif')
    else:
        out_gif = os.path.join(basepath, 'z.gif')
else:
    sys.exit('mode error')

fit_df= pd.read_csv(surf_fit)
a = fit_df['a'][1]
b = fit_df['b'][1]
c = fit_df['c'][1]

def calc_fit_z(x, y):
    z = a * x + b * y + c
    return z

df = pd.read_csv(csv_path)

x0 = []
y0 = []
z0 = []
zerr0 = []
x1 = []
y1 = []
z1 = []
zerr1 = []
for i in range(len(df)):
    if fit_mode == 0:
        if df['flag'][i] == 0:
            x0.append(df['x'][i])
            y0.append(df['y'][i])
            z0.append(df['z'][i])
            zerr0.append(df['z_err'][i])
        else:
            x1.append(df['x'][i])
            y1.append(df['y'][i])
            z1.append(df['z'][i])
            zerr1.append(df['z_err'][i])
    else:
        fit_z = calc_fit_z(df['x'][i], df['y'][i])
        z_fix = df['z'][i] - fit_z
        if df['flag'][i] == 0:
            x0.append(df['x'][i])
            y0.append(df['y'][i])
            z0.append(z_fix)
            zerr0.append(df['z_err'][i])
        else:
            x1.append(df['x'][i])
            y1.append(df['y'][i])
            z1.append(z_fix)
            zerr1.append(df['z_err'][i])

def render_frame(angle):
    """data の 3D 散布図を PIL Image に変換して返す"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if mode == 0 or mode == 2:
        ax.scatter(x0, y0, z0, marker='o', c='r', label='modlule0')
        for num in np.arange(0, len(zerr0)):
            ax.plot([x0[num], x0[num]], [y0[num], y0[num]], [z0[num] + zerr0[num], z0[num] - zerr0[num]], marker="_", c='r')
    if mode == 1 or mode == 2:
        ax.scatter(x1, y1, z1, marker='o', c='b', label='modlule1')
        for num in np.arange(0, len(zerr1)):
            ax.plot([x1[num], x1[num]], [y1[num], y1[num]], [z1[num] + zerr1[num], z1[num] - zerr1[num]], marker="_", c='b')
    ax.set_xlim([-4.5, 4.5])
    ax.set_ylim([-4.5, 4.5])
    ax.view_init(5, angle)
    plt.close()
    ax.legend()
    ax.set_xlabel('x [mm]')
    ax.set_ylabel('y [mm]')
    ax.set_zlabel('z [um]')
    # PIL Image に変換
    buf = BytesIO()
    fig.savefig(buf, dpi=300)
    print('agnle: {} ended'.format(angle))
    return Image.open(buf)


images = [render_frame(angle) for angle in range(180, 270, 1)]
images[0].save(out_gif, save_all=True, append_images=images[1:], duration=200, loop=0)
