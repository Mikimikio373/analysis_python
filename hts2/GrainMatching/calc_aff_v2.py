import numpy as np
import sys
import os
import pandas as pd
import pandas as pn
import json
import math
import yaml

basepath = 'R:\\minami\\20221103_zabuton'
rootpath = 'c:\\Users\\flab\\cpp_project\\root\\plot_fitting.C'
type_max = 1 + 1
module_max = 2 + 1
ver_max = 5 + 1
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

            # 統計数の少ないデータ(うまくフィッティングできていないデータ)の削除
            drop_line = []
            for a in range(0, len(fit_pn)):
                if fit_pn['Entries'][a] < 170:
                    drop_line.append(a)
                if abs(fit_pn['sigmaX'][a]) > 0.5:
                    drop_line.append(a)
                if abs(fit_pn['sigmaY'][a]) > 0.5:
                    drop_line.append(a)
                #フィッティングした時のシグマ値とエントリーから誤差を計算
                vx = fit_pn['VX'][a]
                vy = fit_pn['VY'][a]

                dx = fit_pn['sigmaX'][a] / math.sqrt(fit_pn['Entries'][a])
                dy = fit_pn['sigmaY'][a] / math.sqrt(fit_pn['Entries'][a])
                dx_all.append(dx)
                dy_all.append(dy)

                if vy == 0:
                    view_base = 0
                else:
                    view_base = (view_x + 1) * vy - 1
                base_json_path = areapath + '/IMAGE00_AREA-1/V{:08}_L0_VX0000_VY0000_0_{:03}.json'.format(view_base,
                                                                                                        npicture)
                if vy == 0:
                    view = view_base = vx
                else:
                    view = view_base + vx + 1
                json_path = areapath + '/IMAGE00_AREA-1/V{:08}_L0_VX{:04}_VY{:04}_0_{:03}.json'.format(view, vx, vy,
                                                                                                       npicture)
                # スキャンデータがない時の処理
                if not os.path.exists(base_json_path):
                    print('error! there is not base_json_path')
                    sys.exit()
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

            fit_pn['dX'] = dsX_all
            fit_pn['dY'] = dsY_all
            fit_pn['dx'] = dx_all
            fit_pn['dy'] = dy_all
            fit_pn = fit_pn.drop(fit_pn.index[drop_line])
            fit_pn = fit_pn.reset_index(drop=True)
            print(len(fit_pn))

            fit_pn.to_csv(areapath + '/GrainMatching_loop/fitdata_edit.csv')

            ##
            #root macro
            ##

            os.chdir(areapath)
            current_dir = os.getcwd()
            print('path changed. current path: {}'.format(current_dir))

            command_plot = 'root -l -q -b {}'.format(rootpath)
            os.system(command_plot)
