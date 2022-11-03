import numpy as np
import sys
import os
import pandas as pn
import math

area = '../A'

fit_csv = area + '/GrainMatching_loop/fitdata_edit.csv'
fit_pn = pn.read_csv(fit_csv, header=0)
# print(fit_pn)
print(len(fit_pn))
dx_all = []
dy_all = []

for i in range(0, len(fit_pn)):
    dx = fit_pn['sigmaX'][i] / math.sqrt(fit_pn['Entries'][i])
    dy = fit_pn['sigmaY'][i] / math.sqrt(fit_pn['Entries'][i])
    dx_all.append(dx)
    dy_all.append(dy)

fit_pn['dx'] = dx_all
fit_pn['dy'] = dy_all

fit_pn.to_csv(area + '/GrainMatching_loop/fitdata_edit.csv')

