import json
import os
import sys

import numpy as np
import cv2
from statistics import mean, stdev

import struct
import matplotlib.pyplot as plt


vvh_path = 'Q:/minami/HTS_scandata/unit4-pl88_30-30/ValidViewHistory.json'
with open(vvh_path, 'rb') as f:
    vvh = json.load(f)

module = 2
sensor = 0

for module in (range(3)):
    for sensor in range(12):
        imager = 12 * module + sensor
        print(imager)
        noglist = []
        picnum = 0
        for i in range(144):
            filename = "Q:/minami/HTS_scandata/unit4-pl88_30-30/IMAGE/{:02}_{:02}/ImageFilterWithStream_GPU_2_{:08}_0_024.spng".format(module, sensor, i)
            if not os.path.exists(filename):
                continue
            print(filename)
            out = os.path.join(os.path.join(os.path.dirname(filename), 'png'))
            os.makedirs(out, exist_ok=True)
            size = os.path.getsize(filename)
            f = open(filename, "rb")
            first = vvh[i]['StartAnalysisPicNo'][imager]
            last = first + 16
            cnt = 0
            while True:
                if f.tell() == size:break
                n_bytes = struct.unpack('Q', f.read(8))[0]
                data = np.fromfile(f, np.uint8, n_bytes, "", 0)
                dst = cv2.imdecode(data, -1)
                dst = dst * 255
                nog = cv2.countNonZero(dst)
                cnt += 1
                if first < cnt <= last:
                    picnum += 1
                    noglist.append(nog)

        histreturn = plt.hist(noglist, bins=50, histtype='stepfilled',
                     facecolor='yellow',
                     linewidth=1, edgecolor='black')
        factor = 0.9
        entries = len(noglist)
        ave = mean(noglist)
        std_dev = stdev(noglist)
        text = 'Entries: {:d}\nMean: {:4g}\nStd_dev: {:4g}'.format(entries, ave, std_dev)
        plt.text(max(histreturn[1]) * factor, max(histreturn[0]) * factor, text, bbox=(dict(boxstyle='square', fc='w')))
        # plt.show()
        out = 'B:/data/powerpoint/HTS2_data/4master_theisis/hts1_hitpixel/HTS-1_{}-{}_hitpixel.png'.format(module, sensor)
        plt.savefig(out, dpi=300)
        plt.clf()
        print(np.average(noglist))
        print(picnum, 16*144/2, 24*144/2)
