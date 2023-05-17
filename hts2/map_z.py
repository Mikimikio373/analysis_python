import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json

folder = 'z_map'

if os.path.exists(folder):
    print("This folder already exists. Can I overwrite it? Press \'y\' as Yes or \'n\' as No")
    answer = input()
    if answer == "y":
        os.makedirs(folder, exist_ok=True)
    else:
        print("this program ended")
        sys.exit()

else:
    os.makedirs(folder)

x_size = 18     # x方向の大きさ
y_size = 72     # y方向の大きさ
n = 0
x = np.arange(x_size + 1)
y = np.arange(y_size + 1)
L0z_top = []
L0z_bottom = []
L1z_top = []
L1z_bottom = []
L0_thick = []
L1_thick = []
base_thick = []

n_sum = x_size * y_size * 2
# xy = "xy"
for i in range(0, y_size):
    L0z_top.append([])
    L0z_bottom.append([])
    L1z_top.append([])
    L1z_bottom.append([])
    L0_thick.append([])
    L1_thick.append([])
    base_thick.append([])

while n < n_sum:
    for vy in range(0, y_size):
        for layer in range(0, 2):
            for vx in range(0, x_size):
                json_file = open('V{0:08}_L{1}_VX{2:04}_VY{3:04}_0_016.json'.format(n, layer, vx, vy), 'r')
                j = json.load(json_file)
                n += 1

                if layer == 0:
                    z_top = round(j["Images"][0]["z"], 5)
                    z_bottom = round(j["Images"][-1]["z"], 5)
                    thick = z_top - z_bottom
                    L0z_top[vy].append(z_top)
                    L0z_bottom[vy].append(z_bottom)
                    L0_thick[vy].append(thick)
                else:
                    z_top = round(j["Images"][0]["z"], 5)
                    z_bottom = round(j["Images"][-1]["z"], 5)
                    thick = z_top - z_bottom
                    L1z_top[vy].append(z_top)
                    L1z_bottom[vy].append(z_bottom)
                    L1_thick[vy].append(thick)

                print('V{0:08}_L{1}_VX{2:04}_VY{3:04}_0_016.json ended'.format(n, layer, vx, vy))
                json_file.close()

for vx in range(0, x_size):
    for vy in range(0, y_size):
        base = L0z_bottom[vy][vx] - L1z_top[vy][vx]
        base_thick[vy].append(base)

plt.pcolormesh(x, y, L0z_top, cmap=cm.jet)
pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
pp.set_label("height [mm]", fontname="Arial", fontsize=16)  # カラーバーのラベル
plt.title('L0 z top', fontsize=20)
plt.xlabel('X position', fontsize=16)
plt.ylabel('Y position', fontsize=16)
# plt.show()
plt.savefig(os.path.join(folder, 'zmap_L0_top.png'))
plt.clf()

plt.pcolormesh(x, y, L0z_bottom, cmap=cm.jet)
pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
pp.set_label("height [mm]", fontname="Arial", fontsize=16)  # カラーバーのラベル
plt.title('L0 z bottom', fontsize=20)
plt.xlabel('X position', fontsize=16)
plt.ylabel('Y position', fontsize=16)
# plt.show()
plt.savefig(os.path.join(folder, 'zmap_L0_bottom.png'))
plt.clf()

plt.pcolormesh(x, y, L1z_top, cmap=cm.jet)
pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
pp.set_label("height [mm]", fontname="Arial", fontsize=16)  # カラーバーのラベル
plt.title('L1 z top', fontsize=20)
plt.xlabel('X position', fontsize=16)
plt.ylabel('Y position', fontsize=16)
# plt.show()
plt.savefig(os.path.join(folder, 'zmap_L1_top.png'))
plt.clf()

plt.pcolormesh(x, y, L1z_bottom, cmap=cm.jet)
pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
pp.set_label("height [mm]", fontname="Arial", fontsize=16)  # カラーバーのラベル
plt.title('L1 z bottom', fontsize=20)
plt.xlabel('X position', fontsize=16)
plt.ylabel('Y position', fontsize=16)
# plt.show()
plt.savefig(os.path.join(folder, 'zmap_L1_bottom.png'))
plt.clf()

plt.pcolormesh(x, y, L0_thick, cmap=cm.jet)
pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
pp.set_label("thickness [mm]", fontname="Arial", fontsize=16)  # カラーバーのラベル
plt.title('L0 thickness', fontsize=20)
plt.xlabel('X position', fontsize=16)
plt.ylabel('Y position', fontsize=16)
# plt.show()
plt.savefig(os.path.join(folder, 'zmap_L0_thick.png'))
plt.clf()

plt.pcolormesh(x, y, L1_thick, cmap=cm.jet)
pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
pp.set_label("thickness [mm]", fontname="Arial", fontsize=16)  # カラーバーのラベル
plt.title('L1 thickness', fontsize=20)
plt.xlabel('X position', fontsize=16)
plt.ylabel('Y position', fontsize=16)
# plt.show()
plt.savefig(os.path.join(folder, 'zmap_L1_thick.png'))
plt.clf()

plt.pcolormesh(x, y, base_thick, cmap=cm.jet)
pp = plt.colorbar(orientation="vertical")  # カラーバーの表示
pp.set_label("thickness [mm]", fontname="Arial", fontsize=16)  # カラーバーのラベル
plt.title('base thickness', fontsize=20)
plt.xlabel('X position', fontsize=16)
plt.ylabel('Y position', fontsize=16)
# plt.show()
plt.savefig(os.path.join(folder, 'zmap_base_thick.png'))
plt.clf()


