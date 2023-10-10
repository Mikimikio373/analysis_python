import yaml
import json

out_list = []

# for module in range(6):
#     for sensor in range(12):
#         tmp = {'module': module, 'sensor': sensor, 'id': module * 12 + sensor, 'pos': 0}
#         out_list.append(tmp)
#
# with open('C:/Users/flab/analysis_python/hts2/scan_check_tool/sensor_pos.yml', 'w') as f:
#     yaml.safe_dump(out_list, f, default_flow_style=False, sort_keys=False)
#
# with open('C:/Users/flab/analysis_python/hts2/scan_check_tool/sensor_pos.json', 'w') as f:
#     json.dump(out_list, f, indent=2)

with open('C:/Users/flab/analysis_python/hts2/scan_check_tool/sensor_pos.yml', 'rb') as f:
    y_load = yaml.safe_load(f)

with open('C:/Users/flab/analysis_python/hts2/scan_check_tool/sensor_pos.json', 'w') as f:
    json.dump(y_load, f, indent=2)

# y_sorted = sorted(y_load, key=lambda x: x['pos'])
#
# for i in range(len(y_sorted)):
#     print(y_sorted[i])

