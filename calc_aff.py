import numpy as np
import sys
import os
import pandas as pd
import pandas as pn
import json
import math
import yaml

# pythonpath = 'R:\\minami\\20220921_forGrainMaching0.025\\analysis_python'
basepath = 'R:\\minami\\20221103_zabuton'
# exepath = 'C:\\Users\\flab\\source\\repos\\myproject\\x64\\Release\\GrainMatching_r.exe'
# rootpath = 'R:\\minami\\20220921_forGrainMaching0.025\\root\\cut_fit.C'
type_max = 1 + 1
module_max = 2 + 1
ver_max = 5 + 1

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
            fit_csv = os.path.join(areapath, 'GrainMatching_loop/fitdata.csv')

            fit_pn = pn.read_csv(fit_csv, header=0)
            # fit_pn = fit_pn.drop(columns='entriesY')
            # print(fit_pn)
            print(len(fit_pn))
            # 統計数の少ないデータ(うまくフィッティングできていないデータ)の削除
            drop_line = []
            for a in range(0, len(fit_pn)):
                if fit_pn['Entries'][a] < 80:
                    drop_line.append(a)
                if fit_pn['sigmaX'][a] > 0.5:
                    drop_line.append(a)
                if fit_pn['sigmaY'][a] > 0.5:
                    drop_line.append(a)
            fit_pn = fit_pn.drop(fit_pn.index[drop_line])
            fit_pn = fit_pn.reset_index(drop=True)
            print(len(fit_pn))

            dsX_all = []
            dsY_all = []
            dx_all = []
            dy_all = []

            ###
            ###
            #ファイルの整理
            ###
            ###
            for i in range(0, len(fit_pn)):
                vx = fit_pn['VX'][i]
                vy = fit_pn['VY'][i]
                # viewの計算注意
                view = view_x * vy + vx
                json_path = areapath + '/IMAGE00_AREA-1/V{:08}_L0_VX{:04}_VY{:04}_0_{:03}.json'.format(view, vx, vy, npicture)
                base_json_path = areapath + '/IMAGE00_AREA-1/V00000001_L0_VX0001_VY0000_0_{:03}.json'.format(npicture)
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
                dx = fit_pn['sigmaX'][i] / math.sqrt(fit_pn['Entries'][i])
                dy = fit_pn['sigmaY'][i] / math.sqrt(fit_pn['Entries'][i])
                dx_all.append(dx)
                dy_all.append(dy)
                # print(dsX, dsY)

                dsX_all.append(dsX)
                dsY_all.append(dsY)

            fit_pn['dX'] = dsX_all
            fit_pn['dY'] = dsY_all
            fit_pn['dx'] = dx_all
            fit_pn['dy'] = dy_all

            fit_pn.to_csv(areapath + '/GrainMatching_loop/fitdata_edit.csv')


            ###
            ###
            #フィッティング用データの用意
            ###
            ###

            # dxdX = []
            # dxdY = []
            # dydX = []
            # dydY = []
            # vx_num = 1
            # vy_num = 0
            # delta_stage = 0.00001
            # for i in range(0, len(fit_pn)):
            #     if fit_pn['VX'][i] == vx_num:
            #         dxdY_line = [fit_pn['dY'][i], fit_pn['meanX'][i], delta_stage, fit_pn['dx'][i]]
            #         dydY_line = [fit_pn['dY'][i], fit_pn['meanY'][i], delta_stage, fit_pn['dy'][i]]
            #         # print(dxdY_line)
            #
            #         dxdY.append(dxdY_line)
            #         dydY.append(dydY_line)
            #     elif fit_pn['VY'][i] == vy_num:
            #         if fit_pn['Entries'][i] < 10:
            #             continue
            #         dxdX_line = [fit_pn['dX'][i], fit_pn['meanX'][i], delta_stage, fit_pn['dx'][i]]
            #         dydX_line = [fit_pn['dX'][i], fit_pn['meanY'][i], delta_stage, fit_pn['dy'][i]]
            #
            #         dxdX.append(dxdX_line)
            #         dydX.append(dydX_line)
            #     else:
            #         continue
            #
            # dxdX_pn = pd.DataFrame(dxdX)
            # dxdY_pn = pd.DataFrame(dxdY)
            # dydX_pn = pd.DataFrame(dydX)
            # dydY_pn = pd.DataFrame(dydY)
            # # print(dxdX_pn)
            # dxdX_pn.to_csv(areapath + '/GrainMatching_loop/dxdX.csv', header=False, index=False)
            # dxdY_pn.to_csv(areapath + '/GrainMatching_loop/dxdY.csv', header=False, index=False)
            # dydX_pn.to_csv(areapath + '/GrainMatching_loop/dydX.csv', header=False, index=False)
            # dydY_pn.to_csv(areapath + '/GrainMatching_loop/dydY.csv', header=False, index=False)

            # sys.exit()

