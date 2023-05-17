import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json

folder = 'z_dist'

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

x_size = 4     # x方向の大きさ
y_size = 8     # y方向の大きさ
n = 0
n_picture = 16
x = np.arange(n_picture - 1)
n_sum = x_size * y_size
z0 = []
z1 = []
for ay in range(0, y_size):
    z0.append([])
    z1.append([])
    for ax in range(0, x_size):
        z0[ay].append([])
        z1[ay].append([])
while n < n_sum:
    for vy in range(0, y_size):
        for layer in range(0, 2):
            for vx in range(0, x_size):
                json_file = open('V{0:08}_L{1}_VX{2:04}_VY{3:04}_0_{4:03}.json'.format(n, layer, vx, vy, n_picture), 'r')
                j = json.load(json_file)
                n += 1
                if layer == 0:
                    for i in range(0, len(j["Images"]) - 1):
                        dist = round((j["Images"][i]["z"] - j["Images"][i + 1]["z"]), 6) * pow(10, 3)
                        z0[vy][vx].append(dist)
                    print("V{0:08}_L{1}_VX{2:04}_VY{3:04} ended".format(n, layer, vx, vy))
                else:
                    for i in range(0, len(j["Images"]) - 1):
                        dist = round((j["Images"][i]["z"] - j["Images"][i + 1]["z"]), 6) * pow(10, 3)
                        z1[vy][vx].append(dist)
                    print("V{0:08}_L{1}_VX{2:04}_VY{3:04} ended".format(n, layer, vx, vy))


for ay in range(0, y_size):
    for ax in range(0, x_size):
        plt.plot(x, z0[ay][ax], marker="o")

plt.title('one step z distance VY={0} VX={1}~{2}'.format(ay, 0, x_size - 1), fontsize=20)
plt.xlabel('x position(0 = z[0] - z[1])', fontsize=16)
plt.ylabel('z distance', fontsize=16)
# plt.ylim(3.9, 4.2)
# plt.show()
plt.savefig(os.path.join(folder, 'dist.png'.format(ay)))
plt.clf()
