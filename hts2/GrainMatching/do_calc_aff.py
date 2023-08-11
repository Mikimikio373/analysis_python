import os
import subprocess
import sys

import yaml

args = sys.argv
if not len(args) == 3:
    sys.exit('command line error, please input \"minus, option\"')

current_path = os.getcwd()
minus = args[1]
option = args[2]
if not len(option) == 3:
    sys.exit('option error, option must have 3 number like \"111\"')

yaml_path = 'AreaScan4Param.yml'
with open(yaml_path, 'rb') as yml:
    param = yaml.safe_load(yml)
vx = param['Area'][0]['NViewX']
vy = param['Area'][0]['NViewY']
npicture = param["NPictures"]
yml.close()

command_GrainMatching = 'c:\\Users\\flab\\source\\repos\\myproject\\x64\\Release\\GrainMatching_v2.exe {} {} {} {} {}'.format(current_path, npicture - 1, vx, vy, minus)
if option[0] == '1':
    subprocess.run(command_GrainMatching)
elif option[0] == '0':
    print('Graine Maching skipped')
else:
    sys.exit('option error, first number must be 0 or 1')

command_fitting = 'root -l -q -b c:\\Users\\flab\\cpp_project\\root\\cut_fit_FastReadCSV.C+({},{})'.format(vx, vy)
if option[1] == '1':
    subprocess.run(command_fitting)
elif option[1] == '0':
    print('fitting skipped')
else:
    sys.exit('option error, second number must be 0 or 1')

command_edit_calc_aff = 'python c:\\Users\\flab\\analysis_python\\hts2\\edit_calc_affdata.py {} {} {} {}'.format(current_path, vx, vy, npicture)
if option[2] == '1':
    subprocess.run(command_edit_calc_aff)
elif option[2] == '0':
    print('edit calc aff skipped')
else:
    sys.exit('option error, third number must be 0 or 1')
