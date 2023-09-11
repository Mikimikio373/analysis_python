import json
import math
import os.path
import subprocess

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

base_path = 'Q:/minami/20230910_nog2'
pdf_mode = 0    # 0:off 1:on
gap = 0.5

fig = plt.figure(tight_layout=True)
peak_list = []
for i in range(2):
    peak_list.append([])
for i in range(2):
    for j in range(12):
        peak_list[i].append([])

for num in range(1,2):
    if pdf_mode == 1:
        pdf = PdfPages(os.path.join(base_path, '{}'.format(num), 'nogplot.pdf'))
    else:
        pdf = 0
    path = os.path.join(base_path, '{}'.format(num), 'ValidViewHistory.json')
    param_path = os.path.join(base_path, '{}'.format(num), 'PARAMS', 'UserParam.json')

    if not os.path.exists(path):
        print('there not file: {}'.format(path))
        continue
    with open(path, 'rb') as f:
        json_file = json.load(f)
    with open(param_path, 'rb') as f:
        param_file = json.load(f)

    gap = param_file['LayerParam']['CommonParamArray'][0]['ThickOfLayer'] / param_file['LayerParam']['CommonParamArray'][0]['NPicThickOfLayer']
    npicnum = int(param_file['LayerParam']['CommonParamArray'][0]['NPicSnap'])
    z = np.arange(npicnum)
    z = z * gap


    for take in range(len(json_file)):
        max_index_list = []
        for i in range(24):
            max_index = json_file[take]['Nogs'][i].index(max(json_file[take]['Nogs'][i]))
            max_index_list.append(max_index)
            if pdf_mode == 1:
                ax = fig.add_subplot(111)
                ax.scatter(z, json_file[take]['Nogs'][i], marker='x')
                ax.axvline(x=z[max_index], c='r')
                ax.set_title('take:{} module:{} sensor:{}'.format(take, math.floor(i / 12), i % 12))
                ax.set_xlabel('z [um]')
                ax.set_ylabel('number of pit pixel')
                pdf.savefig()
                fig.clf()

        if min(max_index_list) == 0 or max(max_index_list) == 63:
            print('take: {} skipped'.format(take))
            continue
        for i in range(24):
            #1-7が19番目
            peak_list[math.floor(i / 12)][i % 12].append(max_index_list[i] - max_index_list[19])

    print('num: {} endded'.format(num))
    if pdf_mode == 1:
        pdf.close()

out_df = pd.DataFrame()
for i in range(24):
    out_df['{}-{}'.format(math.floor(i / 12), i % 12)] = peak_list[math.floor(i / 12)][i % 12]

out_path = os.path.join(base_path, 'peak_list.csv')
out_df.to_csv(out_path, index=False)


x_list = []
y_list = []
z_list = []
zerr_list = []
module_flag = []
x_width = 1.177
y_width = 0.572
for i in range(24):
    if math.floor(i / 12) == 0:
        flag = 0
        if i % 4 == 0:
            x = x_width * 2.5
        elif i % 4 == 1:
            x = x_width * 0.5
        elif i % 4 == 2:
            x = -x_width * 1.5
        else:
            x = -x_width * 3.5
        if math.floor(i / 4) == 0:
            y = - y_width * 3
        elif math.floor(i / 4) == 1:
            y = 0
        else:
            y = y_width * 3
    else:
        flag = 1
        if i % 4 == 0:
            x = x_width * 3.5
        elif i % 4 == 1:
            x = x_width * 1.5
        elif i % 4 == 2:
            x = -x_width * 0.5
        else:
            x = -x_width * 2.5

        if math.floor((i - 12) / 4) == 0:
            y = y_width * 3
        elif math.floor((i - 12) / 4) == 1:
            y = 0
        else:
            y = -y_width * 3


    x_list.append(x)
    y_list.append(y)
    peak_z = np.mean(peak_list[math.floor(i / 12)][i % 12]) * gap
    peak_z_err = np.std(peak_list[math.floor(i / 12)][i % 12]) / math.sqrt(len(peak_list[math.floor(i / 12)][i % 12])) * gap
    z_list.append(peak_z)
    zerr_list.append(peak_z_err)
    module_flag.append(flag)

xyz_df = pd.DataFrame()
xyz_df['x'] = x_list
xyz_df['y'] = y_list
xyz_df['z'] = z_list
xyz_df['z_err'] = zerr_list
xyz_df['flag'] = module_flag
out_path2 = os.path.join(base_path, 'xyz.csv')
xyz_df.to_csv(out_path2, index=False)

python_path = 'C:/Users/flab/discord/post.py'
command = 'python {} nogplot ended -user mikio'.format(python_path)
# subprocess.run(command)

