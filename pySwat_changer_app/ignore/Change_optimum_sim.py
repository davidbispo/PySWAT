# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 13:49:37 2018

@author: David Bispo
"""
import change_par as cp 
import get_par as gp
import get_output as go
import os
import subprocess
from subprocess import Popen, PIPE
import numpy as np

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

TXTInOut = r'D:\TxtInOut'     
instance_cp = cp.par_handler(TXTInOut)
fileadress = os.path.join(TXTInOut,'output.rch')
variables = ["FLOW_OUTcms"]
observed = r'D:\OneDrive\Planilha-mestra_geral_v2_test.csv'
rel_table = {"tmd":39, "stq":98, "cax":155}

instance_cp.change(parameter = 'CN2', method = 'relative', value = -0.083233, sb= list(range(1,40)))#1
instance_cp.change(parameter = 'GWQMN', method = 'replace', value = 3321.755, sb= list(range(1,40)))#2
instance_cp.change(parameter = 'RCHRG_DP', method = 'replace', value = 0.8061, sb= list(range(1,40)))#3
instance_cp.change(parameter = 'HRU_SLP', method = 'relative', value = -0.147, sb= list(range(1,40)))#4
instance_cp.change(parameter = 'OV_N', method = 'relative', value = -0.3484, sb= list(range(1,40)))#5#
instance_cp.change(parameter = 'LAT_TTIME', method = 'replace', value = 18.199, sb= list(range(1,40)))#6
instance_cp.change(parameter = 'CH_K1', method = 'replace', value = 312.289, sb= list(range(1,40)))#7
instance_cp.change(parameter = 'ALPHA_BNK', method = 'replace', value = 0.3555, sb= list(range(1,40)))#8
instance_cp.change(parameter = 'CH_K2', method = 'replace', value = 300.123, sb= list(range(1,40)))#9
instance_cp.change(parameter = 'SOL_K', method = 'relative', value = 0.0800, sb= list(range(1,40)))#10

instance_cp.change(parameter = 'GWQMN', method = 'replace', value = 7933.317, sb= list(range(40,99)))#11
instance_cp.change(parameter = 'RCHRG_DP', method = 'replace', value = 0.902, sb= list(range(40,99)))#12
instance_cp.change(parameter = 'LAT_TTIME', method = 'replace', value = 0.673, sb= list(range(40,99)))#13
instance_cp.change(parameter = 'CH_K1', method = 'replace', value = -39.276, sb= list(range(40,99)))#14
instance_cp.change(parameter = 'CH_N2', method = 'relative', value = 0.3135, sb= list(range(40,99)))#14
instance_cp.change(parameter = 'ALPHA_BNK', method = 'replace', value = 0.663, sb= list(range(40,99)))#15
instance_cp.change(parameter = 'SOL_AWC', method = 'relative', value = 0.139, sb= list(range(40,99)))#16
instance_cp.change(parameter = 'SOL_K', method = 'relative', value = -0.012, sb= list(range(40,99)))#17
instance_cp.change(parameter = 'ESCO', method = 'relative', value = 1.055, sb= list(range(40,99)))#18

instance_cp.change(parameter = 'GW_DELAY', method = 'replace', value = 13.655, sb= list(range(100,155)))#19
instance_cp.change(parameter = 'GWQMN', method = 'replace', value = 1432.171, sb= list(range(100,155)))#20
instance_cp.change(parameter = 'RCHRG_DP', method = 'replace', value = 0.065, sb= list(range(100,155)))#21
instance_cp.change(parameter = 'SLSOIL', method = 'replace', value = 3.453, sb= list(range(100,155)))#22
instance_cp.change(parameter = 'CH_N2', method = 'relative', value = 0.0438, sb= list(range(100,155)))#232
instance_cp.change(parameter = 'ALPHA_BNK', method = 'replace', value = 1.082, sb= list(range(100,155)))#24
instance_cp.change(parameter = 'CH_K2', method = 'replace', value = 210.034, sb= list(range(100,155)))#25
instance_cp.change(parameter = 'SOL_K', method = 'relative', value = 0.662, sb= list(range(100,155)))#26

os.chdir(r'D:\TxtInOut')       
print("Running Swat..")
for path in execute(["swat.exe"]):
    print(path, end="")

instance_go = go.output_rch(fileadress,[98,155],variables,observed_input = observed, rel_table = rel_table)
#getting all reaches data
array = instance_go.read_rch()

print('Writing to simulations log file...')

output_sims = r'D:\sim_result.txt'
if os.path.isfile(output_sims) == False:
    np.savetxt(output_sims,array, fmt='%s')
else:
    temp = np.loadtxt(output_sims, dtype = str)
    array_to_stack = array[:,2:3]
    temp = np.concatenate((temp,array_to_stack), axis=1)
    np.savetxt(output_sims,temp,fmt='%s')