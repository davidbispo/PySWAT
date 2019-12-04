# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 11:21:02 2018

@author: david
"""
import numpy as np 
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

def batch_printer(filepath,n):
    
    from_file = open(cx, 'r')
    lines = from_file.readlines()
    lines = lines[1:]
    parsed = []
    for line in lines:
        parsed.append(line.split(','))

    array = np.array(parsed, dtype = float)
    array_nrow = array.shape[0]
      
    data = array[:,0]
    sim = array[:,2]
    obs = array[:,1]
    ns = NS(sim, obs)

    fig = plt.figure(figsize = (20,10))
    fig, ax = plt.subplots()
   
    plt.plot(data, sim, label='Simulated', linewidth = 2.8, color = 'navy')
    plt.plot(data, obs, label = 'Observed', linewidth = 2.8, color = 'coral')
    plt.title('Simulated and observed flows - CX station', fontsize=24)
    plt.xlim(data[1300], data[array_nrow/2])
    plt.xlabel('Simulation days', fontsize=20)
    plt.ylabel('Flow(cms)', fontsize=18)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.tick_params(axis='both', which='minor', labelsize=20)
    plt.annotate('NS = %.2f'%ns,
            xy=(0.88, 0.7), xycoords='figure fraction',
            xytext=(0,50), textcoords='offset points', fontsize=24)
    plt.legend(fontsize=18)
    plt.grid()
    plt.tight_layout()
    plt.show()
    
    plt.savefig(r'D:\OneDrive\Dissertacao\7.Writing\1.Figuras\%s'%n+".svg",dpi = 300)

def cupprint(filepaths):
    n = len(filepaths)
    for filepath in filepaths:
        batch_printer(filepath, n)
    
tm = r'D:\OneDrive\Dissertacao\7.Writing\4.Spreadsheets\tm_sim_obs.csv'
sq = r'D:\OneDrive\Dissertacao\7.Writing\4.Spreadsheets\sq_sim_obs.csv'
cx = r'D:\OneDrive\Dissertacao\7.Writing\4.Spreadsheets\cx_sim_obs.csv'

filepaths = [tm,sq,cx]
cupprint(filepaths)



