import json
import matplotlib.pyplot as plt
from statistics import mean, stdev
import numpy as np


imager_num = 24

data_list = []
for i in range(imager_num):
    data_list.append([[], []])


for pl in range(3, 7):
    for area in range(1, 3):
        path = 'P:/usuda/u19-{:03}-a{}/ali.json'.format(pl, area)
        with open(path, 'rb') as f:
            param = json.load(f)
            for i in range(imager_num):
                data_list[i][0].append(param['ali_imager'][i]['Aff_coef_offset'][4]*1000)
                data_list[i][1].append(param['ali_imager'][i]['Aff_coef_offset'][5]*1000)

meanx = mean(data_list[3][0])
meany = mean(data_list[3][1])
for i in range(imager_num):
    print(mean(data_list[i][0]))
    data_list[i][0] = np.asarray(data_list[i][0]) - meanx
    print(mean(data_list[i][0]))
    data_list[i][1] = np.asarray(data_list[i][1]) - meany

for i in range(imager_num):
    plt.hist(data_list[i][0], bins=50, range=(-1, 1))
    plt.title('ali offset (Imager = {})'.format(i))
    plt.xlabel("offset X [um]")
    print('imager: {}, mean: {:.4g}, stdev: {:.4g}'.format(i, mean(data_list[i][0]), stdev(data_list[i][0])))
    plt.show()

