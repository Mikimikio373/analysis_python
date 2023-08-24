import cv2
import cupy as cp
import numpy as np
from matplotlib import pyplot as plt
import time

img_path = 'Q:/minami/graine_u4/PL089/L0_VX0000_VY0000/L0_VX0000_VY0000_10.png'

time_list = []
start = time.perf_counter()
img = cv2.imread(img_path, 0)
end = time.perf_counter()
time_list.append(end - start)

start = time.perf_counter()
f = np.fft.fft2(img)
end = time.perf_counter()
time_list.append(end - start)

fshift = np.fft.fftshift(f)

spectrum = np.abs(fshift)
spectrum_log = np.log(spectrum)
x = np.concatenate([np.arange(-1023, 1), np.arange(1024)])
y = np.concatenate([np.arange(-543, 1), np.arange(544)])
xx, yy = np.meshgrid(x, y)
fig, ax = plt.subplots()
im = ax.contourf(xx, yy, spectrum_log)
fig.colorbar(im, ax=ax)
plt.show()
print(time_list)
