import json
import copy
import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import yaml
import numpy as np

red_bird   = [ 0.2082, 0.0592, 0.0780, 0.0232, 0.1802, 0.5301, 0.8186, 0.9956, 0.9764]
green_bird = [ 0.1664, 0.3599, 0.5041, 0.6419, 0.7178, 0.7492, 0.7328, 0.7862, 0.9832]
blue_bird  = [ 0.5293, 0.8684, 0.8385, 0.7914, 0.6425, 0.4662, 0.3499, 0.1968, 0.0539]
cdict_bird = dict([(key,tuple([(i/8,val,val) for i,val in enumerate(eval(key+"_bird"))])) for key in ["red","green","blue"]])
cmap_bird = matplotlib.colors.LinearSegmentedColormap('bird', cdict_bird)


with open('sensor_pos.yml', 'r') as f:
    pos_list = yaml.safe_load(f)
pos_list = sorted(pos_list, key=lambda x: x['pos'])


with open('AffineParam.json', 'r') as f:
    affparam = json.load(f)

# aff読み込み
aff = []
for i in range(24):
    aff.append([affparam[i]['Aff_coef'][0], affparam[i]['Aff_coef'][1], affparam[i]['Aff_coef'][2], affparam[i]['Aff_coef'][3]])


# plot shrink
shrink = []
for i in range(len(aff)):
    shrink.append((abs(aff[i][0]) + abs(aff[i][3])) / 2)

x = np.arange(1, 8+1)
y = np.arange(1, 9+1)
x, y = np.meshgrid(x, y)
shrink_map = np.zeros((9, 8))
for yi in range(9):
    for xi in range(8):
        pos = xi + yi * 8
        imager = pos_list[pos]['id']
        if imager > 23:
            continue
        shrink_map[yi][xi] = shrink[imager] / max(shrink)

fig = plt.figure(tight_layout=True)
ax = fig.add_subplot(111)
cmap_bird.set_under('w', 0.1) # 下限以下の色を設定
z_ber = ax.pcolormesh(x, y, shrink_map, cmap=cmap_bird, vmin=0.9975, vmax=1.0, edgecolors="black")
divider = make_axes_locatable(ax)  # axに紐付いたAxesDividerを取得
cax = divider.append_axes("right", size="5%", pad=0.1)  # append_axesで新しいaxesを作成
fig.colorbar(z_ber, orientation="vertical", cax=cax)
# plt.gca().set_aspect(1/2)
# plt.show()
plt.savefig('shrink.png', dpi=300)
plt.clf()


# plot rotation
rot = []
for i in range(len(aff)):
    r_abs = (abs(aff[i][1]) + abs(aff[i][2])) / 2 / shrink[i]
    r = r_abs * (aff[i][2] / abs(aff[i][2])) * -1.0  # xのみ反転か、xy両方反転しかないため、cは常にマイナス
    rot.append(r)

x = np.arange(1, len(aff)+1)
plt.plot(x, np.array(rot)*1000, 'x', ms=8, mew=2)
plt.xticks(x, fontsize=12)
plt.yticks(range(-6, 7), fontsize=12)
plt.xlabel('Imager ID', fontsize=16)
plt.ylabel('回転量 [mrad]', fontsize=16, fontname="MS Gothic")
plt.grid()
print(np.average(rot[:12])*1000, np.average(rot[12:])*1000)
# plt.show()
plt.savefig('rotation.png', dpi=300)
