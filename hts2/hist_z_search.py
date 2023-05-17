import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json
import pandas as pn


working_directory = '../'
nog_panda = pn.read_csv('../nog_data_a.csv', header=0, index_col=0)

os.chdir(working_directory)
directory = os.getcwd()
print('directory changed, current directory =', directory)

folder = 'hist_z_search1'

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
L0_thick = []
L1_thick = []
base_thick = []
L0z_bottom = []
L1z_top = []

for i in range(0, y_size):
    L0z_bottom.append([])
    L1z_top.append([])


n_sum = x_size * y_size * 2
while n < n_sum:
    for vy in range(0, y_size):
        for layer in range(0, 2):
            for vx in range(0, x_size):
                json_file = open('IMAGE00_AREA-1/V{0:08}_L{1}_VX{2:04}_VY{3:04}_0_024.json'.format(n, layer, vx, vy), 'r')
                j = json.load(json_file)
                index_name = 'L{}_VX{:04}_VY{:04}'.format(layer, vx, vy)
                n += 1

                first = nog_panda.loc[index_name]['first']
                last = nog_panda.loc[index_name]['last']
                z_top = round(j["Images"][first]["z"], 5)
                z_bottom = round(j["Images"][last]["z"], 5)
                thick = z_top - z_bottom
                if layer == 0:
                    L0z_bottom[vy].append(z_bottom)
                    L0_thick.append(thick)
                elif layer == 1:
                    L1z_top[vy].append(z_top)
                    L1_thick.append(thick)

                print('V{0:08}_L{1}_VX{2:04}_VY{3:04}.json ended'.format(n - 1, layer, vx, vy))
                json_file.close()

for vx in range(0, x_size):
    for vy in range(0, y_size):
        base = L0z_bottom[vy][vx] - L1z_top[vy][vx]
        base_thick.append(base)


plt.hist(base_thick, bins=36)
plt.title('base thickness (histogram)', fontsize=20)
plt.xlabel('base thickness [mm]', fontsize=16)
plt.ylabel('Entries', fontsize=16)
# plt.show()
plt.savefig(os.path.join(folder, 'base_thick_hist.png'))
plt.clf()

plt.hist(base_thick, bins=36, log=True)
plt.title('base thickness (histogram)', fontsize=20)
plt.xlabel('base thickness [mm]', fontsize=16)
plt.ylabel('Entries', fontsize=16)
# plt.show()
plt.savefig(os.path.join(folder, 'base_thick_hist_log.png'))
plt.clf()

base_panda = pn.DataFrame(base_thick)
base_panda.columns = ['base_thick']
base_panda.to_csv(os.path.join(folder, 'base.csv'))

np.savetxt(os.path.join(folder, 'base.txt'), base_thick)
