# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 22:53:45 2018

@author: David Bispo
"""
import pySWATParApp as Ppar
import get_par as gp
import get_output as go
import os
import subprocess
from subprocess import Popen, PIPE
import numpy as np

def execute(cmd):# Runs SWAT into the current terminal
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                             universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

#TXTInOut = r'C:\Barigui_Biorretention\Scenarios\Calibrated\TxtInOut'
TXTInOut = r'C:\Barigui_Biorretention\Scenarios\Altered\TxtInOut'
instance_Ppar = Ppar.par_handler(TXTInOut)
fileadress = os.path.join(TXTInOut,'output.rch')
variables = ["FLOW_OUTcms"]
observed = r'E:\OneDrive\master_spreadsheet.csv'
rel_table = {"tmd":39, "stq":98, "cax":155}

###COMANDS FOR SIMULATION CALIBRATION
instance_Ppar.change(parameter = 'GWQMN', method = 'replace', value = 1850.233, 
                   sb= list(range(1,40)))#2
instance_Ppar.change(parameter = 'RCHRG_DP', method = 'replace', value =0.9503, 
                   sb= list(range(1,40)))#3
instance_Ppar.change(parameter = 'HRU_SLP', method = 'relative', value =-0.206, 
                   sb= list(range(1,40)))#4
instance_Ppar.change(parameter = 'SLSOIL', method = 'replace', value = -4.483,
                   sb= list(range(1,40)))#4
instance_Ppar.change(parameter = 'OV_N', method = 'relative', value = 0.000780,
                   sb= list(range(1,40)))#5#
instance_Ppar.change(parameter = 'LAT_TTIME', method = 'replace', value =16.915,
                   sb= list(range(1,40)))#6
instance_Ppar.change(parameter = 'CH_N1', method = 'relative', value =-0.0138 ,
                   sb= list(range(100,155)))#14
instance_Ppar.change(parameter = 'CH_K1', method = 'replace', value = 466.174, 
                   sb= list(range(1,40)))#7
instance_Ppar.change(parameter = 'ALPHA_BNK', method = 'replace', value =0.211, 
                   sb= list(range(1,40)))#8
instance_Ppar.change(parameter = 'CH_K2', method = 'replace', value = 373.52, 
                   sb= list(range(1,40)))#9
instance_Ppar.change(parameter = 'SOL_AWC', method = 'relative', value = 0.378,
                   sb= list(range(1,40)))#10
instance_Ppar.change(parameter = 'SOL_K', method = 'relative', value = -0.827, 
                   sb= list(range(1,40)))#10


instance_Ppar.change(parameter = 'CN2', method = 'relative', value = -0.164, 
                   sb= list(range(40,99)))#1
instance_Ppar.change(parameter = 'RCHRG_DP', method = 'replace',value=0.277443,
                   sb= list(range(40,99)))#12
instance_Ppar.change(parameter = 'LAT_TTIME', method = 'replace', value= 4.365,
                   sb= list(range(40,99)))#13
instance_Ppar.change(parameter = 'CH_K1', method = 'replace', value = -45.366,
                   sb= list(range(40,99)))#14
instance_Ppar.change(parameter = 'CH_N2', method = 'relative', value =  -0.332,
                   sb= list(range(40,99)))#14
instance_Ppar.change(parameter = 'ALPHA_BNK', method = 'replace', value= 0.794,
                   sb= list(range(40,99)))#15
instance_Ppar.change(parameter = 'CH_K2', method = 'replace', value = 216.269, 
                   sb= list(range(40,99)))#25
instance_Ppar.change(parameter = 'SOL_AWC', method = 'relative', value = 0.564,
                   sb= list(range(40,99)))#16


instance_Ppar.change(parameter = 'CN2', method = 'relative', value = 0.0364,
                   sb= list(range(100,155)))#1
instance_Ppar.change(parameter = 'ALPHA_BF', method = 'replace', value = 1.013, 
                   sb= list(range(100,155)))#1
instance_Ppar.change(parameter = 'GWQMN', method = 'replace', value = 4178.194,
                   sb= list(range(100,155)))#20
instance_Ppar.change(parameter = 'RCHRG_DP', method = 'replace', value = 0.943, 
                   sb= list(range(100,155)))#21
instance_Ppar.change(parameter = 'HRU_SLP', method = 'relative', value =-0.188, 
                   sb= list(range(100,155)))#4
instance_Ppar.change(parameter = 'LAT_TTIME', method = 'replace', value =14.481, 
                   sb= list(range(100,155)))#13
instance_cp.change(parameter = 'CH_N1', method = 'relative', value =  0.134, 
                   sb= list(range(100,155)))#14
instance_cp.change(parameter = 'CH_N2', method = 'relative', value = -0.0346, 
                   sb= list(range(100,155)))#232
instance_cp.change(parameter = 'ALPHA_BNK', method = 'replace', value = 0.654, 
                   sb= list(range(100,155)))#24
instance_cp.change(parameter = 'CH_K2', method = 'replace', value = 175.229, 
                   sb= list(range(100,155)))#25

os.chdir(r'E:\Barigui_InfBasins\TxtInOut')       ###RUN SWAT CALL
print("Running Swat..")
for path in execute(["swat.exe"]):
    print(path), end="")

instance_go = go.output_rch(fileadress,[39,98,155],variables,#Reads SWAT OUTPUT
                            observed_input = observed, rel_table = rel_table)

#getting all reaches data
array = instance_go.read_rch()

print('Writing to simulations log file...')#WRITES SIMULATIONS TO LOG FILE

output_sims = r'E:\sim_result_InfBasins.txt'
if os.path.isfile(output_sims) == False:
    np.savetxt(output_sims,array, fmt='%s')
else:
    temp = np.loadtxt(output_sims, dtype = str)
    array_to_stack = array[:,2:3]
    temp = np.concatenate((temp,array_to_stack), axis=1)
    np.savetxt(output_sims,temp,fmt='%s')
"""
#CHANGES CN VALUES FOR CERTAIN LAND USES - NOT ACTIVE IN THIS CODE

print('changing parameters on Biorretention...')
instance_Ppar.change(parameter = 'CN2', method = 'relative', value = -0.5, sb= 'all', lulc ='BRRD')
instance_Ppar.change(parameter = 'CN2', method = 'relative', value = -0.5, sb= 'all', lulc ='IBID')


"""
print('Programa terminado!!!!!')
"""