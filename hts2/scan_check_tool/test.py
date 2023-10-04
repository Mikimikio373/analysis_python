import yaml

with open('sensor_pos.yml') as f:
    y = yaml.safe_load(f)

print(y[0]['module'])