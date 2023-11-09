import os
import sys
import json

import matplotlib.pyplot as plt
import yaml
import math
import hts2_plot_module as myplt


step_x = myplt.step_x
step_y = myplt.step_y

if not len(sys.argv) == 2:
    sys.exit('please enter \"target path\"')

basepath = sys.argv[1]

# sensor_exposureをたたいているコマンドから、scan_chech_toolの場所を特定
pythonpath = os.path.split(sys.argv[0])[0]
# sensorの場所情報を書いてあるフォルダを読み込み
with open(os.path.join(pythonpath, 'sensor_pos.yml'), 'rb') as f:
    y_load = yaml.safe_load(f)
y_sorted = sorted(y_load, key=lambda x: x['pos'])

ScanAreaParam = os.path.join(basepath, 'ScanAreaParam.json')
with open(ScanAreaParam, 'rb') as sap:
    sap_json = json.load(sap)
sideX = sap_json['SideX']
step_x_num = math.ceil(sideX / step_x)

mode = 0    #0: フルセンサー, 1: 1/3モード
if sap_json['Algorithm'] == 'One_Third_Half_HTS2':
    mode = 1
    print('scan algorithm: One_Third_Half_HTS2')
else:
    print('現在One_Third_Half_HTS2以外対応していません')
    sys.exit()

with open(os.path.join(basepath, 'ValidViewHistory.json'), 'rb') as f:
    vvh_json = json.load(f)

with open(os.path.join(basepath, 'PARAMS', 'UserParam.json'), 'rb') as f:
    user_json = json.load(f)
nog_thr_list = []
for i in range(int(user_json['LayerParam']['LayerNum'])):
    tmp = []
    if 'NogTop' in user_json['LayerParam']['CommonParamArray'][i]:
        tmp.append(user_json['LayerParam']['CommonParamArray'][i]['NogTop'])
    if 'NogBottom' in user_json['LayerParam']['CommonParamArray'][i]:
        tmp.append(user_json['LayerParam']['CommonParamArray'][i]['NogBottom'])
    nog_thr_list.append(tmp)

out_path = os.path.join(basepath, 'GRAPH')
if not os.path.exists(out_path):
    os.makedirs(out_path)

scan_data1, scan_data2 = myplt.initial(vvh_json, sap_json, basepath, mode)

# 実データから実際のy_step数を計算(Xは恥からは時までプロット)
if mode == 0:
    step_y_num = math.floor(len(scan_data1['excount'][1][0]) / step_x_num)
elif mode == 1:
    step_y_num = math.floor(math.floor(len(scan_data1['excount'][1][0]) / step_x_num) / 3)
else:
    step_y_num = None


outfile = os.path.join(out_path, 'scan_area_excount.png')
myplt.plot_area(scan_data1['excount'], 0.1, 1000, step_x_num, step_y_num, 'Exposure Count', y_sorted, outfile)

outfile = os.path.join(out_path, 'sensor_excount.png')
myplt.plot_sensor(scan_data1['excount'], 0.1, 1000, 'Exposure Count', y_sorted, outfile)

outfile = os.path.join(out_path, 'scan_area_nog.png')
myplt.plot_area(scan_data1['nog_over_thr'], 0.1, 60000, step_x_num, step_y_num, 'nog', y_sorted, outfile)

outfile = os.path.join(out_path, 'sensor_nog.png')
myplt.plot_sensor(scan_data1['nog_over_thr'], 0.1, 60000, 'nog', y_sorted, outfile)

outfile = os.path.join(out_path, 'scan_area_nog0.png')
myplt.plot_area(scan_data1['nog0'], 0.1, 100000, step_x_num, step_y_num, 'nog0', y_sorted, outfile)

outfile = os.path.join(out_path, 'scan_area_nog15.png')
myplt.plot_area(scan_data1['nog15'], 0.1, 100000, step_x_num, step_y_num, 'nog15', y_sorted, outfile)

outfile = os.path.join(out_path, 'scan_area_topbottom.png')
myplt.plot_area(scan_data1['top2bottom'], 0, 24, step_x_num, step_y_num, 'bottom - top', y_sorted, outfile)

outfile = os.path.join(out_path, 'sensor_topbottom.png')
myplt.plot_sensor(scan_data1['top2bottom'], 0.1, 24, 'bottom - top', y_sorted, outfile)

outfile = os.path.join(out_path, 'scan_area_not.png')
myplt.plot_area(scan_data1['not'], 0.1, 30000, step_x_num, step_y_num, 'Number Of Tracks', y_sorted, outfile)

outfile = os.path.join(out_path, 'sensor_not.png')
myplt.plot_sensor_not(scan_data1['not'], 'Number Of Tracks', y_sorted, outfile, relative_min=0.8, absolute_max=30000)

outfile = os.path.join(out_path, 'scan_area_StartPicNum.png')
myplt.plot_area(scan_data1['start_picnum'], 0, 12, step_x_num, step_y_num, 'StartPicNum', y_sorted, outfile)

outfile = os.path.join(out_path, 'sensor_StartPicNum.png')
myplt.plot_sensor(scan_data1['start_picnum'], 0.1, 12, 'StartPicNum', y_sorted, outfile)

outfile = os.path.join(out_path, 'scan_area_ThickOfLayer.png')
myplt.plot_area_view(scan_data2['ThickOfLayer'], 40, 120, step_x_num, step_y_num, 'Thick Of Layer', y_sorted, outfile)

outfile = os.path.join(out_path, 'Base_Surface.png')
myplt.plot_finez(scan_data1['fine_z'], 11100, 11700, 11300, 11900, 180, 240, step_x_num, step_y_num, 'Base Surface', y_sorted, outfile)

myplt.plot_nogall(scan_data1['nog_all'], 18, 80000, nog_thr_list, out_path)

