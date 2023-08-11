import csv
import os
import json
import sys

import numpy as np
from matplotlib import pyplot as plt

if not len(sys.argv) == 2:
    sys.exit('command line error. please input \"basepath\"')

basepath = sys.argv[1]

json_path = os.path.join(basepath, 'image.json')
with open(json_path, 'r') as f:
    j = json.load(f)


piezo_list = []
for i in range(len(j['Images'])):
    piezo_list.append(float(j['Images'][i]['piezoz']) * 1000)

x = np.arange(len(j['Images']))

p, cov = np.polyfit(x[2:-7], piezo_list[2:-7], 1, cov=True)
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
plt.axvline(x=x[2], c='r')
plt.axvline(x=x[-8], c='r')
plt.grid()
plt.legend()
plt.savefig(os.path.join(basepath, 'image_json.png'), dpi=300)
# plt.show()
plt.clf()

sigma_y = np.sqrt(1/(len(x[2:-8]) - 2) * np.sum([(a*x1+b-y1)**2 for x1, y1 in zip(x[2:-8], piezo_list[2:-8])]))
print(sigma_y)
y_err = np.asarray(piezo_list) - np.asarray(y_fit)
plt.hist(y_err[2:-8])
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

