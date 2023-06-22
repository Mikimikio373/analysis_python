import subprocess
import os
import sys
import pandas as pn
import json
import yaml
import shutil

basepath = 'R:\\minami\\20230531_aff\\Module1\\sensor-7'
outpath_name = 'check_StartPoint'
GMexe_path = 'C:\\Users\\flab\\source\\repos\\myproject\\x64\\Release\\GrainMatching.exe'
root_macro_path = 'C:\\Users\\flab\\cpp_project\\root\\cut_fit_GM.C'
outpath = os.path.join(basepath, outpath_name)
editdata_path = os.path.join(basepath, 'check_StartPoint', 'encode.csv')

yaml_path = os.path.join(basepath, 'AreaScan4Param.yml')
with open(yaml_path, 'rb') as yml:
    param = yaml.safe_load(yml)

x_size = param['Area'][0]['NViewX']  # x方向の大きさ
y_size = param["Area"][0]["NViewY"]  # y方向の大きさ
layer = param["Area"][0]["NLayer"]
npicture = param["NPictures"]
plate_sum = layer * x_size * y_size

start = 0
end = y_size

mode = '001'

#grain match
if mode[0] == '1':
    for i in range(start + 1, end + 1):
        ref_path = os.path.join(basepath, 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_4_{}.png'.format(start))
        comp_path = os.path.join(basepath, 'IMAGE00_AREA-1', 'png', 'L0_VX0000_VY0000_4_{}.png'.format(i))
        ref_name = 'L0_VX0000_VY0000_{}'.format(start)
        comp_name = 'L0_VX0000_VY0000_{}'.format(i)
        dist_name = 'L0_VX0000_VY0000_{:03}vs{:03}'.format(start, i)
        minus = 50

        command = '{} {} {} {} {} -COBname {} {} -minus {} -skip'.format(GMexe_path, ref_path, comp_path, outpath, dist_name, ref_name, comp_name, minus)
        subprocess.run(command)

#fit
if mode[1] == '1':
    work_dir = outpath
    for i in range(start + 1, end + 1):
        input_csv = 'L0_VX0000_VY0000_{:03}vs{:03}.csv'.format(start, i)
        pdf_name = 'L0_VX0000_VY0000_{:03}vs{:03}_fit.pdf'.format(start, i)
        root_name = 'L0_VX0000_VY0000_{:03}vs{:03}.root'.format(start, i)
        out_csv = 'L0_VX0000_VY0000_{:03}vs{:03}_fit.csv'.format(start, i)

        command = 'root -l -q -b {}(\\\"{}\\\",\\\"{}\\\",\\\"{}\\\",\\\"{}\\\",\\\"{}\\\")'.format(root_macro_path, work_dir.replace('\\', '/'), input_csv, pdf_name, root_name, out_csv)
        subprocess.run(command)


#data edit
if mode[2] == '1':
    stat_dir = os.path.join(outpath, 'stats_CenterOfBrightness')
    GM_dir = os.path.join(outpath, 'GM_data')
    root_dir = os.path.join(outpath, 'root_data')
    plot_dir = os.path.join(outpath, 'plot_data')

    if not os.path.exists(stat_dir):
        os.makedirs(stat_dir)
    if not os.path.exists(GM_dir):
        os.makedirs(GM_dir)
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    view = 0
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

    for i in range(y_size + 1):
        #jsonファイルの読み込み
        if i < 2:
            view += x_size * i
        else:
            view += x_size + 1
        oripath = os.path.join(basepath, 'IMAGE00_AREA-1',
                               'V{:08}_L{}_VX{:04}_VY{:04}_0_{:03}.json'.format(view, 0, 0, 0, npicture))
        json_open = open(oripath)
        j = json.load(json_open)
        if i == 0:
            sx_0 = j['Images'][0]['x']
            sy_0 = j['Images'][0]['y']
            dx = 0
            dy = 0
        else:
            dx = j['Images'][0]['x'] - sx_0
            dy = j['Images'][0]['y'] - sy_0
        line.append(i)
        sx.append(j['Images'][0]['x'])
        sy.append(j['Images'][0]['y'])
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
        fit_data_name = 'L0_VX0000_VY0000_{:03}vs{:03}_fit.csv'.format(start, i)
        fit_csv = os.path.join(outpath, fit_data_name)
        fit_data = pn.read_csv(fit_csv)
        entries.append(fit_data['entries'][0])
        dpx.append(fit_data['dpx'][0])
        dpy.append(fit_data['dpy'][0])
        dpx_err.append(fit_data['dpx_err'][0])
        dpy_err.append(fit_data['dpy_err'][0])

        #ファイルの移動
        stat_path = os.path.join(outpath, 'L0_VX0000_VY0000_{}_stats.csv'.format(i))
        if os.path.exists(stat_path):
            shutil.move(stat_path, stat_dir)
        GM_path = os.path.join(outpath, 'L0_VX0000_VY0000_{:03}vs{:03}.csv'.format(start, i))
        if os.path.exists(GM_path):
            shutil.move(GM_path, GM_dir)
        root_path = os.path.join(outpath, 'L0_VX0000_VY0000_{:03}vs{:03}.root'.format(start, i))
        if os.path.exists(root_path):
            shutil.move(root_path, root_dir)
        plot_path = os.path.join(outpath, 'L0_VX0000_VY0000_{:03}vs{:03}_fit.pdf'.format(start, i))
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

