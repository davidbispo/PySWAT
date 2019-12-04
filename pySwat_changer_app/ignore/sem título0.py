# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 11:26:51 2019

@author: David
"""

import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import os
import matplotlib.dates as mdates
#hru files

folder = r'E:\Users\David\Desktop\swat_results\InfBasins_hru\95_1352'
files = os.listdir(folder)

arrays=[]

for f in files:
    my_address = os.path.join(folder, f)
    my_data = np.genfromtxt(my_address, delimiter=',', dtype=str)
    arrays.append([f,my_data])
    
dates = np.array([arrays[0][1][:,0][1:].tolist()]).T
seriesdic = {}

#stacking shit with the same reduction vales
for k in range(2,6,1):
    for i in arrays:            
        reduction_column = i[1][:,k].tolist()
#        find_underline = i[0].index('_')
        header_column = i[0] + " - " + reduction_column[0]
        dicname=reduction_column[0]
        reduction_column = reduction_column[1:]
        
        if i==arrays[0]:
            calibrated_array = np.array([i[1][1:,1].tolist()]).T
            calibrated_header = np.array([[i[0] + "- calibrated"]])
            calibrated_array = np.vstack((calibrated_header,calibrated_array))
            
            header_array = np.array([header_column]).T
            temp_array=np.array([reduction_column]).T
            temp_array=np.vstack((header_array, temp_array))
            final_array = temp_array
        else:
            calibrated_array_temp = np.array([i[1][1:,1].tolist()]).T
            calibrated_header_temp = np.array([[i[0] + "- calibrated"]])
            calibrated_array_temp = np.vstack((calibrated_header_temp,calibrated_array_temp))
            calibrated_array = np.hstack((calibrated_array,calibrated_array_temp))
            
            header_array = np.array([header_column]).T
            temp_array= np.array([reduction_column]).T
            temp_array=np.vstack((header_array, temp_array))
            final_array = np.hstack((final_array,temp_array))
        
    seriesdic[dicname] = final_array
seriesdic['calibrated'] = calibrated_array
seriesdic['Dates'] = dates
        
#ploting that
seriesdic_to_look = list(seriesdic.keys())
b=seriesdic_to_look.index('Dates')
del seriesdic_to_look[b]
colors = ['#913CCD', '#F15F74', '#F7CD3C', '#2CA8C2', '#98CB4A', '#839098', '#5481E6']

for o in seriesdic_to_look: 
    fig, ax1 = plt.subplots(figsize=(17,10))
    ax2 = ax1.twinx()
    fig.autofmt_xdate()
    header_array = seriesdic[o][0,:].tolist()
    header_array = np.array([header_array]).T
    entering_array = seriesdic[o][1:]
    entering_array = np.hstack((dates,entering_array))
    data_header_array=np.array([['data']])
    header_to_pandas = np.vstack((data_header_array,header_array)).tolist()
    header_to_pandas_list = []
    for s in header_to_pandas:
        header_to_pandas_list.append(s[0])
    
    df = pd.DataFrame(entering_array, columns = header_to_pandas_list)
    df.set_index(pd.DatetimeIndex(df['data']),inplace=True)
    df = df.drop('data',axis=1).convert_objects(convert_numeric=True)
    
    startdate ='2008-2-1'
    enddate='2008-2-28'
    df_to_plot = df.loc[startdate:enddate]
    dates_list_temp = df_to_plot.index.tolist()
    dates_array = np.array(dates_list_temp)
      
    counter=0
    for u in df_to_plot:
        
        if 'dailycn' in u:
            data_to_plot = np.array(df_to_plot[u].tolist())
            ax2.plot(dates_list_temp, data_to_plot, label=u, color = 'red')            
        else:
            data_to_plot = np.array(df_to_plot[u].tolist())
            ax1.plot(dates_array, data_to_plot, label=u, color=colors[counter])
            counter+=1
        
    array_cal = seriesdic['calibrated']
    header_cal_array = array_cal[0,:].tolist()
    header_array = np.array([header_cal_array]).T
    entering_cal_array = np.hstack((dates,array_cal[1:,:]))
    data_header_array=np.array([['data']])
    header_to_pandas = np.vstack((data_header_array,header_array)).tolist()
    header_to_pandas_list = []
    for m in header_to_pandas:
        header_to_pandas_list.append(m[0])
        
    df_cal = pd.DataFrame(entering_cal_array, columns = header_to_pandas_list)
    df_cal.set_index(pd.DatetimeIndex(df_cal['data']),inplace=True)
    df_cal = df_cal.drop('data',axis=1).convert_objects(convert_numeric=True)
    df_cal_to_plot = df_cal.loc[startdate:enddate]
    
    counter=0
    
    for l in df_cal_to_plot:
        if l == 'dailycn' in l:
            data_to_plot = np.array(df_cal_to_plot[l].tolist())
            ax2.plot(dates_list_temp, data_to_plot, label=l, linestyle= '--', color='red')
        else:
    
            data_to_plot = np.array(df_cal_to_plot[l].tolist())
            ax1.plot(dates_list_temp, data_to_plot, label=l, linestyle= '--', color=colors[counter])
            counter+=1
        
    ax1.set_xticks(dates_list_temp) 
    xfmt = mdates.DateFormatter('%d-%m-%y')
    ax1.xaxis.set_major_formatter(xfmt)
    ax1.set_ylim(-0.5,90)
    ax1.set_ylim(-0.5,5)
    ax1.set_xlim(startdate,enddate)
    ax1.grid()
    ax1.legend(ncol=4)
    plt.show()













