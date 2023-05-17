import numpy as np
import sys
import os
import pandas as pn
from matplotlib import pyplot as plt
import yaml

basepath = 'R:\\minami\\20230213_Reversal\\4-6\\PL005'
# folder = 'nog_plot_snap'
folder = 'nog_plot_from_alltxt'


for pl in range(5, 8):
    os.chdir(basepath)

    pl_path = '../PL{:03}'.format(pl)
    if not os.path.exists(pl_path):
        continue
    os.chdir(pl_path)
    current_dir = os.getcwd()
    print('now dir: ', current_dir)
    yaml_path = 'AreaScan4Param.yml'
    with open(yaml_path, 'rb') as yml:
        param = yaml.safe_load(yml)
    yml.close()
    x_size = param['Area'][0]['NViewX']  # x方向の大きさ
    y_size = param["Area"][0]["NViewY"]  # y方向の大きさ
    layer = param["Area"][0]["NLayer"]
    picture_snap = param["NPictures"]
    plate_sum = layer * x_size * y_size
    nog_thr_0 = param["NogThreshold"][0]
    nog_thr_1 = param["NogThreshold"][1]

    nog_panda = pn.read_csv('nog_data.csv', header=0, index_col=0)

    os.makedirs(folder, exist_ok=True)
    os.chdir(folder)
    direct = os.getcwd()
    print('directory changed, current directory = ', direct)

    for i in range(0, len(nog_panda.values)):
        L = nog_panda["layer"][i]
        x = nog_panda["viewX"][i]
        y = nog_panda["viewY"][i]
        first = nog_panda['first'][i]
        last = nog_panda['last'][i]
        index_name = 'L{0}_VX{1:04}_VY{2:04}'.format(L, x, y)
        plt.scatter(np.arange(1, picture_snap + 1), nog_panda.loc[i][5:5+picture_snap].values)
        plt.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.95)
        plt.title(index_name)
        plt.xlabel('picture number \n ←lens         stage→')
        plt.ylabel('Number of grains')
        plt.xlim([0, picture_snap + 1])  # x軸の範囲
        plt.xticks(np.arange(0, picture_snap + 2, 1))  # x軸の最小単位
        if L == 0:
            plt.axhline(y=nog_thr_0, color='blue')
        elif L == 1:
            plt.axhline(y=nog_thr_1, color='blue')
        plt.axvline(x=first, color='red')
        plt.axvline(x=last, color='red')
        # plt.show()
        plt.savefig('nog_plot_{}.png'.format(index_name), dpi=600)
        # sys.exit()
        plt.clf()
        print(index_name, 'ended')


