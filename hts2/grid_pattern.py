import os.path

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 361, 9)
y = np.arange(0, 251, 5)

savepath = 'B:/data/powerpoint/HTS2_data/4master_theisis/stage_move'

plt.hlines(y=y, xmax=max(x), xmin=min(x), alpha=0.5, color="tab:orange", lw=0.5)
plt.vlines(x=x, ymax=max(y), ymin=min(y), alpha=0.5, color="tab:orange", lw=0.5)
plt.quiver(4.5, 2.5, 351, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=1, color='b')
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('Stage X [mm]', fontsize=16)
plt.ylabel('Stage Y [mm]', fontsize=16)
plt.title('Top layer', fontsize=20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
step1 = os.path.join(savepath, 'step1.png')
plt.savefig(step1, dpi=300)

plt.quiver(4.5, 7.5, 351, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=1, color='b')

step3 = os.path.join(savepath, 'step3.png')
plt.savefig(step3, dpi=300)

vec_y = np.arange(12.5, 251, 5)
vec_x = np.ones(len(vec_y)) * 4.5
vec_u = np.ones(len(vec_y)) * 351
vec_v = np.ones(len(vec_y)) * 0
plt.quiver(vec_x, vec_y, vec_u, vec_v, angles='xy', scale_units='xy', scale=1, units='xy', width=1, color='b')
top_all = os.path.join(savepath, 'topall.png')
plt.savefig(top_all, dpi=300)
plt.clf()

plt.hlines(y=y, xmax=max(x), xmin=min(x), alpha=0.5, color="tab:cyan", lw=0.5)
plt.vlines(x=x, ymax=max(y), ymin=min(y), alpha=0.5, color="tab:cyan", lw=0.5)
plt.quiver(355.5, 2.5, -351, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=1, color='tab:orange')
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('Stage X [mm]', fontsize=16)
plt.ylabel('Stage Y [mm]', fontsize=16)
plt.title('Bottom layer', fontsize=20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
step2 = os.path.join(savepath, 'step2.png')
plt.savefig(step2, dpi=300)

plt.quiver(355.5, 7.5, -351, 0, angles='xy', scale_units='xy', scale=1, units='xy', width=1, color='tab:orange')
step4 = os.path.join(savepath, 'step4.png')
plt.savefig(step4, dpi=300)

vec_x = np.ones(len(vec_y)) * 355.5
vec_u = np.ones(len(vec_y)) * -351
plt.quiver(vec_x, vec_y, vec_u, vec_v, angles='xy', scale_units='xy', scale=1, units='xy', width=1, color='tab:orange')
bottom_all = os.path.join(savepath, 'bottomall.png')
plt.savefig(bottom_all, dpi=300)
