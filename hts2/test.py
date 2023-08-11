import os

basepath = 'Q:/minami/20230811_dip/1-7/0.5um'
os.chdir(basepath)
current_dir = os.getcwd()
print('directory changed, current path: {}'.format(current_dir))
count = 8
for i in range(400):
    tar_file_name = '20230811T170{:03}'.format(i)
    if not os.path.exists(tar_file_name):
        continue

    os.rename(tar_file_name, '{}'.format(count))
    count += 1