import os.path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick

basepath = 'A:/Test/TrackMatch_full_240315/150_125_1/TrackMatching4Aff/00_00'
point_csv = os.path.join(basepath, 'edit_fit_data.csv')
surf_csv = os.path.join(basepath, 'aff.csv')

point_df = pd.read_csv(point_csv)
surf_df = pd.read_csv(surf_csv)

x = point_df.query('vy > 0')['fit_dpx'].values
y = point_df.query('vy > 0')['fit_dpy'].values
z = point_df.query('vy > 0')['dsx'].values
diff = []
for i in range(len(z)):
    diff.append((z[i] - (surf_df['a'][0]*x[i] + surf_df['b'][0]*y[i] + surf_df['p'][0]))*1000)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, diff, c='r')
ax.set_xlabel('delta px [pixel]')
ax.set_ylabel('delta py [pixel]')
ax.set_zlabel('data - fit (Stage X) [um]')
plt.show()
plt.clf()

ax = fig.add_subplot(111)
mean = np.mean(diff)
plt.hist(diff, bins=100, range=(mean - 0.001, mean + 0.001))
ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))   # こっちを先に書くこと。
ax.ticklabel_format(style="sci", axis="x", scilimits=(3, -3))   # 10^3（10の3乗）単位にする。
# plt.show()
