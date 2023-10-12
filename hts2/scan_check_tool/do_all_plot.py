import os
import sys
import subprocess

if not len(sys.argv) == 2:
    sys.exit('please enter \"target path\"')

basepath = sys.argv[1]
outpath = os.path.join(basepath, 'GRAPH')
os.makedirs(outpath, exist_ok=True)

# sensor_exposureをたたいているコマンドから、scan_chech_toolの場所を特定
pythonpath = os.path.split(sys.argv[0])[0]

command_nog_s = 'python {}/sensor_nog.py {}'.format(pythonpath, basepath)
subprocess.run(command_nog_s, shell=True)

command_nog_p = 'python {}/plot_nog.py {}'.format(pythonpath, basepath)
subprocess.run(command_nog_p, shell=True)

command_ex_s = 'python {}/sensor_exposure.py {}'.format(pythonpath, basepath)
subprocess.run(command_ex_s, shell=True)

command_ex_p = 'python {}/plot_exposure.py {}'.format(pythonpath, basepath)
subprocess.run(command_ex_p, shell=True)

command_not_s = 'python {}/sensor_not.py {}'.format(pythonpath, basepath)
subprocess.run(command_not_s, shell=True)

command_not_p = 'python {}/plot_not.py {}'.format(pythonpath, basepath)
subprocess.run(command_not_p, shell=True)

command_topbottom_s = 'python {}/sensor_topbottom.py {}'.format(pythonpath, basepath)
subprocess.run(command_topbottom_s, shell=True)

command_topbottom_p = 'python {}/plot_topbottom.py {}'.format(pythonpath, basepath)
subprocess.run(command_topbottom_p, shell=True)

command_thickness_p = 'python {}/plot_thickness.py {}'.format(pythonpath, basepath)
subprocess.run(command_thickness_p, shell=True)
