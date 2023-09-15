import os
import shutil
import glob
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

python_path = 'C:/Users/flab/analysis_python/hts2/image_process/deadpixel_seach.py'
for i in range(2):
    for j in range(12):
        command = 'start python {} {} {}'.format(python_path, i, j)
        print(command)
        subprocess.run(command, shell=True)