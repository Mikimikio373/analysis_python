import os
import sys
import numpy as np
import cv2
import struct

if len(sys.argv) != 2:
    sys.exit('error, please input [filename.spng]')
filename = sys.argv[1]
if not os.path.exists(filename):
    sys.exit('there is no file: {}'.format(filename))
print('open: {}'.format(filename))
out = os.path.join(os.path.dirname(filename), os.path.splitext(os.path.basename(filename))[0])
os.makedirs(out, exist_ok=True)
size = os.path.getsize(filename)
f = open(filename, "rb")
cnt = 0
while True:
    if f.tell() == size:break
    n_bytes = struct.unpack('Q', f.read(8))[0]
    data = np.fromfile(f, np.uint8, n_bytes, "", 0)
    dst = cv2.imdecode(data, -1)
    dst = dst * 255
    outname = os.path.join(out, os.path.splitext(os.path.basename(filename))[0] + '_{}.png'.format(cnt))
    cv2.imwrite(outname, dst)
    cnt += 1

print('{} written'.format(out))