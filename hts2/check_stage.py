import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages

basepath = 'Q:/minami/20230912_Ali2/Module0/sensor-3'
x_path = os.path.join(basepath, 'chech_sage_x.csv')
y_path = os.path.join(basepath, 'chech_sage_y.csv')
pdf_path = os.path.join(basepath, 'chech_step.pdf')
out_pdf = PdfPages(pdf_path)
cmap = plt.get_cmap('tab10')
print(cmap)

x_pd = pd.read_csv(x_path)
y_pd = pd.read_csv(y_path)

nx = 10
ny = 19
num = 0

vx_list = []
vy_list = []

dx_list = []
dy_list = []
for i in range(len(x_pd['index'])):
    index = x_pd['index'][i]
    vx_list.append(int(index[2:4]))
    dx_list.append(x_pd['dx'][i] * 1000)
    dy_list.append(x_pd['dy'][i] * 1000)

plt.scatter(vx_list, dx_list, marker='x', c=cmap(num))
num += 1
plt.title('step x - dx')
plt.xlabel('number of step [/1.17mm]')
plt.ylabel('dx [um]')
out_pdf.savefig()
plt.clf()

plt.scatter(vx_list, dy_list, marker='x', c=cmap(num))
num += 1
plt.title('step x - dy')
plt.xlabel('number of step [/1.17mm]')
plt.ylabel('dy [um]')
out_pdf.savefig()
plt.clf()

dx_list = []
dy_list = []
vy_list_cut = []
dy_list_cut = []
for i in range(len(y_pd['index'])):
    index = y_pd['index'][i]
    vy_list.append(int(index[6:8]))
    dx_list.append(y_pd['dx'][i] * 1000)
    dy_list.append(y_pd['dy'][i] * 1000)
    if y_pd['dy'][i] * 1000 < -0.6:
        continue
    vy_list_cut.append(int(index[6:8]))
    dy_list_cut.append(y_pd['dy'][i] * 1000)

plt.scatter(vy_list, dx_list, marker='x', c=cmap(num))
num += 1
plt.title('step y - dx')
plt.xlabel('number of step [/0.56mm]')
plt.ylabel('dx [um]')
plt.xticks(np.arange(19))
out_pdf.savefig()
plt.clf()

plt.scatter(vy_list, dy_list, marker='x', c=cmap(num))
num += 1
plt.title('step y - dy')
plt.xlabel('number of step [/0.56mm]')
plt.ylabel('dy [um]')
plt.xticks(np.arange(19))
out_pdf.savefig()
plt.clf()

plt.scatter(vy_list_cut, dy_list_cut, marker='x', c=cmap(num))
num += 1
plt.title('step y - dy cut')
plt.xlabel('number of step [/0.56mm]')
plt.ylabel('dy [um]')
plt.xticks(np.arange(19))
out_pdf.savefig()
plt.clf()


out_pdf.close()
