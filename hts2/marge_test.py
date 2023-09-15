import os.path
import subprocess

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import matplotlib.cm as cm

basepath = 'Q:/minami/affine_param/marge_test'

pixel2stage_exe = 'c:/Users/flab/source/repos/myproject/x64/Release/pixel2stage.exe'
img_base = 'Q:/minami/20230914_Ali2/0020/IMAGE'

VVH = 'Q:/minami/20230914_Ali2/0020/ValidViewHistory.json'
with open(VVH) as f:
    VVH_data = json.load(f)

max_num = 10000
min_num = 6000

z = np.arange(64)
# for module in range(2):
#     for sensor in range(12):
#         top = VVH_data[0]['SurfaceDetail'][module * 12 + sensor]['Top']
#         nogs = VVH_data[0]['Nogs'][module * 12 + sensor]
#         thr = 0
#         for i in range(64):
#             if nogs[i] > 90000:
#                 thr = i
#                 break
#         tar_pic_num = thr + 5
#         tar_img = os.path.join(img_base, '{:02}_{:02}'.format(module, sensor), 'ImageFilterWithStream_GPU_0_00000000_0_{:03}.png'.format(tar_pic_num))
#         aff_path = os.path.join('Q:/minami/affine_param', '{}-{:02}_aff.csv'.format(module, sensor))
#         pq_path = os.path.join('Q:/minami/affine_param', '{}-{:02}_pq.csv'.format(module, sensor))
#         pq_data = pd.read_csv(pq_path)
#         command_pixel2stage = '{} {} 0 {} {} {} -autominus {} {} -nojson {} {}'.format(pixel2stage_exe, tar_img, aff_path, basepath, '{}-{:02}'.format(module, sensor), max_num, min_num, pq_data['dx'][0], pq_data['dy'][0])
#         subprocess.run(command_pixel2stage)

cmap = plt.get_cmap('jet')
for module in range(2):
    for sensor in range(12):
        stage_path = os.path.join(basepath, '{}-{:02}_stage.csv'.format(module, sensor))
        stage_df = pd.read_csv(stage_path)
        plt.plot(stage_df['X'], stage_df['Y'], 'o', alpha=0.7, markersize=0.5, label='{}-{:02}'.format(module, sensor), color=cmap((module*12+sensor)/24))

plt.title('sensor overlap')
plt.xlabel('stage x [mm]')
plt.ylabel('stage y [mm]')
plt.xticks(np.arange(-1, 9))
plt.yticks(np.arange(-1, 6))
plt.grid()
plt.savefig(os.path.join(basepath, 'sensor_overlap_test.pdf'))