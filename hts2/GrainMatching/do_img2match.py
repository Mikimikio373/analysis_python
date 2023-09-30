import os
import subprocess
import sys
import math

tar_dir = 'Q:/minami/20230914_Ali2'
os.chdir(tar_dir)
current_dir = os.getcwd()
print('path changed. currend path: {}'.format(current_dir))

img_base = 'Q:/minami/20230914_Ali2/0020/IMAGE'
if not len(sys.argv) == 4:
    sys.exit('please input module sensor picnum')
module = int(sys.argv[1])
sensor = int(sys.argv[2])
picnum = int(sys.argv[3])
img_path = os.path.join(img_base, '{:02}_{:02}'.format(module, sensor), 'ImageFilterWithStream_GPU_0_00000000_0_{:03}.png'.format(picnum)).replace('\\', '/')

if not os.path.exists(img_path):
    sys.exit('there are no file: {}'.format(img_path))

aff_path = os.path.join('Q:/minami/20230912_aff', 'Module{}'.format(module), 'sensor-{}'.format(sensor), 'affdata_surf.csv')

pixel2image_path = 'C:/Users/flab/source/repos/myproject/x64/Release/pixel2stage.exe'
out_path = 'calc_ali'
out_name = '{}-{:02}'.format(module, sensor)
command_pixel2stage = '{} {} 0 {} {} {} -nojson 0 0 -autominus 10000 6000'.format(pixel2image_path, img_path, aff_path, out_path, out_name)
subprocess.run(command_pixel2stage)

match_exepath = 'C:/Users/flab/source/repos/myproject/x64/Release/GrainMatching_in_Stage.exe'
# ref_path = 'calc_ali/all_stage_list.csv'
ref_path = 'calc_ali/0-3_all_list_fix.csv'
comp_path = 'calc_ali/{}_stage.csv'.format(out_name)
matched_name = 'vs{}-{:02}'.format(module, sensor)
x_width = 1.17
y_width = 0.56
i = module * 12 + sensor
if math.floor(i /12) == 0:
    if i % 4 == 0:
        x = x_width * 6
    elif i % 4 == 1:
        x = x_width * 4
    elif i % 4 == 2:
        x = x_width * 2
    else:
        x = 0
    if math.floor(i / 4) == 0:
        y = 0
    elif math.floor(i / 4) == 1:
        y = y_width * 3
    else:
        y = y_width * 6
else:
    if i % 4 == 0:
        x = x_width * 7
    elif i % 4 == 1:
        x = x_width * 5
    elif i % 4 == 2:
        x = x_width * 3
    else:
        x = x_width * 1

    if math.floor((i - 12) / 4) == 0:
        y = y_width * 6
    elif math.floor((i - 12) / 4) == 1:
        y = y_width * 3
    else:
        y = 0
command_stagematch = '{} {} {} {} {} -cutmode {:.3f} {:.3f} 0.1'.format(match_exepath, ref_path, comp_path, out_path, matched_name, x, y)
subprocess.run(command_stagematch)

TTree = 'C:/Users/flab/cpp_project/root/read_ali_csv.C'
dist_path = 'calc_ali/{}'.format(matched_name)
command_read2TTree = 'root -l -q -b {}(\\\"{}\\\")'.format(TTree, dist_path)
subprocess.run(command_read2TTree)