import numpy as np
import cv2
import sys
import os
import pandas as pn
import yaml

working_direc = 'IMAGE00_AREA-1/png'
pythonpath = 'Q:/minami/20220309_GRAINE2018/analysis_python'

for pl in reversed(range(7, 9)):
    os.chdir(pythonpath)

    pl_path = '../{:03}'.format(pl)
    os.chdir(pl_path)
    current_dir = os.getcwd()
    print('now dir: ', current_dir)
    yaml_path = 'AreaScan4Param.yml'
    with open(yaml_path, 'rb') as yml:
        param = yaml.safe_load(yml)


    os.chdir(working_direc)  # ディレクトリの変更
    path = os.getcwd()
    print('path changed.')
    print('current path =', path)

    thr = 14
    kernel_dil = np.ones((2, 2), np.uint8)
    size = 15

    x_size = param['Area'][0]['NViewX']  # x方向の大きさ
    y_size = param["Area"][0]["NViewY"]  # y方向の大きさ
    layer = param["Area"][0]["NLayer"]
    picture_snap = param["NPictures"]
    plate_sum = layer * x_size * y_size

    nog_all = []

    for i in range(0, 2 * x_size * y_size):
        nog_all.append([])

    # print(nog_all)

    columns = np.arange(1, picture_snap + 1)
    index = []

    n = 0
    for y in range(0, y_size):
        for L in range(0, 2):
            for x in range(0, x_size):
                folder2 = 'L{0}_VX{1:04}_VY{2:04}'.format(L, x, y)
                index.append(folder2)

                for layer in range(0, picture_snap):
                    path = os.path.join(folder2, 'L{0}_VX{1:04}_VY{2:04}_{3}.png'.format(L, x, y, layer))
                    if os.path.exists(path):
                        img_ori = cv2.imread(path, 0)
                        img_gaus_mk = cv2.GaussianBlur(img_ori, (size, size), 0)
                        img_sub = cv2.subtract(img_gaus_mk, img_ori)  # imgはガウシアンマスク、それからオリジナルを引く
                        img_sub = cv2.subtract(img_sub, thr)
                        ret, img_thr = cv2.threshold(img_sub, 0, 1, cv2.THRESH_BINARY)
                        nog = cv2.countNonZero(img_thr)
                        nog_all[n].append(nog)
                    else:
                        print('path error')

                n += 1
                print(folder2, 'ended')

    nog_panda = pn.DataFrame(nog_all)
    nog_panda.index = index
    nog_panda.columns = columns
    if os.path.exists('../../nog_data.csv'):
        print("This folder already exists. Can I overwrite it? Press \'y\' as Yes or \'n\' as No")
        answer = input()
        if answer == "y":
            nog_panda.to_csv('../../nog_data.csv')
        else:
            print("this program ended")
            sys.exit()
    else:
        nog_panda.to_csv('../../nog_data.csv')

    # if os.path.exists('../../nog_data_snap.csv'):
    #     print("This folder already exists. Can I overwrite it? Press \'y\' as Yes or \'n\' as No")
    #     answer = input()
    #     if answer == "y":
    #         nog_panda.to_csv('../../nog_data_snap.csv')
    #     else:
    #         print("this program ended")
    #         sys.exit()
    # else:
    #     nog_panda.to_csv('../../nog_data_snap.csv')


