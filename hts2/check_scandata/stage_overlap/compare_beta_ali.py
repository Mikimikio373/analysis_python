import json

import matplotlib.pyplot as plt
import numpy as np

json1 = 'A:/Test/check_FASER/m222-pl002_30cm-1/Beta_EachViewParam.json'
json2 = 'A:/Test/check_FASER/m222-pl002_30cm-1/Beta_EachViewParam_cubic.json'

with open(json1, 'rb') as f:
    eachview1 = json.load(f)

with open(json2, 'rb') as f:
    eachview2 = json.load(f)

print(len(eachview1), len(eachview2))
x = []
y = []
u = []
v = []

for i in range(len(eachview1)):
    x.append(eachview1[i]['Stage_x'])
    y.append(eachview1[i]['Stage_y'])
    u.append(eachview2[i]['Stage_x'] - eachview1[i]['Stage_x'])
    v.append(eachview2[i]['Stage_y'] - eachview1[i]['Stage_y'])
    # print(eachview2[i]['Stage_x'] - eachview1[i]['Stage_x'], eachview2[i]['Stage_y'] - eachview1[i]['Stage_y'])

factor = 2000.0
guide = 0.005
plt.quiver(x, y, np.array(u) * factor, np.array(v) * factor, angles='xy', scale_units='xy', scale=1, units='xy', width=0.1)
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
# pdf.savefig()
# plt.clf()
plt.show()
