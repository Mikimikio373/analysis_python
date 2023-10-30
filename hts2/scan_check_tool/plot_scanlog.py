import os
import matplotlib.pyplot as plt
import numpy as np

basepath = 'B:/data/powerpoint/F2F/F2F20231027/data'

log_path = os.path.join(basepath, 'scan_log.txt')

with open(log_path) as f:
    l = f.readlines()

print(float(l[0].split(',')[1][16:22]))
Hz_list = []
for i in range(len(l)):
    Hz_list.append(float(l[i].split(',')[1][16:22]))

print(np.mean(Hz_list))