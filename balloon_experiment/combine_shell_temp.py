import os
import sys
import datetime


def DeleteNoneLine(line_data):
    n = 1
    while True:
        last_line = line_data[-n][2]
        if not last_line == "":
            break

        n += 1
    return line_data[:-n]


base_dir = '/Users/minamihideyuki/data/lab/for_Australia/pressure_chech/'

dt_now = datetime.datetime.now()
dt_now_str = dt_now.strftime('%Y%m%d')

input_filepath = os.path.join(base_dir, 'all_temp_ondotori20230428.csv')
# input_filepath = os.path.join(base_dir, 'logging_data', 'temp_ondotori', 'TR-72wb_523671AE_20230403105348.csv')

output_filename = 'all_temp_ondotori{}.csv'.format(dt_now_str)
output_filepath = os.path.join(base_dir, output_filename)

if not os.path.exists(input_filepath):
    sys.exit('there is not input file: {}'.format(input_filepath))
input_f = open(input_filepath, 'r', encoding='shift_jis')
input_f_data = input_f.readlines()
input_f.close()
input_f_data = DeleteNoneLine(input_f_data)
input_last_line = input_f_data[-1].split(',')
input_last_time = datetime.datetime.strptime(input_last_line[0], '%Y/%m/%d %H:%M:%S')
print('input last time: {}'.format(input_last_line[0].replace('\"', '')))

output_data = []
if len(sys.argv) > 1:
    plus_filepath = sys.argv[1]
    print(plus_filepath)
    if not os.path.exists(plus_filepath):
        sys.exit('there is not plus file: {}'.format(plus_filepath))
    plus_f = open(plus_filepath, 'r', encoding='shift_jis')
    plus_f_data = plus_f.readlines()
    plus_f.close()
    plus_f_data = DeleteNoneLine(plus_f_data)
    plus_f_data = plus_f_data[4:]
    plus_first_line = plus_f_data[0].split(',')
    plus_first_time = datetime.datetime.strptime(plus_first_line[0], '%Y/%m/%d %H:%M:%S')
    print('plus data first time: {}'.format(plus_first_line[0]))
    if input_last_time >= plus_first_time:
        for i in range(len(plus_f_data)):
            plus_line = plus_f_data[i].split(',')
            plus_time = datetime.datetime.strptime(plus_line[0], '%Y/%m/%d %H:%M:%S')
            if input_last_time >= plus_time:
                continue
            else:
                print(i)
                print('fixed time, input: {}, plus: {}'.format(input_last_line[0], plus_line[0]))
                output_data = input_f_data
                output_data += plus_f_data[i:]
                break
    else:
        output_data = input_f_data
        output_data += plus_f_data
else:
    output_data = input_f_data
    print('No command line arguments specified')


output_f = open(output_filepath, 'w', encoding='shift_jis')
output_f.writelines(output_data)
output_f.close()
