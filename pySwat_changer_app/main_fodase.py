# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:21:20 2018

@author: David Bispo
"""
import change_par as cp 
import get_par as gp
import get_output as go
import os 
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
from subprocess import Popen, PIPE
#import lhsmdu


######################## Extra functions#####################################
#Execute commmand for swat and continuous output
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

#Spinning cursor widget
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

spinner = spinning_cursor()
for _ in range(50):
    sys.stdout.write(next(spinner))
    sys.stdout.flush()
    time.sleep(0.1)
    sys.stdout.write('\b')
    
#Latin hypercube sampler function
#def latinh_pars(maximum, minimum):
    
    #k = lhsmdu.sample(2, 20)
    
    #return k 
######################## Code for printing simulations #####################################
def printsims(array_output, fig_output, variables, observed_input,rel_table):
    
    array = np.loadtxt(array_output, dtype = str)
    instance_go_simarray = go.output_simarray(array)
    instance_go_simarray.print_allinone(figoutput = r'D:\simoutput.png', figsize = (16,8))
    
######################## Sparse unused code#####################################

#TXTInOut = r'D:\TxtInOut'  
#instance_gp = gp.swat_partable(TXTInOut = TXTInOut, sb = list(range(1,39)), lulc='all')
#table, original_table = instance_gp.get_par_hru()

######################## Sparse unused code#####################################
def runsims(nsims,TXTInOut, output,  variables, observed,rel_table = None):
    
#Starting instance of change_par.py
    instance_cp = cp.par_handler(TXTInOut)
    print('Starting...')

#Counter for number of simulations
    for i in range(nsims):
        print("###  Run # {0} \n".format(i+1))
              
        values_list = np.linspace(-0.8,0.8,9) # CHOOSE HERE WHAT VALUE LIST YOU WANT FOR YOUR PARAMETER

#Changer for parameter
        #instance_cp.change(parameter = 'CN2', method = 'relative', value = values_list[i], sb='all',log = 'D:\log.txt')

#Runs SWAT
        os.chdir(r'D:\TxtInOut')       
        print("Running Swat..")
        for path in execute(["swat.exe"]):
            print(path, end="")
        
        print('Run Succesful!...Fetching Data...')
        
#Starting get output instance
        instance_go = go.output_rch(fileadress,[98,155],variables,observed_input = observed, rel_table = rel_table)
#getting all reaches data
        array = instance_go.read_rch()
#print all the fetched outputs in one file
        instance_go.print_allinone(array,figsize=(20,10))
        
#Writes simulation to log file column
        print('Writing to simulations log file...')
        
        if os.path.isfile(output) == False:
            np.savetxt(output,array, fmt='%s')
        else:
            temp = np.loadtxt(output, dtype = str)
            array_to_stack = array[:,2:3]
            temp = np.concatenate((temp,array_to_stack), axis=1)
            np.savetxt(output,temp,fmt='%s')
#Finished message
        print('Done!')
   
######################## Input Data#####################################
output_rch = r'D:\TxtInOut\output.rch'
TXTInOut = r'D:\TxtInOut'      
fileadress = r'D:\TxtInOut\output.rch'
observed = r'D:\OneDrive\Planilha-mestra_geral_v2_test.csv'
rel_table = {"tmd":39, "stq":98, "cax":155}
nsims = 1
output_simlog = r'D:\sim_result.txt'

######################## Function Calling #####################################

#Calls the multiple simulation algorithim
runsims(nsims,TXTInOut,output_simlog,["FLOW_OUTcms"],observed,rel_table)

#Calls the reading for a multiple simulation output file
#instance_output_simarray = go.output_simarray(output_simlog)
#instance_output_simarray.print_allinone(r'D:\results.png', figsize = (20,10),observed = None, rel_table = None)





