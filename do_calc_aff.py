import subprocess
import sys

import yaml

yaml_path = 'AreaScan4Param.yml'
with open(yaml_path, 'rb') as yml:
    param = yaml.safe_load(yml)
vx = param['Area'][0]['NViewX']
vy = param['Area'][0]['NViewY']
npicture = param["NPictures"]
yml.close()

print(vx, vy, npicture)
command_fitting = 'c:\\Users\\flab\\cpp_project\\root\\cut_fit_cutRead.C+({},{})'.format(vx, vy)
subprocess.call(command_fitting)
command_