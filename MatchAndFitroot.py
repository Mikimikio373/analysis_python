import os
import sys
import yaml
import time

# pythonpath = 'R:\\minami\\20221002_forGrainMaching0.025\\analysis_python'
basepath = 'R:\\minami\\20221103_zabuton'
exepath = 'C:\\Users\\flab\\source\\repos\\myproject\\x64\\Release\\GrainMatching_v2.exe'
shift_X = 40
shift_Y = 20
type_max = 1 + 1
module_max = 2 + 1
ver_max = 5 + 1
minus = 45
# if(mode == 0):
#     rootpath = 'R:\\minami\\20221002_forGrainMaching0.025\\root\\cut_fit_csv.C'
# else:
#     rootpath = 'R:\\minami\\20221002_forGrainMaching0.025\\root\\cut_fit_root.C'
rootpath = 'C:\\Users\\flab\\cpp_project\\root\\cut_fit_FastReadCSV.C'

# for n_t in range(1, type_max):
#     for n_m in range(1, module_max):
#         for n_v in range(1, ver_max):
#             type = 'type{}'.format(n_t)
#             module = 'Module{}'.format(n_m)
#             version = 'ver-{}'.format(n_v)
#             area = 'E'
#             areapath = os.path.join(basepath, type, module, version, area)
#             if not os.path.exists(areapath):
#                 print('there is not path')
#                 continue
#             yaml_path = os.path.join(areapath, 'AreaScan4Param.yml')
#             with open(yaml_path, 'rb') as yml:
#                 param = yaml.safe_load(yml)
#             npicture = param["NPictures"] - 1
#             print(npicture)
#
#
#             command_match = "start {} {} {} {} {} {}".format(exepath, areapath, npicture, shift_X, shift_Y, minus)
#             os.system(command_match)
#
# print('sleep time')
# for i in range(1, 6001):
#     time.sleep(1)
#     sys.stdout.write("\r{}/6000".format(i))
#     sys.stdout.flush()

for n_t in range(1, type_max):
    for n_m in range(1, module_max):
        for n_v in range(1, ver_max):
            os.chdir(basepath)
            type = 'type{}'.format(n_t)
            module = 'Module{}'.format(n_m)
            version = 'ver-{}'.format(n_v)
            area = 'E'
            areapath = os.path.join(basepath, type, module, version, area)
            if not os.path.exists(areapath):
                continue
            os.chdir(areapath)
            currend_dir = os.getcwd()
            print('current directry: ', currend_dir)
            command_root = "start root -l -q -b {}+({},{})".format(rootpath, shift_X, shift_Y)
            os.system(command_root)
