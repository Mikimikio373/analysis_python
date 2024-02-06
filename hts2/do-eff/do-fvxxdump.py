import os
import shutil
import subprocess

basepath = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8'
f_dump_path = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8/fvxx_dump2root.bat'

ori_copy = os.path.join(basepath, '4copy')
width_list = [2252, 2458, 2662, 2896, 3072]
height_list = [1196, 1306, 1414, 1538, 1632]
thr_s_list = [9, 9, 9, 9, 8]
thr_e_list = [13, 13, 13, 11, 12]

# width_list = [2252]
# height_list = [1196]
# thr_s_list = [13]
# thr_e_list = [13]

for width, height, thr_s, thr_e in zip(width_list, height_list, thr_s_list, thr_e_list):

    dirname = 'cubic_{}-{}'.format(width, height)

    # basepathへ移動
    os.chdir(basepath)
    current_dir = os.getcwd()
    print('current directory: {}'.format(current_dir))


    for i in range(thr_s, thr_e + 1):
        os.chdir(os.path.join(basepath, dirname))
        current_dir = os.getcwd()
        print('current directory: {}'.format(current_dir))

        # pl088に移動
        thr_name = '{}{}'.format(i, i - 1)
        os.chdir(os.path.join(thr_name, 'area1', 'PL088'))
        current_dir = os.getcwd()
        print('current directory: {}'.format(current_dir))

        # fvxx_dump2rootの実行
        command_dump = '{} 88'.format(f_dump_path)
        subprocess.run(command_dump, shell=True)

        # eff.datのコピー
        shutil.copy2('../ana/efficiency/088/eff_data.dat', 'eff_data.csv')


