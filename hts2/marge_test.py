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

max_num = 100000
min_num = 40000

z = np.arange(64)
list_tar_pic_num = []
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
#         list_tar_pic_num.append(tar_pic_num)
#         tar_img = os.path.join(img_base, '{:02}_{:02}'.format(module, sensor), 'ImageFilterWithStream_GPU_0_00000000_0_{:03}.png'.format(tar_pic_num))
#         aff_path = os.path.join('Q:/minami/affine_param', '{}-{:02}_aff.csv'.format(module, sensor))
#         pq_path = os.path.join('Q:/minami/affine_param', '{}-{:02}_pq.csv'.format(module, sensor))
#         pq_data = pd.read_csv(pq_path)
#         command_pixel2stage = '{} {} 0 {} {} {} -autominus {} {} -nojson {} {}'.format(pixel2stage_exe, tar_img, aff_path, basepath, '{}-{:02}_flip'.format(module, sensor), max_num, min_num, -pq_data['dx'][0], -pq_data['dy'][0])
#         subprocess.run(command_pixel2stage)

# np.savetxt(os.path.join(basepath, 'z_number_list.csv'), np.asarray(list_tar_pic_num), delimiter=',')

plt.figure(tight_layout=True)
cmap = plt.get_cmap('jet')
for module in range(0, 2):
    for sensor in range(12):
        stage_path = os.path.join(basepath, '{}-{:02}_flip_stage.csv'.format(module, sensor))
        stage_df = pd.read_csv(stage_path)
        if module == 1:
            c = 'limegreen'
        else:
            c = 'r'
        plt.plot(stage_df['X'] + 8.9, stage_df['Y'] + 3.8, 'o', alpha=0.7, markersize=0.05, label='{}-{:02}'.format(module, sensor), color=c)
# plt.title('sensor overlap')
plt.xlabel('$X_{s}$ [mm]', fontsize=16)
plt.ylabel('$Y_{s}$ [mm]', fontsize=16)
plt.xticks(np.arange(-1, 10, 1), fontsize=14)
plt.yticks(np.arange(-1, 7, 1), fontsize=14)
plt.xlim(-0.5, 10)
plt.ylim(-0.5, 5.8)
plt.grid()
plt.gca().set_aspect('equal')
plt.savefig(os.path.join(basepath, 'sensor_overlap_4master_large.png'), dpi=300)
# plt.show()