import numpy as np
import cv2
import sys
import os
import pandas as pn
import yaml
import itertools

# basepath = 'R:\\minami\\20230213_Reversal\\4-6\\PL005'
basepath = 'Q:/minami/20230810_ali-z/Module1/sensor-7/pich0.5um-1'

# for pl in range(5, 8):
for pl in range(1):
    os.chdir(basepath)

    # pl_path = '../PL{:03}'.format(pl)
    # if not os.path.exists(pl_path):
    #     continue
    # os.chdir(pl_path)
    current_dir = os.getcwd()
    print('now dir: ', current_dir)
    yaml_path = 'AreaScan4Param.yml'
    with open(yaml_path, 'rb') as yml:
        param = yaml.safe_load(yml)
    yml.close()
    picture_snap = param["NPictures"]
    txt_name = 'all.txt'
    with open('all.txt', 'r') as txt:
        t = txt.readlines()
    txt.close()


    nog_all = []

    for i in range(0, len(t)):
        if not t[i][0] == '0':  # 先頭が0じゃないとスキャンのlogじゃないからpass、表面探査モードとか
            continue
        line = t[i].split('{')[1]
        line = line.split('}')[0]
        surface = line.split('\"Surface\":')
        surface = surface[1].split('\"')[1]
        if not surface == 'good':   # "good"じゃないとスキャンデータとして画像を保存していないからpass
            continue

        # txtから欲しい情報の抽出
        layer = line.split('\"Layer\":')[1]
        layer = int(layer.split(',')[0])
        first = line.split('\"First\":')[1]
        first = int(first.split(',')[0])
        last = line.split('\"Last\":')[1]
        last = int(last.split(',')[0])
        viewX = line.split('\"ViewX\":')[1]
        viewX = int(viewX.split(',')[0])
        viewY = line.split('\"ViewY\":')[1]
        viewY = int(viewY.split(',')[0])
        nog = line.split('\"Nogs\":[')[1]
        nog = nog.split('],\"Now\"')[0]
        nog = nog.split(',')
        nog_int = [int(i) for i in nog]
        nog_line = [layer, viewX, viewY, first,last]
        for snap in range(0, len(nog_int)):
            nog_line.append(nog_int[snap])
        nog_all.append(nog_line)

    snap_col = np.arange(1, picture_snap + 1)
    columns = ['layer', 'viewX', 'viewY', 'first', 'last'] + [str(t) for t in snap_col]
    index = []

    n = 0

    nog_panda = pn.DataFrame(nog_all)
    # nog_panda.index = index
    nog_panda.columns = columns
    nog_panda.to_csv('nog_data.csv')


