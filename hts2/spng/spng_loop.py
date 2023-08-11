import os
import subprocess

basepath = 'Q:/minami/20230810_ali-z/Module1/sensor-7'

for i in range(1, 51):
    tar_dir = os.path.join(basepath, 'pich0.5um-{}'.format(i))
    command = 'python C:/Users/flab/analysis_python/hts2/spng_open_v2.py {}'.format(tar_dir)
    subprocess.run(command, shell=True)