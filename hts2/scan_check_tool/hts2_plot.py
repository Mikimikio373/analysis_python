import os
import sys
import json
import shutil

import yaml
import math

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
with open(os.path.join(pythonpath, 'sensor_pos.yml'), 'rb') as f:
    y_load = yaml.safe_load(f)
y_sorted = sorted(y_load, key=lambda x: x['pos'])

# スキャンパラメータの取得
ScanControllParam = os.path.join(basepath, 'ScanControllParam.json')
if not os.path.exists(ScanControllParam):
    sys.exit('There is no file: {}'.format(ScanControllParam))
with open(ScanControllParam, 'rb') as scp:
    scp_json = json.load(scp)
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
if scp_json['ScanAreaParam']['Algorithm'] == 'One_Third_Half_HTS2':
    mode = 1
    print('scan algorithm: One_Third_Half_HTS2')
else:
    print('現在One_Third_Half_HTS2以外対応していません')
    sys.exit()

# ターゲット輝度値分布を書くためにpathとjsonデータを取得
if 'ImagerControllerParamFilePath' in scp_json['OtherPathParam']:
    evmg_path = scp_json['OtherPathParam']['ImagerControllerParamFilePath']
    with open(evmg_path, 'rb') as f:
        evmg_json = json.load(f)
else:
    evwg_json = None
    flags['bright'] = False

# VaridViewHistryの取得(プロットデータはほぼすべてここから取得している)
with open(os.path.join(basepath, 'ValidViewHistory.json'), 'rb') as f:
    vvh_json = json.load(f)

# GRAPHファイルの作成
out_path = os.path.join(basepath, 'GRAPH')
not_path = os.path.join(out_path, 'NOT')
os.makedirs(not_path, exist_ok=True)
if mode == 0:
    module = 6
    sensor = 12
elif mode == 1:
    module = 2
    sensor = 12
else:
    module = None
    sensor = None
for m in range(module):
    for s in range(sensor):
        target_txt = os.path.join(basepath, 'DATA', '{:02}_{:02}'.format(m, s), 'TrackHit2_0_99999999_0_000.txt')
        target_json = os.path.join(basepath, 'DATA', '{:02}_{:02}'.format(m, s), 'TrackHit2_0_99999999_0_000.json')
        if not os.path.exists(target_txt):
            print('There is no file: {}'.format(target_txt))
            continue
        if not os.path.exists(target_json):
            print('There is no file: {}'.format(target_json))
            continue

        shutil.copy2(target_txt, os.path.join(not_path, '{:02}_{:02}_TrackHit2_0_99999999_0_000.txt'.format(m, s)))
        shutil.copy2(target_json, os.path.join(not_path, '{:02}_{:02}_TrackHit2_0_99999999_0_000.json'.format(m, s)))

# initialプロットするためのデータ取得
scan_data1, scan_data2, scan_data3 = mylib.initial(vvh_json, not_path, layer, mode)

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
                    'Exposure Count', y_sorted, outfile, startX, startY)

    outfile = os.path.join(out_path, 'sensor_excount.png')
    mylib.plot_sensor(scan_data1['excount'], args.exposure_range[0], args.exposure_range[1], 'Exposure Count',
                      y_sorted, outfile)

if flags['nog']:
    outfile = os.path.join(out_path, 'scan_area_nog.png')
    mylib.plot_area(scan_data1['nog_over_thr'], args.nog_range[0], args.nog_range[1], step_x_num, step_y_num, 'nog',
                    y_sorted, outfile, startX, startY)

    outfile = os.path.join(out_path, 'sensor_nog.png')
    mylib.plot_sensor(scan_data1['nog_over_thr'], args.nog_range[0], args.nog_range[1], 'nog', y_sorted, outfile)

if flags['nog0']:
    outfile = os.path.join(out_path, 'scan_area_nog0.png')
    mylib.plot_area(scan_data1['nog0'], args.nog0_range[0], args.nog0_range[1], step_x_num, step_y_num, 'nog0',
                    y_sorted, outfile, startX, startY)

    outfile = os.path.join(out_path, 'scan_area_nog15.png')
    mylib.plot_area(scan_data1['nog15'], args.nog15_range[0], args.nog15_range[1], step_x_num, step_y_num, 'nog15',
                    y_sorted, outfile, startX, startY)

if flags['toptobottom']:
    outfile = os.path.join(out_path, 'scan_area_topbottom.png')
    mylib.plot_area(scan_data1['top2bottom'], -0.5, npic + 0.5, step_x_num, step_y_num, 'bottom - top', y_sorted,
                    outfile, startX, startY)

    outfile = os.path.join(out_path, 'sensor_topbottom.png')
    mylib.plot_sensor(scan_data1['top2bottom'], 0.1, npic, 'bottom - top', y_sorted, outfile)


if flags['not']:
    outfile = os.path.join(out_path, 'scan_area_not.png')
    mylib.plot_area(scan_data1['not'], 0.1, args.not_absolute_max, step_x_num, step_y_num, 'Number Of Tracks',
                    y_sorted, outfile, startX, startY)

    outfile = os.path.join(out_path, 'sensor_not.png')
    mylib.plot_sensor_not(scan_data1['not'], 'Number Of Tracks', y_sorted, outfile,
                          relative_min=args.not_relative_min, absolute_max=args.not_absolute_max)

if flags['not_un']:
    outfile = os.path.join(out_path, 'scan_area_not_unclust.png')
    mylib.plot_area(scan_data1['not_uncrust'], 1, args.unclusst_not_max, step_x_num, step_y_num, 'Unclusterd Number of Tracks', y_sorted,
                    outfile, startX, startY)

    outfile = os.path.join(out_path, 'sensor_not_unclust.png')
    mylib.plot_sensor(scan_data1['not_uncrust'], 1, args.unclusst_not_max, 'Unclusterd Number of Tracks', y_sorted, outfile)

if flags['mainprocess']:
    outfile = os.path.join(out_path, 'sensor_process.png')
    mylib.plot_sensor(scan_data1['main_process'], 1, args.main_process_max, 'time of Main Process [ms]', y_sorted, outfile)

if flags['startpicnum']:
    outfile = os.path.join(out_path, 'scan_area_StartPicNum.png')
    mylib.plot_area(scan_data1['start_picnum'], -0.5, npic - 15.5, step_x_num, step_y_num, 'StartPicNum',
                    y_sorted, outfile, startX, startY)

    outfile = os.path.join(out_path, 'sensor_StartPicNum.png')
    mylib.plot_sensor(scan_data1['start_picnum'], 0.1, npic - 15.5, 'StartPicNum', y_sorted, outfile)

if flags['thickoflayer']:
    outfile = os.path.join(out_path, 'scan_area_ThickOfLayer.png')
    mylib.plot_area_view(scan_data2['ThickOfLayer'], thick_min, thick_max, step_x_num, step_y_num, 'Thick Of Layer [um]',
                         y_sorted, outfile)

if flags['base']:
    outfile = os.path.join(out_path, 'Base_Surface.png')
    mylib.plot_base(scan_data1['fine_z'], args.base_surface_range[0], args.base_surface_range[1],
                    args.base_surface_range[2], args.base_surface_range[3], args.base_thickness_range[0],
                    args.base_thickness_range[1], step_x_num, step_y_num, 'Base Surface [mm]', y_sorted, outfile)

if flags['bright']:
    mylib.plot_TargetBright(evmg_json, y_sorted, out_path)

if flags['freq']:
    df3 = mylib.calc_df(scan_data3)
    mylib.plot_frequency(df3, out_path)

if flags['nog_all']:
    mylib.plot_nogall(scan_data1['nog_all'], args.imager_id, args.nog_all_max, nog_thr_list, out_path, alpha=0.15)

if flags['text']:
    mylib.text_dump(scan_data1, scan_data2, out_path)

# GRAPHフォルダを開く
os.startfile(out_path)
