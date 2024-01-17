import math
import os
import subprocess

import edit_fitdata as edit


basepath = 'A:\\Test\\TrackMatch\\trackmatching4aff-m222-pl001'
nx = 45
ny = 25
origin_view = 0
x_lean_num = 100
angcut = 12.0
phcut = 10
volcut = 20

imager_num = 24
for i in range(24):
    sensor = i % 12
    module = math.floor(i / 12)
    out_path = os.path.join(basepath, 'TrackMatching4Aff', '{:02}_{:02}'.format(module, sensor))
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    os.chdir(out_path)

    command_TM = 'C:\\Users\\flab\\source\\repos\\myproject\\x64\\Release\\TrackMatching4Aff.exe {} {} {} {} {} {} {}'.format(basepath, nx, ny, i, angcut, phcut, volcut)
    subprocess.run(command_TM)

    command_fit = 'root -l -q -b C:\\Users\\flab\\cpp_project\\root\\fit_TrackMatching4aff.C({},{},{})'.format(nx, ny, x_lean_num)
    subprocess.run(command_fit)

    befor_fit_csv = os.path.join(out_path, 'fit_data.csv')
    vvh_path = os.path.join(basepath, 'ValidViewHistory.json')
    edit.edit_fitdata(befor_fit_csv, vvh_path, origin_view, x_lean_num)

    command_cal_aff = 'root -l -q -b C:\\Users\\flab\\cpp_project\\root\\fit_surf_TrackMatching4Aff.C'
    subprocess.run(command_cal_aff)
