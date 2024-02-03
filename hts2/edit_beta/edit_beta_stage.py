import csv
import json
import os


def read_fitparam(path: str):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    coef = [[], []]
    for j in range(len(coef)):
        for i in range(len(l[2 * j + 1])):
            coef[j].append(float(l[2 * j + 1][i]))

    dx, dy = coef
    return dx, dy


def quadratic_2var(x, y, coef):
    a, b, c, d, e, f = coef
    z = a * x * x + b * y * y + c * x * y + d * x + e * y + f
    return z


def cubic_2var(x, y, coef):
    a, b, c, d, e, f, g, h, i, j = coef
    z = a * x * x * x + b * y * y * y + c * x * x * y + d * x * y * y + e * x * x + f * y * y + g * x * y + h * x + i * y + j
    return z

def quad(x, y, coef):
    a, b, c, d, e, f, g, h, i, j, k, l ,m , n, o = coef
    z = a*x*x*x*x + b*y*y*y*y + c*x*x*x*y + d*x*x*y*y + e*x*y*y*y + f*x*x*x + g*y*y*y + h*x*x*y + i*x*y*y + j*x*x + k*y*y + l*x*y + m*x + n*y + o
    return z


tar_dir = 'A:/Test/check_FASER/m222-pl002_30cm-1'
fit_param_path = 'A:/Test/check_FASER/m222-pl002_30cm-1/fit_stage_quad/ali_stage_fittig-data.csv'

coef_dx, coef_dy = read_fitparam(fit_param_path)
print(coef_dx, coef_dy)

json_name = os.path.join(tar_dir, 'Beta_EachViewParam.json')

with open(json_name, 'rb') as f:
    eachview = json.load(f)

for i in range(len(eachview)):
    sx = eachview[i]['Stage_x']
    sy = eachview[i]['Stage_y']
    # print(type(sx), type(sy))
    # eachview[i]['Stage_x'] = sx - cubic_2var(sx, sy, coef_dx)
    # eachview[i]['Stage_y'] = sy - cubic_2var(sx, sy, coef_dy)
    eachview[i]['Stage_x'] = sx - quad(sx, sy, coef_dx)
    eachview[i]['Stage_y'] = sy - quad(sx, sy, coef_dy)

out_json_name = os.path.join(tar_dir, 'Beta_EachViewParam_edit.json')
with open(out_json_name, 'w') as f:
    json.dump(eachview, f, indent=2)

