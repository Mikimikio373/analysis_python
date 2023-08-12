import os
import sys

if not len(sys.argv) == 2:
    sys.exit('command line error, \"tar dir\"')

tar_dir = sys.argv[1]
os.chdir(tar_dir)
current_dir = os.getcwd()
print('directory changed, current path: {}'.format(current_dir))


for a in range(1, 12):
    tar_file_name = '1_{:02}'.format(a)
    if not os.path.exists(tar_file_name):
        continue

    # print(tar_file_name, a + 1)
    os.rename(tar_file_name, '{}'.format(a + 1))
