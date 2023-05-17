import os
import sys
import datetime
import pandas as pn
import math


def CheckNoneLine(df):
    last_line_num = []
    for i in range(2, len(df.columns)):
        for j in range(1, len(df)):
            tmp = float(df.iloc[-j][i])
            if not math.isnan(tmp):
                last_line_num.append(j)
                break
    return max(last_line_num) - 1

base_dir = '/Users/minamihideyuki/data/lab/for_Australia/keishakei/'

dt_now = datetime.datetime.now()
dt_now_str = dt_now.strftime('%Y%m%d')

input_filepath = os.path.join(base_dir, 'all_tilt_from20230321_to20230430.csv')


output_filename = 'all_tilt_from20230321_to{}.csv'.format(dt_now_str)
output_filepath = os.path.join(base_dir, output_filename)

if not os.path.exists(input_filepath):
    sys.exit('there is not input file: {}'.format(input_filepath))
input_f = open(input_filepath, 'r')
input_f_data = input_f.readlines()
input_f.close()
input_pn = pn.read_csv(input_filepath)
input_last_time = float(input_pn.iloc[-1][1])
print('input last time: {}'.format(input_pn.iloc[-1][0]))

output_data = []
if len(sys.argv) > 1:
    plus_filepath = sys.argv[1]
    print(plus_filepath)
    if not os.path.exists(plus_filepath):
        sys.exit('there is not plus file: {}'.format(plus_filepath))
    plus_f = open(plus_filepath, 'r')
    plus_f_data = plus_f.readlines()
    plus_f.close()
    plus_pn = pn.read_csv(plus_filepath)
    delete_line_num = CheckNoneLine(plus_pn)
    print(delete_line_num)
    if not delete_line_num == 0:
        plus_f_data = plus_f_data[:-delete_line_num]
        plus_pn = plus_pn.drop(plus_pn.index[-delete_line_num:])
    print('plus data first time: {}'.format(plus_pn.iloc[3][0]))
    plus_first_time = float(plus_pn.iloc[3][1])
    if input_last_time >= plus_first_time:
        for i in range(3, len(plus_pn)):
            plus_time = float(plus_pn.iloc[i][1])
            if input_last_time >= plus_time:
                continue
            else:
                print('fixed time, input: {}, plus: {}'.format(input_pn.iloc[-1][0], plus_pn['Date/Time'][i]))
                output_data = input_f_data
                output_data += plus_f_data[i:]
                break
    else:
        output_data = input_f_data
        output_data += plus_f_data[3:]
else:
    output_data = input_f_data
    print('No command line arguments specified')

output_f = open(output_filepath, 'w')
output_f.writelines(output_data)
output_f.close()
