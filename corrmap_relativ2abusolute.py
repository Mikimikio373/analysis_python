
path_i = "R:\\minami\\netscandata\\20220704_minamicham\\for_hts1-2_compare\\4BestAli_Pl003_HTS1-2\\align\\corrmap-align-002-003.lst"

f_input = open(path_i, 'r')

data = f_input.readlines()
f_input.close()

path_o = "R:\\minami\\netscandata\\20220704_minamicham\\for_hts1-2_compare\\4BestAli_Pl003_HTS1-2\\align\\corrmap-align-002-003_aff.lst"
f_output = open(path_o, 'w')
for i in range(0, len(data)):
    if data[i][9] != '2':
        print('error')
    else:
        line = data[i][:8] + '3' + data[i][10:]
        f_output.write(line)

