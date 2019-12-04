# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 21:16:30 2018

@author: david
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def NS(s,o):
    """
    Nash Sutcliffe efficiency coefficient
    input:
        s: simulated
        o: observed
    output:
        ns: Nash Sutcliffe efficient coefficient
    """
    return 1 - sum((s-o)**2)/sum((o-np.mean(o))**2)

def print_rch(array):
    
    nrow = array.shape[0]
      
    data = array[:,0]
    sim = array[:,1]
    #obs = array[:,1]
    #ns = NS(sim, obs)

    fig = plt.figure(figsize = (20,10))
  
    plt.plot(data, sim, label='Simulated', linewidth = 1, color = 'navy')
    #plt.plot(data, obs, label = 'Observed', linewidth = 2.8, color = 'coral')
    plt.title('Simulated and observed flows - CX station', fontsize=24)
    plt.xlim(0, nrow)
    plt.xlabel('Simulation days', fontsize=20)
    plt.ylabel('Flow(cms)', fontsize=18)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.tick_params(axis='both', which='minor', labelsize=20)
    #plt.annotate('NS = %.2f'%ns,
            #xy=(0.88, 0.7), xycoords='figure fraction',
            #xytext=(0,50), textcoords='offset points', fontsize=24)
    plt.legend(fontsize=18)
    plt.grid()
    plt.tight_layout()
    plt.show()
    
    #plt.savefig(r'D:\OneDrive\Dissertacao\7.Writing\1.Figuras\%s'%n+".svg",dpi = 300)
    
def read_rch(fileadress, filetype, list_lkp, rch):
    
    from_file = open(fileadress, 'r')
    
    lines = from_file.readlines()
    result_list=lines[9:]
    header = lines[8].split()
    result_list_parse1 = []
    for i in result_list:
        a = i.split()[1:]
        result_list_parse1.append(a)
    
    result_array = np.array(result_list_parse1,dtype = float)
    days_g_address = header.index("MON")
    rch_address = header.index("RCH")
          
    result_array_filtered=result_array[result_array[:,rch_address] == rch]
    
    days_g = result_array_filtered[:,days_g_address]
    days_sim = np.array(np.arange(1,days_g.shape[0]+1),dtype = float)
    
    result_array_filtered = np.insert(result_array_filtered,2,days_sim,axis = 1)
    header.insert(2,"SDG")
    
    coln_final_array = len(list_lkp)
    a = np.zeros((result_array_filtered.shape[0], int(coln_final_array)))
    a = np.insert(a,0,result_array_filtered[:,2], axis = 1)
    
    col_index_list = []
    
    for i in list_lkp:
        col_interest = [header.index("FLOW_OUTcms")]#multiplos - depois    count = 1
        col_index_list.append(col_interest)
        
    count = 1
    for i in col_interest:
        analysis_array = result_array_filtered[:,i]
        a[:,count] = analysis_array
        count = count+1
    return a 

def read_hru(fileadress, filetype, list_lkp, rch):
        
fileadress = r'D:\OneDrive\output.rch'
a = read_rch(fileadress, filetype = 'rch', list_lkp=["FLOW_OUTcms"], rch = 39)
print_rch(a)   