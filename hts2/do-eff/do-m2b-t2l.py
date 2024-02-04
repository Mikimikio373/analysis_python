import os
import shutil
import subprocess

basepath = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8'
tracking_base = 'R:/usuda/GRAINE2023_u4/PL088_0906gap4.8um/IMAGE00_AREA-1'
f_filter_path = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8/f-filter_end.bat'

ori_copy = os.path.join(basepath, '4copy')
width_list = [2252, 2458, 2662, 3072]
height_list = [1196, 1306, 1414, 1632]
thr_s_list = [9, 9, 9, 8]
thr_e_list = [13, 13, 13, 12]
# width_list = [2252, 2458, 2662]
# height_list = [1196, 1306, 1414]
# thr_s_list = [9, 9, 9]
# thr_e_list = [13, 13, 13]

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

        thr_name = '{}{}'.format(i, i - 1)

        os.chdir(os.path.join(thr_name, 'work'))
        current_dir = os.getcwd()
        print('current directory: {}'.format(current_dir))

        # m2bの実行
        command_m2b = 'do-m2b_root6.bat 088 1'
        subprocess.run(command_m2b, shell=True)

        # linkletの実行
        command_t2l = 'do-linklet_root6.bat 087 088 1'
        subprocess.run(command_t2l, shell=True)

        # do-effの実行
        os.chdir(os.path.join(basepath, dirname, thr_name, 'area1', 'ana', 'efficiency'))
        current_dir = os.getcwd()
        print('current directory: {}'.format(current_dir))
        command_eff = 'do-eff 088'
        subprocess.run(command_eff, shell=True)


