import os.path
import subprocess

basepath = 'R:\\minami\\20221228_aff'
python_path = 'c:\\Users\\flab\\analysis_python\\do_calc_aff.py'
minus = 45
option = '111'
ori_path = os.getcwd()
for i in range(1, 2):
    for j in range(1, 13):
        module = 'Module{}'.format(i)
        sensor = 'sensor-{}'.format(j)
        target_path = os.path.join(basepath, module, sensor)
        os.chdir(target_path)
        print('path changed, current path: {}'.format(target_path))

        command_do_calc_aff = 'start python {} {} {}'.format(python_path, minus, option)
        print(command_do_calc_aff)
        subprocess.run(command_do_calc_aff, shell=True)

os.chdir(ori_path)