import json
import subprocess
import sys
import os

import numpy as np

basepath = 'Q:/minami/20230811_dip/1-7/0.5um'

for i in range(1, 51):
    tar_dir = os.path. join(basepath, '{}'.format(i))
    command = 'python piezo-z.py {}'.format(tar_dir)
    # print(command)
    subprocess.run(command, shell=True)