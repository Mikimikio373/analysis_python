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

x = np.arange(len(Hz_list))
plt.plot(x, Hz_list, 'x', ms=0.2)
plt.xlabel('Number Of View', fontsize=15)
plt.ylabel('Frequency [Hz]', fontsize=15)
plt.grid()
print(np.mean(Hz_list))
plt.show()