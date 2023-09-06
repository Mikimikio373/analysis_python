import csv
import os
import json
import sys

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

if len(sys.argv) == 2:
    basepath = sys.argv[1]
    starskip = 0
    endskip = 0
elif len(sys.argv) == 4:
    basepath = sys.argv[1]
    starskip = int(sys.argv[2])
    endskip = int(sys.argv[3])
else:
    sys.exit('use error. please input \"basepath\", (\"start skip num\", \"end skip num\")')

print(basepath)
json_path = os.path.join(basepath, 'image.json')
with open(json_path, 'r') as f:
    j = json.load(f)


piezo_list = []
skip_list = []
for i in range(len(j['Images'])):
    if j['Images'][i]['piezoz'] == 0.0:
        skip_list.append(i)
        print('detect skip point {}'.format(i))
    piezo_list.append(float(j['Images'][i]['piezoz']) * 1000)


x = np.arange(len(j['Images']))

for i in range(len(skip_list)):
    tmp1 = piezo_list.pop(skip_list[i])
    x = x[x != skip_list[i]]

delete_num = -endskip - len(skip_list)
if delete_num == 0:
    x_fix = x
    piezo_list_fix = piezo_list
else:
    x_fix = x[starskip:delete_num]
    piezo_list_fix = piezo_list[starskip:delete_num]

p, cov = np.polyfit(x_fix, piezo_list_fix, 1, cov=True)
a = p[0]
b = p[1]
a_err = np.sqrt(cov[0, 0])
b_err = np.sqrt(cov[1, 1])
print(p)
print(a_err, b_err)

y_fit = a * x + b

plt.plot(x, piezo_list, '-x')
plt.plot(x, y_fit, '-', label='y = {:.3g} $\pm$ {:.3g} x + ({:.3g} $\pm$ {:.3g})'.format(a, a_err, b, b_err))
plt.xlabel('number of picture')
plt.ylabel('z [um]')
plt.axvline(x=x_fix[0], c='r')
plt.axvline(x=x_fix[-1], c='r')
plt.grid()
plt.legend()
plt.savefig(os.path.join(basepath, 'image_json.png'), dpi=300)
# plt.show()
plt.clf()

sigma_y = np.sqrt(1/(len(x_fix)) * np.sum([(a*x1+b-y1)**2 for x1, y1 in zip(x_fix, piezo_list_fix)]))
print(sigma_y)
if delete_num == 0:
    y_err = np.asarray(piezo_list) - np.asarray(y_fit)
else:
    y_err = np.asarray(piezo_list_fix) - np.asarray(y_fit[starskip:delete_num])
plt.hist(y_err[2:-8], bins=50, range=(-0.5, 0.5))
plt.xlabel('data - fit [um]')
plt.ylabel('entries')
plt.title('σ = {:.3g}'.format(sigma_y))
plt.savefig(os.path.join(basepath, 'fit_error.png'), dpi=300)
# plt.show()
plt.clf()

with open(os.path.join(basepath, 'fitdata.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['a', a])
    writer.writerow(['b', b])
    writer.writerow(['a_err', a_err])
    writer.writerow(['b_err', b_err])
    writer.writerow(['fit err', sigma_y])

z_data_df = pd.DataFrame()
z_data_df['piezo z'] = piezo_list
z_data_df['fit z'] = y_fit
z_data_df.to_csv(os.path.join(basepath, 'piezo_z.csv'), index=False)
