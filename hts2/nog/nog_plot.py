import numpy as np
import sys
import os
import pandas as pn
from matplotlib import pyplot as plt

working_directly = 'Q:/minami/20220309_GRAINE2018/007'
# folder = 'nog_plot_snap'
folder = 'nog_plot_v1.2'


path = os.path.join(working_directly, folder)

# nog_panda = pn.read_csv('../nog_data.csv', header=0, index_col=0)
# nog_panda = pn.read_csv('../nog_data_snap.csv', header=0, index_col=0)
# nog_panda = pn.read_csv('../nog_data_b3.csv', header=0, index_col=0)
nog_panda = pn.read_csv('../009/nog_data.csv', header=0, index_col=0)


os.chdir(working_directly)
direct = os.getcwd()
print('directory changed, current directory = ', direct)

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

os.chdir(folder)
direct = os.getcwd()
print('directory changed, current directory = ', direct)


x_size = 18     # x方向の大きさ
y_size = 37    # y方向の大きさ
picture_snap = 24

n = 0
for y in range(0, y_size):
    for L in range(0, 2):
        for x in range(0, x_size):
            index_name = 'L{0}_VX{1:04}_VY{2:04}'.format(L, x, y)
            # first = nog_panda.loc[index_name]['first'] + 1
            # last = nog_panda.loc[index_name]['last'] + 1
            plt.scatter(np.arange(1, picture_snap + 1), nog_panda.loc[index_name][0:picture_snap].values)
            plt.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.95)
            plt.title(index_name)
            plt.xlabel('picture number \n ←lens         stage→')
            plt.ylabel('Number of grains')
            plt.xlim([0, picture_snap + 1])  # x軸の範囲
            plt.xticks(np.arange(0, picture_snap + 2, 1))  # x軸の最小単位
            plt.axhline(y=10000, color='blue')
            # plt.axvline(x=first, color='red')
            # plt.axvline(x=last, color='red')
            # plt.show()
            plt.savefig('nog_plot_{}.png'.format(index_name), dpi=600)
            n += 1
            # sys.exit()
            plt.clf()
            print(index_name, 'ended')


