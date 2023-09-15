import json
import math
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

json_path = 'Q:/minami/20230913_Ali/20230913_oneshot/ValidViewHistory.json'
pdf_path = 'Q:/minami/20230913_Ali/20230913_oneshot/nog_plot.pdf'
out_pdf = PdfPages(pdf_path)

with open(json_path, 'rb') as f:
    json_data = json.load(f)

z = np.arange(64)

for i in range(24):
    plt.scatter(z, json_data[0]['Nogs'][i], marker='x')
    plt.title("Module:{} sensor:{}".format(math.floor(i / 12), i % 12))
    plt.xlabel('number of picture [-/um]')
    plt.ylabel('nogs')
    plt.ylim(0, 120000)
    out_pdf.savefig()
    plt.clf()


out_pdf.close()
