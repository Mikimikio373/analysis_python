import numpy as np
import sys
import os
import pandas as pd
import pandas as pn
import json
import math
import yaml

basepath = 'R:\\minami\\20221103_zabuton'
type_max = 1 + 1
module_max = 1 + 1
ver_max = 1 + 1
shift_x = 40
shift_y = 20

for n_t in range(1, type_max):
    for n_m in range(1, module_max):
        for n_v in range(1, ver_max):
            type = 'type{}'.format(n_t)
            module = 'Module{}'.format(n_m)
            version = 'ver-{}'.format(n_v)
            area = 'E'
            areapath = os.path.join(basepath, type, module, version, area)
            if not os.path.exists(areapath):
                continue
            yaml_path = os.path.join(areapath, 'AreaScan4Param.yml')
            with open(yaml_path, 'rb') as yml:
                param = yaml.safe_load(yml)
            npicture = param["NPictures"]
            view_x = param["Area"][0]["NViewX"]
            view_y = param["Area"][0]["NViewY"]
            fit_csv = os.path.join(areapath, 'GrainMatching_loop/fitdata.csv')

            fit_pn = pn.read_csv(fit_csv, header=0)
            # エンコーダ情報の取得
            dsX_all = []
            dsY_all = []
            dx_all = []
            dy_all = []
            n = 0
            view = 0
            base_json_path = areapath + '/IMAGE00_AREA-1/V{:08}_L0_VX0000_VY0000_0_{:03}.json'.format(view, npicture)
            for vy in range(0, shift_y):
                for vx in range(0, shift_x):
                    if (vx == 0 and vy == 0):
                        continue
                    view = view_x * vy + vx + n
                    json_path = areapath + '/IMAGE00_AREA-1/V{:08}_L0_VX{:04}_VY{:04}_0_{:03}.json'.format(view, vx, vy,
                                                                                                           npicture)
                    # print(json_path)

                    # スキャンデータがない時の処理
                    if not os.path.exists(json_path):
                        print('json not exist: ', json_path)
                        dsX = 'none'
                        dsY = 'none'
                        dsX_all.append(dsX)
                        dsX_all.append(dsY)
                        continue

                    base_json = open(base_json_path, 'r')
                    json_open = open(json_path, 'r')
                    j = json.load(json_open)
                    base_j = json.load(base_json)
                    base_json.close()
                    json_open.close()

                    base_sX = base_j['Images'][0]['x']
                    base_sY = base_j['Images'][0]['y']
                    sX = j['Images'][0]['x']
                    sY = j['Images'][0]['y']

                    dsX = sX - base_sX
                    dsY = sY - base_sY
                    # print(dsX, dsY)

                    dsX_all.append(dsX)
                    dsY_all.append(dsY)

                view = view_x * (vy + 1) + n
                n += 1
                base_json_path = areapath + '/IMAGE00_AREA-1/V{:08}_L0_VX0000_VY0000_0_{:03}.json'.format(view, npicture)
                # print(base_json_path)

            fit_pn['dX'] = dsX_all
            fit_pn['dY'] = dsY_all


            # 統計数の少ないデータ(うまくフィッティングできていないデータ)の削除
            drop_line = []
            for a in range(0, len(fit_pn)):
                if fit_pn['Entries'][a] < 80:
                    drop_line.append(a)
                if fit_pn['sigmaX'][a] > 0.5:
                    drop_line.append(a)
                if fit_pn['sigmaY'][a] > 0.5:
                    drop_line.append(a)
                #フィッティングした時のシグマ値とエントリーから誤差を計算
                dx = fit_pn['sigmaX'][a] / math.sqrt(fit_pn['Entries'][a])
                dy = fit_pn['sigmaY'][a] / math.sqrt(fit_pn['Entries'][a])
                dx_all.append(dx)
                dy_all.append(dy)

            fit_pn['dx'] = dx_all
            fit_pn['dy'] = dy_all
            fit_pn = fit_pn.drop(fit_pn.index[drop_line])
            fit_pn = fit_pn.reset_index(drop=True)
            print(len(fit_pn))

            ###
            ###
            # ファイルの整理
            ###
            ###


            fit_pn.to_csv(areapath + '/GrainMatching_loop/fitdata_edit.csv')
