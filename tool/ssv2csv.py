import csv
import os.path
import sys


def ssv2csv(filename: str):
    print(filename + ' open')
    outname = os.path.splitext(filename)[0] + '.csv'
    with open(filename, 'r') as i, open(outname, 'w') as o:
        reader = csv.reader(i, delimiter=' ', skipinitialspace=True)
        print(reader)
        writer = csv.writer(o)
        writer.writerows(reader)
    print(outname + ' written')


fname = sys.argv[1]
ssv2csv(fname)
