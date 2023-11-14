import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import check_stage_module as mylib

path1 = 'ali.json'
shift_data, int_data, stage = mylib.read_ali_stage(path1)

pdf = PdfPages('test.pdf')

X = shift_data[0].query('flag == 2')['X']
Y = shift_data[0].query('flag == 2')['Y']
U = shift_data[0].query('flag == 2')['U']
V = shift_data[0].query('flag == 2')['V']
stage_x = sorted(list(set(stage[0]["stage_x"])))
stage_y = sorted(list(set(stage[0]["stage_y"])))

fig = plt.figure()
ax = fig.add_subplot(111)

mylib.plot_stage_shift_vec(ax, pdf, X, Y, U, V, stage_x, stage_y, 'layer = 0 (X overlap)')
mylib.plot_stage_shift_scatter(fig, pdf, X, Y, U, V, 'layer = 0 (X overlap)')

pdf.close()

