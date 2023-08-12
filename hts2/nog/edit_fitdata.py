import json
import subprocess
import sys
import os

import numpy as np
import pandas as pd

basepath = 'Q:/minami/20230811_dip/1-7/0.5um'

for i in range(1, 51):
    tar_dir = os.path. join(basepath, '{}'.format(i))
    command = 'python piezo-z.py {}'.format(tar_dir)
    # print(command)
    subprocess.run(command, shell=True)

a_list = []
b_list = []
aerr_list = []
berr_list = []
fiterr_list = []
b_data = []

for i in range(1, 51):
    tar_csv = os.path. join(basepath, '{}'.format(i), 'fitdata.csv')
    df = pd.read_csv(tar_csv, header=None)
    a_list.append(df[1][0])
    b_list.append(df[1][1])
    aerr_list.append(df[1][2])
    berr_list.append(df[1][3])
    fiterr_list.append(df[1][4])

    tar_json = os.path.join(basepath, '{}'.format(i), 'image.json')
    with open(tar_json, 'r') as f:
        j = json.load(f)
    b_data.append(float(j['Images'][0]['piezoz']) *1000)

out_df = pd.DataFrame()
out_df['a'] = a_list
out_df['b'] = b_list
out_df['a err'] = aerr_list
out_df['b err'] = berr_list
out_df['fit err'] = fiterr_list
out_df['b data'] = b_data

out_csv = os.path.join(basepath, 'piezo-z_list.csv')
out_df.to_csv(out_csv, index=False)

