import os
import subprocess
import sys
import yaml
import shutil
import pandas as pn
import json

basepath = 'R:\\minami\\20230531_aff\\Module1\\sensor-7'
GMexe_path = 'C:\\Users\\flab\\source\\repos\\myproject\\x64\\Release\\GrainMatching.exe'
root_macro_path = 'C:\\Users\\flab\\cpp_project\\root\\cut_fit_GM.C'
out_path_name = 'check_ystep'
out_path = os.path.join(basepath, out_path_name)
editdata_path = os.path.join(basepath, out_path_name, 'fitdata.csv')
yaml_path = os.path.join(basepath, 'AreaScan4Param.yml')
with open(yaml_path, 'rb') as yml:
    param = yaml.safe_load(yml)

x_size = param['Area'][0]['NViewX']  # x方向の大きさ
y_size = param["Area"][0]["NViewY"]  # y方向の大きさ
layer = param["Area"][0]["NLayer"]
npicture = param["NPictures"]
plate_sum = layer * x_size * y_size

mode = '001'

#GM
if mode[0] == '1':
    target_max = 6000
    target_min = 5000
    for i in range(1, y_size):
        ref_path = os.path.join(basepath, 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_{}_{}.png'.format(npicture - 1, i))
        ref_name = 'L0_VX0000_VY0000_{}'.format(i)
        comp_path = os.path.join(basepath, 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY{:04}_{}.png'.format(i, npicture-1, i))
        comp_name = 'L0_VX0000_VY{:04}'.format(i)
        dist_name = 'L0_VX0000_VY0000_{}vsVY{:04}'.format(i, i)

        command = '{} {} {} {} {} -COBname {} {} -autominus {} {} -skip'.format(GMexe_path, ref_path, comp_path, out_path,
                                                                         dist_name, ref_name, comp_name, target_max, target_min)
        subprocess.run(command)

#fit
if mode[1] == '1':
    for i in range(1, y_size):
        input_csv = 'L0_VX0000_VY0000_{}vsVY{:04}.csv'.format(i, i)
        pdf_name = 'L0_VX0000_VY0000_{}vsVY{:04}_fit.pdf'.format(i, i)
        root_name = 'L0_VX0000_VY0000_{}vsVY{:04}.root'.format(i, i)
        out_csv = 'L0_VX0000_VY0000_{}vsVY{:04}_fit.csv'.format(i, i)

        command = 'root -l -q -b {}(\\\"{}\\\",\\\"{}\\\",\\\"{}\\\",\\\"{}\\\",\\\"{}\\\")'.format(root_macro_path,
                                                                                                    out_path.replace(
                                                                                                        '\\', '/'),
                                                                                                    input_csv, pdf_name,
                                                                                                    root_name, out_csv)
        subprocess.run(command)

#data edit
if mode[2] == '1':
    stat_dir = os.path.join(out_path, 'stats_CenterOfBrightness')
    GM_dir = os.path.join(out_path, 'GM_data')
    root_dir = os.path.join(out_path, 'root_data')
    plot_dir = os.path.join(out_path, 'plot_data')

    if not os.path.exists(stat_dir):
        os.makedirs(stat_dir)
    if not os.path.exists(GM_dir):
        os.makedirs(GM_dir)
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    sx_0 = 0
    sy_0 = 0
    sx = []
    sy = []
    dsx = []
    dsy = []
    line = []
    entries = []
    dpx = []
    dpy = []
    dpx_err = []
    dpy_err = []

    for i in range(y_size):
        #jsonファイルの読み込み
        if i == 0:
            view = 0
            ref_json = os.path.join(basepath, 'IMAGE00_AREA-1',
                                    'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view, 0, 0, 0, npicture))
            comp_json = ref_json
        else:
            view = (x_size + 1) * i - 1
            ref_json = os.path.join(basepath, 'IMAGE00_AREA-1',
                                   'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view, 0, 0, 0, npicture))
            comp_json = os.path.join(basepath, 'IMAGE00_AREA-1',
                                   'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view + 1, 0, 0, i, npicture))
        ref_json_open = open(ref_json)
        j_ref = json.load(ref_json_open)
        comp_json_open = open(comp_json)
        j_comp = json.load(comp_json_open)
        if i == 0:
            sx_0 = j_ref['Images'][0]['x']
            sy_0 = j_ref['Images'][0]['y']
            dx = 0
            dy = 0
        else:
            dx = j_comp['Images'][0]['x'] - j_ref['Images'][0]['x']
            dy = j_comp['Images'][0]['y'] - j_ref['Images'][0]['y']
        line.append(i)
        sx.append(j_comp['Images'][0]['x'])
        sy.append(j_comp['Images'][0]['y'])
        dsx.append(dx)
        dsy.append(dy)

        #fitdata読み込み
        if i == 0:
            entries.append(0)
            dpx.append(0)
            dpy.append(0)
            dpx_err.append(0)
            dpy_err.append(0)
            continue
        fit_data_name = 'L0_VX0000_VY0000_{}vsVY{:04}_fit.csv'.format(i, i)
        fit_csv = os.path.join(out_path, fit_data_name)
        fit_data = pn.read_csv(fit_csv)
        entries.append(fit_data['entries'][0])
        dpx.append(fit_data['dpx'][0])
        dpy.append(fit_data['dpy'][0])
        dpx_err.append(fit_data['dpx_err'][0])
        dpy_err.append(fit_data['dpy_err'][0])

        #ファイルの移動
        # stat_path = os.path.join(out_path, 'L0_VX0000_VY0000_{}vsVY{:04}.csv'.format(i, i))
        # if os.path.exists(stat_path):
        #     shutil.move(stat_path, stat_dir)
        GM_path = os.path.join(out_path, 'L0_VX0000_VY0000_{}vsVY{:04}.csv'.format(i, i))
        if os.path.exists(GM_path):
            shutil.move(GM_path, GM_dir)
        root_path = os.path.join(out_path, 'L0_VX0000_VY0000_{}vsVY{:04}.root'.format(i, i))
        if os.path.exists(root_path):
            shutil.move(root_path, root_dir)
        plot_path = os.path.join(out_path, 'L0_VX0000_VY0000_{}vsVY{:04}_fit.pdf'.format(i, i))
        if os.path.exists(plot_path):
            shutil.move(plot_path, plot_dir)
        # os.remove(fit_csv)

    out = pn.DataFrame()
    out['time'] = line
    out['sx'] = sx
    out['sy'] = sy
    out['dsx'] = dsx
    out['dsy'] = dsy
    out['entries'] = entries
    out['dpx'] = dpx
    out['dpy'] = dpy
    out['dpx_err'] = dpx_err
    out['dpy_err'] = dpy_err
    out.to_csv(editdata_path, index=False)