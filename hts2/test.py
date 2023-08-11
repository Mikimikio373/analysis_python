import json
import sys
import os

import numpy as np

if not len(sys.argv) == 2:
    sys.exit('command line error. please input \"basepath\"')

basepath = sys.argv[1]

z_list = []
for i in range(1, 51):
    tar_json = os.path.join(basepath, '{}'.format(i), 'image.json')
    with open(tar_json, 'r') as f:
        j = json.load(f)

    z_list.append(float(j['Images'][0]['stagez']))

out_csv = os.path.join(basepath, 'stagez.csv')
np.savetxt(out_csv, np.asarray(z_list), delimiter=',')