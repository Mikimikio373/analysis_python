import os
import shutil
import sys
import cv2
import cupy as cp
import numpy as np
from matplotlib import pyplot as plt
import time
from matplotlib.backends.backend_pdf import PdfPages

if not len(sys.argv) == 2:
    exit('exception : usage : input png file path')
if not sys.argv[1][-4:] == '.png':
    exit('exception : usage : input png file path')
img_path = sys.argv[1]

path_list = os.path.split(img_path)
output_dir = os.path.join(path_list[0], 'fft')
os.makedirs(output_dir, exist_ok=True)
shutil.copy2(img_path, os.path.join(output_dir, path_list[1]))

fft_path1 = os.path.join(output_dir, path_list[1][:-4] + '_fft.png')
fft_path2 = os.path.join(output_dir, path_list[1][:-4] + '_fftbar.png')

img = cv2.imread(img_path, 0)
half_width = int(len(img[0]) / 2)
half_height = int(len(img) / 2)


f = np.fft.fft2(img)

fshift = np.fft.fftshift(f)

spectrum = np.abs(fshift)
spectrum_log = np.log10(spectrum)
if not len(img[0]) % 2 == 0:
    x = np.concatenate([np.arange(-(half_width - 1), 1), np.arange(half_width) + 1])
else:
    x = np.concatenate([np.arange(-(half_width - 1), 1), np.arange(half_width)])
if not len(img) % 2 == 0:
    y = np.concatenate([np.arange(-(half_height - 1), 1), np.arange(half_height + 1)])
else:
    y = np.concatenate([np.arange(-(half_height - 1), 1), np.arange(half_height)])
xx, yy = np.meshgrid(x, y)
fig, ax = plt.subplots()
im = ax.pcolormesh(xx, yy, spectrum_log, cmap='gray')
fig.colorbar(im, ax=ax, label='log10')
plt.savefig(fft_path2, dpi=600)

max_spect = np.max(spectrum_log)
min_spect = np.min(spectrum_log)
if min_spect < 0:
    spectrum_log  = spectrum_log - min_spect
img_spect = (spectrum_log * 255 / (max_spect - min_spect)).astype(np.uint8)
cv2.imwrite(fft_path1, img_spect)

