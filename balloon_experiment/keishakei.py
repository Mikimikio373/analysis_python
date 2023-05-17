import pandas as pn
import sys
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
import datetime
from matplotlib.backends.backend_pdf import PdfPages


def plot_angle(fig, pdfdata, pndata, index, cmap, cmap_num):
    ax = fig.add_subplot(111)
    ax.plot('time', index, data=pndata, marker='x', lw=0.5, c=cmap(cmap_num))
    ax.set_title(index, fontsize=15)
    ax.set_xlim(np.array(pndata['time'])[0], np.array(pndata['time'])[-1])
    Minute_fmt = mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S")
    ax.xaxis.set_major_formatter(Minute_fmt)
    ax.set_ylabel('(tanθ)')
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    pdfdata.savefig()
    fig.clf()
    cmap_num += 1
    return cmap_num


print(len(sys.argv))
if len(sys.argv) < 2:
    sys.exit('command line error, please input csv path')
path = sys.argv[1]
edit_path = path[:-4] + '_edit.csv'
pdf_path = path[:-4] + '.pdf'
print(path)
print(edit_path)
print(pdf_path)
if not os.path.exists(path):
    sys.exit('there are not tha path :{}'.format(path))
input = pn.read_csv(path)

input = input.drop(input.index[0:2])
input = input.drop(columns=['No.7', 'No.8'])
input = input.reset_index(drop=True)
print(len(input))
a = 0.2167
b = 0.5432
x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []
time_all = []

for i in range(0, len(input)):
    # print(input['No.1'][i])
    tan1 = a * float(input['No.1'][i]) - b
    tan2 = a * float(input['No.2'][i]) - b
    tan3 = a * float(input['No.3'][i]) - b
    tan4 = a * float(input['No.4'][i]) - b
    tan5 = a * float(input['No.5'][i]) - b
    tan6 = a * float(input['No.6'][i]) - b
    x1.append(-tan1)
    y1.append(-tan2)
    x2.append(tan3)
    y2.append(tan4)
    x3.append(tan6)
    y3.append(-tan5)
    time_all.append(datetime.datetime.strptime(input['Date/Time'][i], '%Y-%m-%d %H:%M:%S'))

input['time'] = time_all
input['x1'] = x1
input['y1'] = y1
input['x2'] = x2
input['y2'] = y2
input['x3'] = x3
input['y3'] = y3
input['x1-x2'] = np.array(x1) - np.array(x2)
input['y1-y2'] = np.array(y1) - np.array(y2)
input['x3-x2'] = np.array(x3) - np.array(x2)
input['y3-y2'] = np.array(y3) - np.array(y2)

input = input[:-5]

input.to_csv(edit_path, index=False)

fig = plt.figure(tight_layout=True)
cmap_num = 0
cmap = plt.get_cmap("tab10")
out_pdf = PdfPages(pdf_path)
for i in range(1, 4):
    cmap_num = plot_angle(fig, out_pdf, input, 'x{}'.format(i), cmap, cmap_num)
for i in range(1, 4):
    cmap_num = plot_angle(fig, out_pdf, input, 'y{}'.format(i), cmap, cmap_num)

cmap_num = plot_angle(fig, out_pdf, input, 'x1-x2', cmap, cmap_num)
cmap_num = plot_angle(fig, out_pdf, input, 'y1-y2', cmap, cmap_num)
cmap_num = plot_angle(fig, out_pdf, input, 'x3-x2', cmap, cmap_num)
cmap_num = plot_angle(fig, out_pdf, input, 'y3-y2', cmap, cmap_num)
out_pdf.close()
