import csv
import os.path
import sys


def ssv2csv(filename: str):
    print(filename + ' open')
    outname = os.path.splitext(filename)[0] + '.csv'
    with open(filename, 'r') as f:
        mt2_txt = f.read()
        mt2_csv = mt2_txt.replace(' ', ',')
    print('write now')
    with open(outname, 'w') as f:
        f.write(mt2_csv)
    print('{} written'.format(outname))


fname = sys.argv[1]
ssv2csv(fname)
