import math
import os.path
import sys

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors

mt1 = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8/noncubic/1413ph7_vph2/area1/PL088/f0881_tan1cut.txt'
# mt1 = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8/HTS1data/f0882_tan1cut.txt'
# mt2 = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8/noncubic/1413ph7_vph2/area1/PL088/nonkaidancut/f0882.txt'
mt2 = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8/1110ph7_vph2/area1/PL088/f0882.txt'
mt1_csvout = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8/noncubic/1413ph7_vph2/area1/PL088/f0881_tan1cut.csv'
# mt1_csvout = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8/HTS1data/f0882_tan1cut.csv'
mt2_csvout = 'Q:/minami/netscandata/GRAINE2023pl088_0906gap4.8/1110ph7_vph2/area1/PL088/f0882.txt'
out = 'B:/data/powerpoint/HTS2_meeting/20240109'

print('txt2csv')
print('read now')
with open(mt2, 'r') as f:
    mt2_txt = f.read()
    mt2_csv = mt2_txt.replace(' ', ',')
print('write now')
with open(mt2_csvout, 'w') as f:
    f.write(mt2_csv)
