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

for width, height, thr_s, thr_e in zip(width_list, height_list, thr_s_list, thr_e_list):

    dirname = 'cubic_{}-{}'.format(width, height)

    # basepathへ移動
    os.chdir(basepath)
    current_dir = os.getcwd()
    print('current directory: {}'.format(current_dir))

    # dirの作製及び移動
    os.makedirs(dirname, exist_ok=True)

    for i in range(thr_s, thr_e + 1):
        os.chdir(os.path.join(basepath, dirname))
        current_dir = os.getcwd()
        print('current directory: {}'.format(current_dir))

        thr_name = '{}{}'.format(i, i - 1)

        # copy dirのコピー
        if not os.path.exists(thr_name):
            shutil.copytree(ori_copy, thr_name)

        tagert_fvxx1 = os.path.join(tracking_base,
                                    'tracking_cubic{}_{}_zfilt-0.40_180_5_6_{}-{}'.format(i, i - 1, width, height), 'mt2f',
                                    'f0881.vxx')
        tagert_fvxx2 = os.path.join(tracking_base,
                                    'tracking_cubic{}_{}_zfilt-0.40_180_5_6_{}-{}'.format(i, i - 1, width, height), 'mt2f',
                                    'f0882.vxx')

        shutil.copy2(tagert_fvxx1, os.path.join(thr_name, 'area1', 'PL088'))
        shutil.copy2(tagert_fvxx2, os.path.join(thr_name, 'area1', 'PL088'))
        print('fvxx copyed')

        os.chdir(os.path.join(thr_name, 'area1', 'PL088'))
        current_dir = os.getcwd()
        print('current directory: {}'.format(current_dir))
        command_clust = 'start {} 88 2'.format(f_filter_path)
        subprocess.run(command_clust, shell=True)


