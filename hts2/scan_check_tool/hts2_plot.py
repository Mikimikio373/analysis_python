import os
import sys
import json
import math
import datetime

import yaml


import hts2_plot_module as mylib

step_x = mylib.step_x
step_y = mylib.step_y

# current directoryの取得
basepath = os.getcwd()

# オプション情報の取得
args = mylib.get_option()

# オプションからon offの情報を取得
flags = mylib.check_flag(args.only_plot, args.off_plot)

# sensor_exposureをたたいているコマンドから、scan_chech_toolの場所を特定
pythonpath = os.path.split(sys.argv[0])[0]

print('reading json files')
# sensorの配置情報が書いてあるymlファイルの読み込み
if os.path.exists(os.path.join(pythonpath, 'sensor_pos.yml')):
    with open(os.path.join(pythonpath, 'sensor_pos.yml'), 'rb') as f:
        y_load = yaml.safe_load(f)
    y_sorted = sorted(y_load, key=lambda x: x['pos'])
else:
    sys.exit('there is no file: {}'.format(os.path.join(pythonpath, 'sensor_pos.yml')))

# スキャンパラメータの取得
ScanControllParam = os.path.join(basepath, 'ScanControllParam.json')
if not os.path.exists(ScanControllParam):
    sys.exit('There is no file: {}'.format(ScanControllParam))
with open(ScanControllParam, 'rb') as scp:
    scp_json = json.load(scp)

#anyViewStepならstep_x step_yをjsonから取得 2024/4/11 tkawahara
if 'ViewStepX' in scp_json['ScanAreaParam']:
    step_x = scp_json['ScanAreaParam']['ViewStepX']
if 'ViewStepY' in scp_json['ScanAreaParam']:
    step_y = scp_json['ScanAreaParam']['ViewStepY']

slo_json = None
#'2Layers_Once_All_Twice_Zigzag_HTS2_AnyViewStep'の場合、ScanLinesOrigin.jsonを読み込む
if scp_json['ScanAreaParam']['Algorithm'] == '2Layers_Once_All_Twice_Zigzag_HTS2_AnyViewStep':
    ScanLinesOrigin = os.path.join(basepath, 'ScanLinesOrigin.json')
    if not os.path.exists(ScanLinesOrigin):
        sys.exit('There is no file: {}'.format(ScanLinesOrigin))
    with open(ScanLinesOrigin, 'rb') as slo:
        slo_json = json.load(slo)

#32層Scanかどうか
flags['is32layerScan'] = False
flags['thick0'] = False
flags['thick1'] = False
flags['thinOuter'] = False
flags['thinBase'] = False
if 'NPicAnalysis' in scp_json['TrackingParam']:
    if scp_json['TrackingParam']['NPicAnalysis'] == 32:
        flags['is32layerScan'] = True
        #TrackingParam[CommonParamArray][0 and 1][Alternate0 and Alternate1 and Thin16Base and Thin16Outer]がTrueの場合、32LayerScan
        if scp_json['TrackingParam']['CommonParamArray'][0]['Alternate0'] and scp_json['TrackingParam']['CommonParamArray'][1]['Alternate0']:
            flags['thick0'] = True
        if scp_json['TrackingParam']['CommonParamArray'][0]['Alternate1'] and scp_json['TrackingParam']['CommonParamArray'][1]['Alternate1']:
            flags['thick1'] = True
        if scp_json['TrackingParam']['CommonParamArray'][0]['Thin16Base'] and scp_json['TrackingParam']['CommonParamArray'][1]['Thin16Base']:
            flags['thinBase'] = True
        if scp_json['TrackingParam']['CommonParamArray'][0]['Thin16Outer'] and scp_json['TrackingParam']['CommonParamArray'][1]['Thin16Outer']:
            flags['thinOuter'] = True
        print('32LayerScan')


# スキャンエリア情報
sideX = scp_json['ScanAreaParam']['SideX']
centerX = scp_json['ScanAreaParam']['CenterX']
sideY = scp_json['ScanAreaParam']['SideY']
centerY = scp_json['ScanAreaParam']['CenterY']
layer = scp_json['ScanAreaParam']['Layer']
step_x_num = math.ceil(sideX / step_x)
step_y_num = math.ceil(sideY / step_y)
startX = centerX - float(step_x_num) / 2.0 * step_x
startY = centerY - float(step_y_num) / 2.0 * step_y
# プロットする際に使う情報
npic = scp_json['LayerParam']['CommonParamArray'][0]['NPicSnap']
thick_min = 20
thick_max = 100
nog_thr_list = []
for i in range(int(scp_json['LayerParam']['LayerNum'])):
    tmp = []
    if 'NogTop' in scp_json['LayerParam']['CommonParamArray'][i]:
        tmp.append(scp_json['LayerParam']['CommonParamArray'][i]['NogTop'])
    if 'NogBottom' in scp_json['LayerParam']['CommonParamArray'][i]:
        tmp.append(scp_json['LayerParam']['CommonParamArray'][i]['NogBottom'])
    nog_thr_list.append(tmp)

if 'MaxThickness' in scp_json['LayerParam']['CommonParamArray'][0]:
    thick_max = scp_json['LayerParam']['CommonParamArray'][0]['MaxThickness']
if 'MinThickness' in scp_json['LayerParam']['CommonParamArray'][0]:
    thick_min = scp_json['LayerParam']['CommonParamArray'][0]['MinThickness']

# スキャン方法によるプロットモードの選択
mode = 0  # 0: フルセンサー, 1: 1/3モード
if scp_json['ScanAreaParam']['Algorithm'] == 'All_Half_Zigzag_HTS2' or scp_json['ScanAreaParam']['Algorithm'] == 'All_Half_Zigzag_HTS2_AnyViewStep'\
    or scp_json['ScanAreaParam']['Algorithm'] == 'One_Half_Zigzag_HTS2' or scp_json['ScanAreaParam']['Algorithm'] =="All_Half_Zigzag_HTS2_AnyViewStep_WaitTB"\
        or scp_json['ScanAreaParam']['Algorithm']=="Benchmark_N":
    print('scan algorithm: All_Half_Zigzag_HTS2')
elif scp_json['ScanAreaParam']['Algorithm'] == '2Layers_Once_All_Twice_Zigzag_HTS2_AnyViewStep':
    print('scan algorithm: 2Layers_Once_All_Twice_Zigzag_HTS2')    
elif scp_json['ScanAreaParam']['Algorithm'] == 'One_Third_Half_HTS2':
    mode = 1
    print('scan algorithm: One_Third_Half_HTS2')
else:
    print(scp_json['ScanAreaParam']['Algorithm'] + "は描画対応していない可能性があります。")
    #print('現在One_Third_Half_HTS2以外対応していません')
    #sys.exit()

# ターゲット輝度値分布を書くためにpathとjsonデータを取得
if 'ImagerControllerParamFilePath' in scp_json['OtherPathParam']:
    evmg_path = scp_json['OtherPathParam']['ImagerControllerParamFilePath']
    with open(evmg_path, 'rb') as f:
        evmg_json = json.load(f)
else:
    evwg_json = None
    flags['bright'] = False

# scan時間取得
with open(os.path.join(basepath, 'EachScanParam.json'), 'rb') as f:
    esp_json = json.load(f)
time_first = esp_json['TimeFirst']
time_last = esp_json['TimeLast']
time_total_dt = datetime.datetime.strptime(time_last, '%Y/%m/%d %H:%M:%S') - datetime.datetime.strptime(time_first, '%Y/%m/%d %H:%M:%S')
time_total = time_total_dt.seconds
time_list = [time_first, time_last, time_total]

# VaridViewHistryの取得(プロットデータはほぼすべてここから取得している)
with open(os.path.join(basepath, 'ValidViewHistory.json'), 'rb') as f:
    vvh_json = json.load(f)

# GRAPHファイルの作成
out_path = os.path.join(basepath, 'GRAPH')
not_path = os.path.join(out_path, 'NOT')
os.makedirs(not_path, exist_ok=True)
# notdataのコピー
mylib.copy_notdata(basepath, not_path, mode)

# initialプロットするためのデータ取得
scan_data1, scan_data2, scan_data3 = mylib.initial(vvh_json, not_path, flags, layer, mode)

##'2Layers_Once_All_Twice_Zigzag_HTS2_AnyViewStep'の場合,
#slo_json[view]['Param']['Direction']が1のみのviewlistを取得
d1_list = []
if slo_json is not None:
    for i in range(len(slo_json)):
        if (slo_json[i]['Param']['Direction'] == "1" and slo_json[i]['Layer'] == 0) or (slo_json[i]['Param']['Direction'] == "2" and slo_json[i]['Layer'] == 1):
            d1_list.append(i)
#print('d1_list:', d1_list)
#scan_data1, scan_data2, scan_data3をd1_listのみ抽出
if len(d1_list) > 0:
    scan_data1, scan_data2, scan_data3 = mylib.initial(vvh_json, not_path, flags, layer, mode, d1_list)

d1_list = []
if slo_json is not None:
    count = 0
    for i in range(len(slo_json)):
        if (slo_json[i]['Param']['Direction'] == "2" and slo_json[i]['Layer'] == 1) or (slo_json[i]['Param']['Direction'] == "2" and slo_json[i]['Layer'] == 0):
            break
        count += 1
    print('count:', count)
    for i in range(len(slo_json)):
        if (slo_json[i]['Param']['Direction'] == "1" and slo_json[i]['Layer'] == 1) or (slo_json[i]['Param']['Direction'] == "1" and slo_json[i]['Layer'] == 0):
            d1_list.append(i)
    print('d1_list:', d1_list)
    d1_list_2 = []
    for i in range(len(d1_list)//count):
        temp1 = []
        temp2 = []
        for j in range(count):
            if j % 2 == 0:
                temp1.append(d1_list[i*count + j])
                #print("i*count + j:", i*count + j)
            else:
                temp2.append(d1_list[(i+1)*count - j])
                #print("i+1*count - j:", (i+1)*count- j)
        for j in temp1:
            d1_list_2.append(j)
        for j in temp2:
            d1_list_2.append(j)
    print('d1_list_2:', d1_list_2)
    d1_list = d1_list_2
if len(d1_list) > 0:
    scan_data1, scan_data2, scan_data3 = mylib.initial(vvh_json, not_path, flags, layer, mode, d1_list)

#'2Layers_Once_All_Once_Zigzag_HTS2_AnyViewStep'の場合、ScanLinesOrigin.jsonを読み込む
if scp_json['ScanAreaParam']['Algorithm'] == '2Layers_Once_All_Once_Zigzag_HTS2_AnyViewStep':
    d1_list = []
    for i in range(step_y_num):
        temp1 = []
        temp2 = []
        for j in range(step_x_num*2):
                if j % 2 == 0:
                    temp1.append(i*step_x_num*2 + j)
                else:
                    temp2.append((i+1)*step_x_num*2 - j)
        for j in temp1:
            d1_list.append(j)
        for j in temp2:
            d1_list.append(j)
    print('d1_list:', d1_list)
    if len(d1_list) > 0:
        scan_data1, scan_data2, scan_data3 = mylib.initial(vvh_json, not_path, flags, layer, mode, d1_list)

# 実データから実際のy_step数を計算(Xは端から端までプロット)
if mode == 0:
    step_y_num = math.floor(len(scan_data1['excount'][1][0]) / step_x_num)
elif mode == 1:
    step_y_num = math.floor(math.floor(len(scan_data1['excount'][1][0]) / step_x_num) / 3)
else:
    step_y_num = None


# plot開始
if flags['ex']:
    outfile = os.path.join(out_path, 'scan_area_excount.png')
    mylib.plot_area(scan_data1['excount'], args.exposure_range[0], args.exposure_range[1], step_x_num, step_y_num,
                    'Exposure Count', y_sorted, outfile, startX, startY, 0, mode)

    outfile = os.path.join(out_path, 'sensor_excount.png')
    mylib.plot_sensor(scan_data1['excount'], args.exposure_range[0], args.exposure_range[1], 'Exposure Count',
                      y_sorted, outfile)

if flags['nog']:
    outfile = os.path.join(out_path, 'scan_area_nog.png')
    mylib.plot_area(scan_data1['nog_over_thr'], args.nog_range[0], args.nog_range[1], step_x_num, step_y_num, 'Number of Grains (nog)',
                    y_sorted, outfile, startX, startY, 0, mode)

    outfile = os.path.join(out_path, 'sensor_nog.png')
    mylib.plot_sensor(scan_data1['nog_over_thr'], args.nog_range[0], args.nog_range[1], 'Number of Grains (nog)', y_sorted, outfile)

if flags['nog0']:
    outfile = os.path.join(out_path, 'scan_area_nog0.png')
    mylib.plot_area(scan_data1['nog0'], args.nog0_range[0], args.nog0_range[1], step_x_num, step_y_num, 'nog0',
                    y_sorted, outfile, startX, startY, 0, mode)

if flags['nog15']:
    outfile = os.path.join(out_path, 'scan_area_nog15.png')
    mylib.plot_area(scan_data1['nog15'], args.nog15_range[0], args.nog15_range[1], step_x_num, step_y_num, 'nog15',
                    y_sorted, outfile, startX, startY, 0, mode)

if flags['toptobottom']:
    outfile = os.path.join(out_path, 'scan_area_topbottom.png')
    mylib.plot_area(scan_data1['top2bottom'], -0.5, npic + 0.5, step_x_num, step_y_num, 'Number of Layer in Emulsion', y_sorted,
                    outfile, startX, startY, 0, mode)

    outfile = os.path.join(out_path, 'sensor_topbottom.png')
    mylib.plot_sensor(scan_data1['top2bottom'], 0.1, npic, 'Number of Layer in Emulsion', y_sorted, outfile)


if flags['not']:
    outfile = os.path.join(out_path, 'scan_area_not.png')
    mylib.plot_area(scan_data1['not'], 0.1, args.not_absolute_max, step_x_num, step_y_num, 'Number of Tracks (not)',
                    y_sorted, outfile, startX, startY, 0, mode)

    outfile = os.path.join(out_path, 'sensor_not.png')
    mylib.plot_sensor_not(scan_data1['not'], 'Number Of Tracks (not)', y_sorted, outfile,
                          relative_min=args.not_relative_min, absolute_max=args.not_absolute_max)

if flags['not_un']:
    outfile = os.path.join(out_path, 'scan_area_not_unclust.png')
    mylib.plot_area(scan_data1['not_uncrust'], 1, args.unclust_not_max, step_x_num, step_y_num, 'Unclusterd Number of Tracks', y_sorted,
                    outfile, startX, startY, 0, mode)

    outfile = os.path.join(out_path, 'sensor_not_unclust.png')
    mylib.plot_sensor(scan_data1['not_uncrust'], 1, args.unclust_not_max, 'Unclusterd Number of Tracks', y_sorted, outfile)

if flags['mainprocess']:
    outfile = os.path.join(out_path, 'scan_area_process.png')
    mylib.plot_area(scan_data1['main_process'], 1, args.main_process_max, step_x_num, step_y_num, 'time of Main Process [ms]', y_sorted, outfile, startX, startY, 0, mode)
    outfile = os.path.join(out_path, 'sensor_process.png')
    mylib.plot_sensor(scan_data1['main_process'], 1, args.main_process_max, 'time of Main Process [ms]', y_sorted, outfile)

if flags['startpicnum']:
    outfile = os.path.join(out_path, 'scan_area_StartPicNum.png')
    mylib.plot_area(scan_data1['start_picnum'], -0.5, npic - 15.5, step_x_num, step_y_num, 'StartPicNum',
                    y_sorted, outfile, startX, startY, 0, mode)

    outfile = os.path.join(out_path, 'sensor_StartPicNum.png')
    mylib.plot_sensor(scan_data1['start_picnum'], 0.1, npic - 15.5, 'StartPicNum', y_sorted, outfile)

if flags['thickoflayer']:
    outfile = os.path.join(out_path, 'scan_area_ThickOfLayer.png')
    mylib.plot_area(scan_data2['ThickOfLayer'], thick_min, thick_max, step_x_num, step_y_num, 'Thick Of Layer [um]',
                         y_sorted, outfile, startX, startY, 1, mode)

if flags['base']:
    outfile = os.path.join(out_path, 'Base_Surface.png')
    mylib.plot_base(scan_data1['fine_z'], args.base_surface_range[0], args.base_surface_range[1],
                    args.base_surface_range[2], args.base_surface_range[3], args.base_thickness_range[0],
                    args.base_thickness_range[1], step_x_num, step_y_num, 'Base Surface [mm]', y_sorted, outfile, mode)

if flags['bright']:
    mylib.plot_TargetBright(evmg_json, y_sorted, out_path)

if flags['freq']:
    df3 = mylib.calc_df(scan_data3)
    mylib.plot_frequency(df3, out_path, time_list)

if flags['nog_all']:
    mylib.plot_nogall(scan_data1['nog_all'], args.imager_id, args.nog_all_max, nog_thr_list, out_path, alpha=0.15)

if flags['text']:
    mylib.text_dump(scan_data1, scan_data2, time_total, out_path)
    if flags['is32layerScan']:
        mylib.text_dump32(scan_data1, scan_data2, time_total, out_path, flags)
    
# GRAPHフォルダを開く
os.startfile(out_path)

if flags['is32layerScan']:
    #32Layerフォルダの作成
    if not os.path.exists(os.path.join(out_path, '32LayerScan')):
        os.makedirs(os.path.join(out_path, '32LayerScan'), exist_ok=True)
    if flags['not']:
        if flags["thick0"]:
            outfile = os.path.join(out_path, "32LayerScan","scan_area_not_thick0.png")
            mylib.plot_area(scan_data1['not_thick0'], 0.1, args.not_absolute_max_32layer_thick, step_x_num, step_y_num, 'Number of Tracks (not) of Thick0',
                            y_sorted, outfile, startX, startY, 0, mode)
            outfile = os.path.join(out_path, "32LayerScan","sensor_not_thick0.png")
            mylib.plot_sensor_not(scan_data1['not_thick0'], 'Number Of Tracks (not) of Thick0', y_sorted, outfile,
                                relative_min=args.not_relative_min, absolute_max=args.not_absolute_max_32layer_thick)
        if flags["thick1"]:
            outfile = os.path.join(out_path, "32LayerScan","scan_area_not_thick1.png")
            mylib.plot_area(scan_data1['not_thick1'], 0.1, args.not_absolute_max_32layer_thick, step_x_num, step_y_num, 'Number of Tracks (not) of Thick1',
                            y_sorted, outfile, startX, startY, 0, mode)
            outfile = os.path.join(out_path, "32LayerScan","sensor_not_thick1.png")
            mylib.plot_sensor_not(scan_data1['not_thick1'], 'Number Of Tracks (not) of Thick1', y_sorted, outfile,
                                relative_min=args.not_relative_min, absolute_max=args.not_absolute_max_32layer_thick)
        if flags["thinOuter"]:
            outfile = os.path.join(out_path, "32LayerScan","scan_area_not_thin_outer.png")
            mylib.plot_area(scan_data1['not_thin0'], 0.1, args.not_absolute_max_32layer_thin, step_x_num, step_y_num, 'Number of Tracks (not) of Thin Outer',
                            y_sorted, outfile, startX, startY, 0, mode)
            outfile = os.path.join(out_path, "32LayerScan","sensor_not_thin_outer.png")
            mylib.plot_sensor_not(scan_data1['not_thin0'], 'Number Of Tracks (not) of Thin Outer', y_sorted, outfile,
                                relative_min=args.not_relative_min, absolute_max=args.not_absolute_max_32layer_thin)
        if flags["thinBase"]:
            outfile = os.path.join(out_path, "32LayerScan","scan_area_not_thin_inner.png")
            mylib.plot_area(scan_data1['not_thin1'], 0.1, args.not_absolute_max_32layer_thin, step_x_num, step_y_num, 'Number of Tracks (not) of Thin Inner',
                            y_sorted, outfile, startX, startY, 0, mode)
            outfile = os.path.join(out_path, "32LayerScan","sensor_not_thin_inner.png")
            mylib.plot_sensor_not(scan_data1['not_thin1'], 'Number Of Tracks (not) of Thin Inner', y_sorted, outfile,
                                relative_min=args.not_relative_min, absolute_max=args.not_absolute_max_32layer_thin)
    if flags['not_un']:
        if flags["thick0"]:
            outfile = os.path.join(out_path, "32LayerScan","scan_area_not_unclust_thick0.png")
            mylib.plot_area(scan_data1['not_uncrust_thick0'], 1, args.unclust_not_max_32layer_thick, step_x_num, step_y_num, 'Unclusterd Number of Tracks of Thick0', y_sorted,
                            outfile, startX, startY, 0, mode)
            outfile = os.path.join(out_path, "32LayerScan","sensor_not_unclust_thick0.png")
            mylib.plot_sensor(scan_data1['not_uncrust_thick0'], 1, args.unclust_not_max_32layer_thick, 'Unclusterd Number of Tracks of Thick0', y_sorted, outfile)
        if flags["thick1"]:
            outfile = os.path.join(out_path, "32LayerScan","scan_area_not_unclust_thick1.png")
            mylib.plot_area(scan_data1['not_uncrust_thick1'], 1, args.unclust_not_max_32layer_thick, step_x_num, step_y_num, 'Unclusterd Number of Tracks of Thick1', y_sorted,
                            outfile, startX, startY, 0, mode)
            outfile = os.path.join(out_path, "32LayerScan","sensor_not_unclust_thick1.png")
            mylib.plot_sensor(scan_data1['not_uncrust_thick1'], 1, args.unclust_not_max_32layer_thick, 'Unclusterd Number of Tracks of Thick1', y_sorted, outfile)
        if flags["thinOuter"]:
            outfile = os.path.join(out_path, "32LayerScan","scan_area_not_unclust_thin_outer.png")
            mylib.plot_area(scan_data1['not_uncrust_thin0'], 1, args.unclust_not_max_32layer_thin, step_x_num, step_y_num, 'Unclusterd Number of Tracks of Thin Outer', y_sorted,
                            outfile, startX, startY, 0, mode)
            outfile = os.path.join(out_path, "32LayerScan","sensor_not_unclust_thin_outer.png")
            mylib.plot_sensor(scan_data1['not_uncrust_thin0'], 1, args.unclust_not_max_32layer_thin, 'Unclusterd Number of Tracks of Thin Outer', y_sorted, outfile)
        if flags["thinBase"]:
            outfile = os.path.join(out_path, "32LayerScan","scan_area_not_unclust_thin_inner.png")
            mylib.plot_area(scan_data1['not_uncrust_thin1'], 1, args.unclust_not_max_32layer_thin, step_x_num, step_y_num, 'Unclusterd Number of Tracks of Thin Inner', y_sorted,
                            outfile, startX, startY, 0, mode)
            outfile = os.path.join(out_path, "32LayerScan","sensor_not_unclust_thin_inner.png")
            mylib.plot_sensor(scan_data1['not_uncrust_thin1'], 1, args.unclust_not_max_32layer_thin, 'Unclusterd Number of Tracks of Thin Inner', y_sorted, outfile)

        


