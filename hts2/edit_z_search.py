import json
import pandas as pn

ref_path = "R:\\minami\\20230609_ali-z\\Module1\\sensor-7\\ori\\IMAGE00_AREA-1\\V00000000_L0_VX0000_VY0000_0_064.json"
compare_path = "R:\\minami\\20230609_ali-z\\Module0\\sensor-6\\IMAGE00_AREA-1\\V00000000_L0_VX0000_VY0000_0_064.json"

ref_json = open(ref_path, 'r')
ref_j = json.load(ref_json)

compare_json = open(compare_path, 'r')
compare_j = json.load(compare_json)

csv_path = 'R:\\minami\\20230609_ali-z\\Module1\\sensor-7\\ori\\IMAGE00_AREA-1\\png\\GrainMatching4z-match\\z_search.csv'
pn_data = pn.read_csv(csv_path)


ref_num = int(pn_data['name'][0][5:8])
first = int(pn_data['name'].iloc[0][9:])
last = int(pn_data['name'].iloc[-1][9:])

picnumkust = []
dz_list = []
for i in range(first, last + 1):
    dz = compare_j['Images'][i]['z'] - ref_j['Images'][ref_num]['z']
    dz *= 1000
    picnumkust.append(i)
    dz_list.append(dz)

pn_data['picnum'] = picnumkust
pn_data['dz'] = dz_list
pn_data = pn_data.drop('entries_y', axis=1)
pn_data = pn_data.rename(columns={'entries_x': 'entries'})
pn_data = pn_data.reindex(columns=['name', 'picnum', 'dz', 'height_x', 'mean_x', 'sigma_x', 'height_y', 'mean_y', 'sigma_y', 'entries'])

out_path = csv_path[:-4] + '_edit.csv'
pn_data.to_csv(out_path)