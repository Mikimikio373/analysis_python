import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

basepath = 'Q:/minami/affine_param/marge_test'

os.chdir(basepath)
concurrent_path = os.getcwd()
print(concurrent_path)

GM_stage = 'C:/Users/flab/source/repos/myproject/x64/Release/GrainMatching_in_Stage.exe'
calc_root = 'root -b -q -l C:/Users/flab/cpp_project/root/overlap.C'
x_list = []
for i in range(12):
    os.chdir(basepath)
    concurrent_path = os.getcwd()
    # print(concurrent_path)
    if i < 4:
        j = i + 8
    elif i < 8:
        j = i
    else:
        j = i - 8

    command_gmstage = '{0} 1-{1:02}_flip_stage.csv 0-{2:02}_flip_stage.csv overlap 01{1:02}vs00{2:02} -cutmode 0 0 0.0015'.format(GM_stage, i, j)
    # subprocess.run(command_gmstage, shell=True)

    os.chdir('overlap')
    command_root = '{}(\\\"01{:02}vs00{:02}\\\")'.format(calc_root, i, j)
    # subprocess.run(command_root, shell=True)

    overlap_csv = '01{:02}vs00{:02}_overlap.csv'.format(i, j)
    df = pd.read_csv(overlap_csv)
    # print(df['x_max'][0] - df['x_min'][0])
    # x_list.append((df['x_max'][0] - df['x_min'][0])*1000)
    x_list.append(df['x_mean'][0] * 1000)



for i in range(12):
    os.chdir(basepath)
    concurrent_path = os.getcwd()
    # print(concurrent_path)
    if i % 4 == 3:
        continue
    if i < 4:
        j = i + 9
    elif i < 8:
        j = i + 1
    else:
        j = i - 7

    command_gmstage = '{0} 0-{1:02}_flip_stage.csv 1-{2:02}_flip_stage.csv overlap 00{1:02}vs01{2:02} -cutmode 0 0 0.0015'.format(GM_stage, i, j)
    # subprocess.run(command_gmstage, shell=True)

    os.chdir('overlap')
    command_root = '{}(\\\"00{:02}vs01{:02}\\\")'.format(calc_root, i, j)
    # subprocess.run(command_root, shell=True)

    overlap_csv = '00{:02}vs01{:02}_overlap.csv'.format(i, j)
    df = pd.read_csv(overlap_csv)
    # print(df['x_max'][0] - df['x_min'][0])
    # x_list.append((df['x_max'][0] - df['x_min'][0])*1000)
    x_list.append(df['x_mean'][0]*1000)

print(len(x_list))
plt.hist(x_list, bins=50, range=(-0.3, 0.3))
plt.show()