import os
import sys
import datetime

csv_dir = '/Users/minamihideyuki/data/lab/for_Australia/pressure_chech'

# input_filename = '20230310_leaktest3.csv'
# input_filepath = os.path.join(csv_dir, 'logging_data', 'diff_press', input_filename)
# plus_filename = '20230328_press.csv'
# plus_filepath = os.path.join(csv_dir, 'logging_data', 'diff_press', plus_filename)

input_filename = '20230310_leaktest3.csv'
input_filepath = os.path.join(csv_dir, 'logging_data', 'diff_press', input_filename)
plus_filename = '20230429_press.csv'
plus_filepath = os.path.join(csv_dir, 'logging_data', 'diff_press', plus_filename)

dt_now = datetime.datetime.now()
dt_now_str = dt_now.strftime('%Y%m%d')

output_filename = 'all_diff_press_{}.csv'.format(dt_now_str)
output_filepath = os.path.join(csv_dir, output_filename)

mode = 0    #mode0は、差圧データを統合

if not os.path.exists(input_filepath):
    sys.exit('there is not file: {}'.format(input_filepath))
input_f = open(os.path.join(csv_dir, input_filepath), 'r')
input_f_data = input_f.readlines()
input_f.close()

output_data = input_f_data

if not os.path.exists(plus_filepath):
    sys.exit('there is not file: {}'.format(plus_filepath))
plus_f1 = open(plus_filepath, 'r')
plus_f1_data = plus_f1.readlines()
plus_f1.close()

if mode == 0:
    output_data += plus_f1_data[3:]

output_f = open(output_filepath, 'w')
output_f.writelines(output_data)
output_f.close()
