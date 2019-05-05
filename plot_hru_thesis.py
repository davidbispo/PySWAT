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
from pylab import *
#hru files


def plothru(folder, dic, outname):
    files = os.listdir(folder)
    
    arrays=[]
    
    dictitle={
            'calibrated': 'Baseline Scenario',
            'altered_10': '10% Reduction scenario',
            'altered_30': '30% Reduction scenario',
            'altered_50': '50% Reduction scenario',
            'altered_70': '70% Reduction scenario',
            }
    

    #/*------------------------------ Fix Here -------------------------------------------/*
    dic_seriesname = dic
    
    #/*------------------------------ Fix Here -------------------------------------------/*
    
    for f in files:
        my_address = os.path.join(folder, f)
        my_data = np.genfromtxt(my_address, delimiter=',', dtype=str, encoding="utf8")
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
    colors = ['#913CCD', '#F15F74', '#F7CD3C', '#2CA8C2', '#98CB4A', '#839098', '#5481E6', '#45601c' ]
    
    for o in seriesdic_to_look: 
        fig = plt.figure(figsize=(17,12))
        ax1 = plt.subplot(411)
        ax2 = plt.subplot(412)
        ax3 = plt.subplot(413)
        ax4 = plt.subplot(414)
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
        print(df_to_plot.dtypes.index)
        for u in df_to_plot:
            
            if 'dailycn' in u :
                data_to_plot = np.array(df_to_plot[u].tolist())
                ax1.plot(dates_list_temp, data_to_plot, label=dic_seriesname[u], color = 'red', zorder=1)    
                ax1.set_zorder(1)
                ax1.patch.set_visible(False)
            
            elif 'prec' in u:
                axp = ax1.twinx()
                data_to_plot = np.array(df_to_plot[u].tolist())
                axp.bar(dates_list_temp, data_to_plot, label=dic_seriesname[u], color = '#4b9ad5', edgecolor='#67a9db', lw=2)    
                axp.set_zorder(0)
                
            elif 'sw_' in u: 
                data_to_plot = np.array(df_to_plot[u].tolist())
                ax2.plot(dates_array, data_to_plot, label=dic_seriesname[u], color=colors[counter])
                counter+=1
                
            elif 'perc' in u:
                axs = ax2.twinx()
                data_to_plot = np.array(df_to_plot[u].tolist())
                axs.plot(dates_array, data_to_plot, label=dic_seriesname[u], color=colors[counter])
                counter+=1
            elif 'da_st' in u:
                data_to_plot = np.array(df_to_plot[u].tolist())
                ax3.plot(dates_array, data_to_plot, label=dic_seriesname[u], color=colors[counter])
                ax3.set_zorder(1)
                ax3.patch.set_visible(False)
                counter+=1
            elif 'sa_st' in u:
                axq = ax3.twinx()
                data_to_plot = np.array(df_to_plot[u].tolist())
                axq.plot(dates_list_temp, data_to_plot, label=dic_seriesname[u], color = colors[counter])    
                counter+=1
            else:
                data_to_plot = np.array(df_to_plot[u].tolist())
                ax4.plot(dates_array, data_to_plot, label=dic_seriesname[u], color=colors[counter])
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
            if 'dailycn' in l and o != 'calibrated':# insert baseline except for baseline
                data_to_plot = np.array(df_cal_to_plot[l].tolist())
                ax1.plot(dates_list_temp, data_to_plot, label=dic_seriesname[l], linestyle= '--', color='red')           
            elif 'sw_' in l and o != 'calibrated':
                data_to_plot = np.array(df_cal_to_plot[l].tolist())
                ax2.plot(dates_list_temp, data_to_plot, label=dic_seriesname[l], linestyle= '--', color=colors[counter], lw=3)
                counter+=1
            elif 'perc' in l and o != 'calibrated':
                data_to_plot = np.array(df_cal_to_plot[l].tolist())
                axs.plot(dates_list_temp, data_to_plot, label=dic_seriesname[l], linestyle= '--', color=colors[counter], lw=3)
                counter+=1
            
            elif 'da_st' in l and o != 'calibrated':
                data_to_plot = np.array(df_cal_to_plot[l].tolist())
                ax3.plot(dates_array, data_to_plot, label=dic_seriesname[l], color=colors[counter],linestyle= '--',lw=3)
                counter+=1
            elif 'sa_st' in l and o != 'calibrated':
                data_to_plot = np.array(df_cal_to_plot[l].tolist())
                axq.plot(dates_array, data_to_plot, label=dic_seriesname[l], color=colors[counter],linestyle= '--',lw=3)
                counter+=1           
            else:
                if o != 'calibrated' and 'prec' not in l:
                    data_to_plot = np.array(df_cal_to_plot[l].tolist())
                    ax4.plot(dates_list_temp, data_to_plot, label=dic_seriesname[l], linestyle= '--', color=colors[counter], lw=3)    
                    counter+=1
        
        ax1.set_xticks(dates_list_temp) 
        xfmt = mdates.DateFormatter('%d-%m-%y')
        ax1.xaxis.set_major_formatter(xfmt)
        ax1.set_title(dictitle[o], fontsize = 20)
        
        ax1.set_xlim(startdate,enddate)
        ax1.grid()

        ax1.xaxis.set_major_formatter(xfmt)
        ax1.set_xticks(dates_list_temp) 
        ax1.set_ylabel('Curve number', size=14)
        ax1.tick_params(axis = 'both', which = 'major', labelsize = 14)
        ax1.legend(loc='upper left', ncol=1, fontsize = 12, bbox_to_anchor=(0.0,0.64))
                
        axp.set_ylabel('Precipitation (mm)', size=14)#duplicate of cn axe - precipitation
        axp.legend(loc='upper right', fontsize = 12, bbox_to_anchor=(0.17,0.85))
        axp.tick_params(axis = 'both', which = 'major', labelsize = 14)
        
        ax2.set_xticks(dates_list_temp)
        ax2.set_xlim(startdate,enddate)
        ax2.grid()
        ax2.legend(loc='upper left', ncol=1, fontsize = 12, bbox_to_anchor=(0.02,0.975))
        ax2.xaxis.set_major_formatter(xfmt)
        ax2.set_ylabel('Soil Water (mm)', size=14)
        ax2.tick_params(axis = 'both', which = 'major', labelsize = 14)
        
        axs.set_ylabel('Percolated Water (mm)', size=14)#duplicate of sw axe - perc
        axs.legend(loc='best', fontsize = 12, bbox_to_anchor=(0.24,0.7)) 
        axs.tick_params(axis = 'both', which = 'major', labelsize = 14)
        
        ax3.set_xticks(dates_list_temp)
        ax3.set_xlim(startdate,enddate)
        ax3.grid()
        ax3.legend(loc='lower right', ncol=1, fontsize = 12, bbox_to_anchor=(1.0,0.12))    
        ax3.xaxis.set_major_formatter(xfmt)
        ax3.set_ylabel('Deep Aq. Storage (mm)', size=14)
        ax3.tick_params(axis = 'both', which = 'major', labelsize = 14)
        
        axq.tick_params(axis = 'x', which = 'major', labelsize = 0)
        axq.tick_params(axis = 'y', which = 'major', labelsize = 14)
        axq.legend(loc='best', fontsize = 12,ncol=1, bbox_to_anchor=(0.35,0.45))
        axq.set_ylabel('Shallow Aq. Storage (mm)', size=14)

        ax4.set_xticks(dates_list_temp)
        ax4.set_xlim(startdate,enddate)
        ax4.grid()
        ax4.legend(loc='upper left', ncol=2, fontsize = 12)
        ax4.xaxis.set_major_formatter(xfmt)
        ax4.set_ylabel('Other Variables (mm)', size=14)
        ax4.tick_params(axis = 'both', which = 'major', labelsize = 14)
    
        plt.subplots_adjust(top= 2)
        plt.tight_layout()
        plt.savefig(outname+"%s"%dictitle[o]+".jpg")
        plt.show()
        print(r"/*----------------------------/*")

dic_seriesname_infbasins95= {
       'dailycn_hru95_InfBasins.csv - altered_10': 'Daily CN - Inf. Basins - Altered',
       'gwq_hru95_InfBasins.csv - altered_10'  : 'GWQ - Inf. Basins - Altered',
       'latq_hru95_InfBasins.csv - altered_10' : 'LATQ - Inf. Basins - Altered',
       'percolated_InfBasins.csv - altered_10' : 'PERC - Inf. Basins - Altered',
       'surq_hru95_InfBasins.csv - altered_10' : 'SURQ - Inf. Basins - Altered',
       'sw_hru95_InfBasins.csv - altered_10'   : 'SW - Inf. Basins - Altered',
       'wyld_hru95_InfBasins.csv - altered_10' : 'WYLD - Inf. Basins - Altered',
       'da_st_hru95_InfBasins.csv - altered_10' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_InfBasins.csv - altered_10' : 'SA_ST - Swales - Altered',
        'prec_hru95_InfBasins.csv - altered_10' : 'Precipitation',


       'dailycn_hru95_InfBasins.csv - altered_30': 'Daily CN - Inf. Basins - Altered',
       'gwq_hru95_InfBasins.csv - altered_30'  : 'GWQ - Inf. Basins - Altered',
       'latq_hru95_InfBasins.csv - altered_30' : 'LATQ - Inf. Basins - Altered',
       'percolated_InfBasins.csv - altered_30' : 'PERC - Inf. Basins - Altered',
       'surq_hru95_InfBasins.csv - altered_30' : 'SURQ - Inf. Basins - Altered',
       'sw_hru95_InfBasins.csv - altered_30'   : 'SW - Inf. Basins - Altered',
       'wyld_hru95_InfBasins.csv - altered_30' : 'WYLD - Inf. Basins - Altered',
       'da_st_hru95_InfBasins.csv - altered_30' : 'DA_ST - Inf. Basins - Altered',
       'sa_st_hru95_InfBasins.csv - altered_30' : 'SA_ST - Inf. Basins - Altered',
        'prec_hru95_InfBasins.csv - altered_30' : 'Precipitation',

       'dailycn_hru95_InfBasins.csv - altered_50': 'Daily CN - Inf. Basins - Altered',
       'gwq_hru95_InfBasins.csv - altered_50'  : 'GWQ - Inf. Basins - Altered',
       'latq_hru95_InfBasins.csv - altered_50' : 'LATQ - Inf. Basins - Altered',
       'percolated_InfBasins.csv - altered_50' : 'PERC - Inf. Basins - Altered',
       'surq_hru95_InfBasins.csv - altered_50' : 'SURQ - Inf. Basins - Altered',
       'sw_hru95_InfBasins.csv - altered_50' :  'SW - Inf. Basins - Altered',
       'wyld_hru95_InfBasins.csv - altered_50' :  'WYLD - Inf. Basins - Altered',
       'da_st_hru95_InfBasins.csv - altered_50' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_InfBasins.csv - altered_50' : 'SA_ST - Swales - Altered',
        'prec_hru95_InfBasins.csv - altered_50' : 'Precipitation',

       'dailycn_hru95_InfBasins.csv - altered_70': 'Daily CN - Inf. Basins - Altered',
       'gwq_hru95_InfBasins.csv - altered_70'  : 'GWQ - Inf. Basins - Altered',
       'latq_hru95_InfBasins.csv - altered_70' : 'LATQ - Inf. Basins - Altered',
       'percolated_InfBasins.csv - altered_70' : 'PERC - Inf. Basins - Altered',
       'surq_hru95_InfBasins.csv - altered_70' : 'SURQ - Inf. Basins - Altered',
       'sw_hru95_InfBasins.csv - altered_70' :   'SW - Inf. Basins - Altered',
       'wyld_hru95_InfBasins.csv - altered_70' : 'WYLD - Inf. Basins - Altered',
       'da_st_hru95_InfBasins.csv - altered_70' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_InfBasins.csv - altered_70' : 'SA_ST - Swales - Altered',
        'prec_hru95_InfBasins.csv - altered_70' : 'Precipitation',

       'dailycn_hru95_InfBasins.csv- calibrated': 'Daily CN - Inf. Basins - Baseline',
       'gwq_hru95_InfBasins.csv- calibrated'  : 'GWQ - Inf. Basins - Baseline',
       'latq_hru95_InfBasins.csv- calibrated' : 'LATQ - Inf. Basins - Baseline',
       'percolated_InfBasins.csv- calibrated' : 'PERC - Inf. Basins - Baseline',
       'surq_hru95_InfBasins.csv- calibrated' : 'SURQ - Inf. Basins - Baseline',
       'sw_hru95_InfBasins.csv- calibrated' :   'SW - Inf. Basins - Baseline',
       'wyld_hru95_InfBasins.csv- calibrated' : 'WYLD - Inf. Basins - Baseline',
       'da_st_hru95_InfBasins.csv- calibrated' : 'DA_ST - Swales - Baseline',
       'sa_st_hru95_InfBasins.csv- calibrated' : 'SA_ST - Swales - Baseline',
        'prec_hru95_InfBasins.csv- calibrated' : 'Precipitation',

        }

dic_seriesname_infbasins110= {
        
       'dailycn_hru110_InfBasins.csv - altered_10' : 'Daily CN - Inf. Basins - Altered',
       'gwq_hru110_InfBasins.csv - altered_10' : 'GWQ - Inf. Basins - Altered',
       'latq_hru110_InfBasins.csv - altered_10' : 'LATQ - Inf. Basins - Altered',
       'percolated_hru110_InfBasins.csv - altered_10' : 'PERC - Inf. Basins - Altered',
       'surq_hru110_InfBasins.csv - altered_10' : 'SURQ - Inf. Basins - Altered',
       'sw_hru110_InfBasins.csv - altered_10' : 'SW - Inf. Basins - Altered',
       'wyld_hru110_InfBasins.csv - altered_10' : 'WYLD - Inf. Basins - Altered',
       'prec_hru110_InfBasins.csv - altered_10' : 'Precipitation',
       'da_st_hru110_InfBasins.csv - altered_10' : 'DA_ST - Swales - Altered',
       'sa_st_hru110_InfBasins.csv - altered_10' : 'SA_ST - Swales - Altered',
        
       'dailycn_hru110_InfBasins.csv - altered_30' : 'Daily CN - Inf. Basins - Altered',
       'gwq_hru110_InfBasins.csv - altered_30' : 'GWQ - Inf. Basins - Altered',
       'latq_hru110_InfBasins.csv - altered_30' : 'LATQ - Inf. Basins - Altered',
       'percolated_hru110_InfBasins.csv - altered_30' : 'PERC - Inf. Basins - Altered',
       'surq_hru110_InfBasins.csv - altered_30' : 'SURQ - Inf. Basins - Altered',
       'sw_hru110_InfBasins.csv - altered_30' : 'SW - Inf. Basins - Altered',
       'wyld_hru110_InfBasins.csv - altered_30' : 'WYLD - Inf. Basins - Altered',
       'prec_hru110_InfBasins.csv - altered_30' : 'Precipitation',
       'da_st_hru110_InfBasins.csv - altered_30' : 'DA_ST - Swales - Altered',
       'sa_st_hru110_InfBasins.csv - altered_30' : 'SA_ST - Swales - Altered',
       
       'dailycn_hru110_InfBasins.csv - altered_50' : 'Daily CN - Inf. Basins - Altered',
       'gwq_hru110_InfBasins.csv - altered_50' : 'GWQ - Inf. Basins - Altered',
       'latq_hru110_InfBasins.csv - altered_50' : 'LATQ - Inf. Basins - Altered',
       'percolated_hru110_InfBasins.csv - altered_50' : 'PERC - Inf. Basins - Altered',
       'surq_hru110_InfBasins.csv - altered_50' : 'SURQ - Inf. Basins - Altered',
       'sw_hru110_InfBasins.csv - altered_50' : 'SW - Inf. Basins - Altered',
       'wyld_hru110_InfBasins.csv - altered_50' : 'WYLD - Inf. Basins - Altered',
       'prec_hru110_InfBasins.csv - altered_50' : 'Precipitation',
       'da_st_hru110_InfBasins.csv - altered_50' : 'DA_ST - Swales - Altered',
       'sa_st_hru110_InfBasins.csv - altered_50' : 'SA_ST - Swales - Altered',
       
       
       'dailycn_hru110_InfBasins.csv - altered_70' : 'Daily CN - Inf. Basins - Altered',
       'gwq_hru110_InfBasins.csv - altered_70' : 'GWQ - Inf. Basins - Altered',
       'latq_hru110_InfBasins.csv - altered_70' : 'LATQ - Inf. Basins - Altered',
       'percolated_hru110_InfBasins.csv - altered_70' : 'PERC - Inf. Basins - Altered',
       'surq_hru110_InfBasins.csv - altered_70' : 'SURQ - Inf. Basins - Altered',
       'sw_hru110_InfBasins.csv - altered_70' : 'SW - Inf. Basins - Altered',
       'wyld_hru110_InfBasins.csv - altered_70' : 'WYLD - Inf. Basins - Altered',
       'prec_hru110_InfBasins.csv - altered_70' : 'Precipitation',
       'da_st_hru110_InfBasins.csv - altered_70' : 'DA_ST - Swales - Altered',
       'sa_st_hru110_InfBasins.csv - altered_70' : 'SA_ST - Swales - Altered',
       
       'dailycn_hru110_InfBasins.csv- calibrated': 'Daily CN - Inf. Basins - Baseline',
       'gwq_hru110_InfBasins.csv- calibrated'  : 'GWQ - Inf. Basins - Baseline',
       'latq_hru110_InfBasins.csv- calibrated' : 'LATQ - Inf. Basins - Baseline',
       'percolated_hru110_InfBasins.csv- calibrated' : 'PERC - Inf. Basins - Baseline',
       'surq_hru110_InfBasins.csv- calibrated' : 'SURQ - Inf. Basins - Baseline',
       'sw_hru110_InfBasins.csv- calibrated' :   'SW - Inf. Basins - Baseline',
       'wyld_hru110_InfBasins.csv- calibrated' : 'WYLD - Inf. Basins - Baseline',
       'prec_hru110_InfBasins.csv- calibrated' : 'Precipitation',
       'da_st_hru110_InfBasins.csv- calibrated' : 'DA_ST - Swales - Baseline',
       'sa_st_hru110_InfBasins.csv- calibrated' : 'SA_ST - Swales - Baseline',
        }


dic_seriesname_swales95= {
        
       'dailycn_hru95_swales.csv - altered_10' : 'Daily CN - Swales - Altered',
       'gwq_hru95_swales.csv - altered_10' : 'GWQ - Swales - Altered',
       'latq_hru95_swales.csv - altered_10' : 'LATQ - Swales - Altered',
       'percolated_hru95_swales.csv - altered_10' : 'PERC - Swales - Altered',
       'surq_hru95_swales.csv - altered_10' : 'SURQ - Swales - Altered',
       'sw_hru95_swales.csv - altered_10' : 'SW - Swales - Altered',
       'wyld_hru95_swales.csv - altered_10' : 'WYLD - Swales - Altered',
       'prec_hru95_swales.csv - altered_10' : 'Precipitation',
       'da_st_hru95_swales.csv - altered_10' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_swales.csv - altered_10' : 'SA_ST - Swales - Altered',
               
       'dailycn_hru95_swales.csv - altered_30' : 'Daily CN - Swales - Altered',
       'gwq_hru95_swales.csv - altered_30' : 'GWQ - Swales - Altered',
       'latq_hru95_swales.csv - altered_30' : 'LATQ - Swales - Altered',
       'percolated_hru95_swales.csv - altered_30' : 'PERC - Swales - Altered',
       'surq_hru95_swales.csv - altered_30' : 'SURQ - Swales - Altered',
       'sw_hru95_swales.csv - altered_30' : 'SW - Swales - Altered',
       'wyld_hru95_swales.csv - altered_30' : 'WYLD - Swales - Altered',
       'prec_hru95_swales.csv - altered_30' : 'Precipitation',
       'da_st_hru95_swales.csv - altered_30' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_swales.csv - altered_30' : 'SA_ST - Swales - Altered',
              
       'dailycn_hru95_swales.csv - altered_50' : 'Daily CN - Swales - Altered',
       'gwq_hru95_swales.csv - altered_50' : 'GWQ - Swales - Altered',
       'latq_hru95_swales.csv - altered_50' : 'LATQ - Swales - Altered',
       'percolated_hru95_swales.csv - altered_50' : 'PERC - Swales - Altered',
       'surq_hru95_swales.csv - altered_50' : 'SURQ - Swales - Altered',
       'sw_hru95_swales.csv - altered_50' : 'SW - Swales - Altered',
       'wyld_hru95_swales.csv - altered_50' : 'WYLD - Swales - Altered',
       'prec_hru95_swales.csv - altered_50' : 'Precipitation',
       'da_st_hru95_swales.csv - altered_50' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_swales.csv - altered_50' : 'SA_ST - Swales - Altered',
       
       'dailycn_hru95_swales.csv - altered_70' : 'Daily CN - Swales - Altered',
       'gwq_hru95_swales.csv - altered_70' : 'GWQ - Swales - Altered',
       'latq_hru95_swales.csv - altered_70' : 'LATQ - Swales - Altered',
       'percolated_hru95_swales.csv - altered_70' : 'PERC - Swales - Altered',
       'surq_hru95_swales.csv - altered_70' : 'SURQ - Swales - Altered',
       'sw_hru95_swales.csv - altered_70' : 'SW - Swales - Altered',
       'wyld_hru95_swales.csv - altered_70' : 'WYLD - Swales - Altered',
       'prec_hru95_swales.csv - altered_70' : 'Precipitation',
       'da_st_hru95_swales.csv - altered_70' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_swales.csv - altered_70' : 'SA_ST - Swales - Altered',
       
       
       'dailycn_hru95_swales.csv- calibrated': 'Daily CN - Inf. Basins - Baseline',
       'gwq_hru95_swales.csv- calibrated'  : 'GWQ - Inf. Basins - Baseline',
       'latq_hru95_swales.csv- calibrated' : 'LATQ - Inf. Basins - Baseline',
       'percolated_hru95_swales.csv- calibrated' : 'PERC - Swales - Baseline',
       'surq_hru95_swales.csv- calibrated' : 'SURQ - Inf. Basins - Baseline',
       'sw_hru95_swales.csv- calibrated' :   'SW - Inf. Basins - Baseline',
       'wyld_hru95_swales.csv- calibrated' : 'WYLD - Inf. Basins - Baseline',
       'prec_hru95_swales.csv- calibrated' : 'Precipitation',
       'da_st_hru95_swales.csv- calibrated' : 'DA_ST - Swales - Baseline',
       'sa_st_hru95_swales.csv- calibrated' : 'SA_ST - Swales - Baseline',
        }

dic_seriesname_swales110= {
        
       'dailycn_hru111_swales.csv - altered_10' : 'Daily CN - Swales - Altered',
       'gwq_hru111_swales.csv - altered_10' : 'GWQ - Swales - Altered',
       'latq_hru111_swales.csv - altered_10' : 'LATQ - Swales - Altered',
       'percolated_hru111_swales.csv - altered_10' : 'PERC - Swales - Altered',
       'surq_hru111_swales.csv - altered_10' : 'SURQ - Swales - Altered',
       'sw_hru111_swales.csv - altered_10' : 'SW - Swales - Altered',
       'wyld_hru111_swales.csv - altered_10' : 'WYLD - Swales - Altered',
       'da_st_hru111_swales.csv - altered_10' : 'DA_ST - Swales - Altered',
       'sa_st_hru111_swales.csv - altered_10' : 'SA_ST - Swales - Altered',
       'prec_hru111_swales.csv - altered_10' : 'Precipitation',
        
       'dailycn_hru111_swales.csv - altered_30' : 'Daily CN - Swales - Altered',
       'gwq_hru111_swales.csv - altered_30' : 'GWQ - Swales - Altered',
       'latq_hru111_swales.csv - altered_30' : 'LATQ - Swales - Altered',
       'percolated_hru111_swales.csv - altered_30' : 'PERC - Swales - Altered',
       'surq_hru111_swales.csv - altered_30' : 'SURQ - Swales - Altered',
       'sw_hru111_swales.csv - altered_30' : 'SW - Swales - Altered',
       'wyld_hru111_swales.csv - altered_30' : 'WYLD - Swales - Altered',
       'da_st_hru111_swales.csv - altered_30' : 'DA_ST - Swales - Altered',
       'sa_st_hru111_swales.csv - altered_30' : 'SA_ST - Swales - Altered',
       'prec_hru111_swales.csv - altered_30' : 'Precipitation',
              
       'dailycn_hru111_swales.csv - altered_50' : 'Daily CN - Swales - Altered',
       'gwq_hru111_swales.csv - altered_50' : 'GWQ - Swales - Altered',
       'latq_hru111_swales.csv - altered_50' : 'LATQ - Swales - Altered',
       'percolated_hru111_swales.csv - altered_50' : 'PERC - Swales - Altered',
       'surq_hru111_swales.csv - altered_50' : 'SURQ - Swales - Altered',
       'sw_hru111_swales.csv - altered_50' : 'SW - Swales - Altered',
       'wyld_hru111_swales.csv - altered_50' : 'WYLD - Swales - Altered',
       'da_st_hru111_swales.csv - altered_50' : 'DA_ST - Swales - Altered',
       'sa_st_hru111_swales.csv - altered_50' : 'SA_ST - Swales - Altered',
       'prec_hru111_swales.csv - altered_50' : 'Precipitation',
       
       'dailycn_hru111_swales.csv - altered_70' : 'Daily CN - Swales - Altered',
       'gwq_hru111_swales.csv - altered_70' : 'GWQ - Swales - Altered',
       'latq_hru111_swales.csv - altered_70' : 'LATQ - Swales - Altered',
       'percolated_hru111_swales.csv - altered_70' : 'PERC - Swales - Altered',
       'surq_hru111_swales.csv - altered_70' : 'SURQ - Swales - Altered',
       'sw_hru111_swales.csv - altered_70' : 'SW - Swales - Altered',
       'wyld_hru111_swales.csv - altered_70' : 'WYLD - Swales - Baseline',
       'prec_hru111_swales.csv - altered_70' : 'Precipitation',
       'da_st_hru111_swales.csv - altered_70' : 'DA_ST - Swales - Altered',
       'sa_st_hru111_swales.csv - altered_70' : 'SA_ST - Swales - Altered',
       
       
       'dailycn_hru111_swales.csv- calibrated': 'Daily CN - Inf. Basins - Baseline',
       'gwq_hru111_swales.csv- calibrated'  : 'GWQ - Inf. Basins - Baseline',
       'latq_hru111_swales.csv- calibrated' : 'LATQ - Inf. Basins - Baseline',
       'percolated_hru111_swales.csv- calibrated' : 'PERC - Inf. Basins - Baseline',
       'surq_hru111_swales.csv- calibrated' : 'SURQ - Inf. Basins - Baseline',
       'sw_hru111_swales.csv- calibrated' :   'SW - Inf. Basins - Baseline',
       'wyld_hru111_swales.csv- calibrated' : 'WYLD - Inf. Basins - Baseline',
       'prec_hru111_swales.csv- calibrated' : 'Precipitation',
       'da_st_hru111_swales.csv- calibrated' : 'DA_ST - Swales - Altered',
       'sa_st_hru111_swales.csv- calibrated' : 'SA_ST - Swales - Altered',
       
        }

dic_seriesname_biorretention95= {
        
       'dailycn_hru95_biorretention.csv - altered_10' : 'Daily CN - Swales - Altered',
       'gwq_hru95_biorretention.csv - altered_10' : 'GWQ - Biorretention - Altered',
       'latq_hru95_biorretention.csv - altered_10' : 'LATQ - Biorretention - Altered',
       'percolated_hru95_biorretention.csv - altered_10' : 'PERC - Biorretention - Altered',
       'surq_hru95_biorretention.csv - altered_10' : 'SURQ - Biorretention - Altered',
       'sw_hru95_biorretention.csv - altered_10' : 'SW - Biorretention - Altered',
       'wyld_hru95_biorretention.csv - altered_10' : 'WYLD - Biorretention - Altered',
       'prec_hru95_biorretention.csv - altered_10' : 'Precipitation',
       'da_st_hru95_biorretention.csv - altered_10' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_biorretention.csv - altered_10' : 'SA_ST - Swales - Altered',
        
       'dailycn_hru95_biorretention.csv - altered_30' : 'Daily CN - Biorretention - Altered',
       'gwq_hru95_biorretention.csv - altered_30' : 'GWQ - Biorretention - Altered',
       'latq_hru95_biorretention.csv - altered_30' : 'LATQ - Biorretention - Altered',
       'percolated_hru95_biorretention.csv - altered_30' : 'PERC - Biorretention - Altered',
       'surq_hru95_biorretention.csv - altered_30' : 'SURQ - Biorretention - Baseline',
       'sw_hru95_biorretention.csv - altered_30' : 'SW - Biorretention - Altered',
       'wyld_hru95_biorretention.csv - altered_30' : 'WYLD - Biorretention - Altered',
       'prec_hru95_biorretention.csv - altered_30' : 'Precipitation',
       'da_st_hru95_biorretention.csv - altered_30' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_biorretention.csv - altered_30' : 'SA_ST - Swales - Altered',
             
       'dailycn_hru95_biorretention.csv - altered_50' : 'Daily CN - Biorretention - Altered',
       'gwq_hru95_biorretention.csv - altered_50' : 'GWQ - Biorretention - Altered',
       'latq_hru95_biorretention.csv - altered_50' : 'LATQ - Biorretention - Altered',
       'percolated_hru95_biorretention.csv - altered_50' : 'PERC - Biorretention - Altered',
       'surq_hru95_biorretention.csv - altered_50' : 'SURQ - Biorretention - Alterede',
       'sw_hru95_biorretention.csv - altered_50' : 'SW - Biorretention - Altered',
       'wyld_hru95_biorretention.csv - altered_50' : 'WYLD - Biorretention - Altered',
       'prec_hru95_biorretention.csv - altered_50' : 'Precipitation',
       'da_st_hru95_biorretention.csv - altered_50' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_biorretention.csv - altered_50' : 'SA_ST - Swales - Altered',
       
       'dailycn_hru95_biorretention.csv - altered_70' : 'Daily CN - Biorretention - Altered',
       'gwq_hru95_biorretention.csv - altered_70' : 'GWQ - Biorretention - Altered',
       'latq_hru95_biorretention.csv - altered_70' : 'LATQ - Biorretention - Altered',
       'percolated_hru95_biorretention.csv - altered_70' : 'PERC - Biorretention - Altered',
       'surq_hru95_biorretention.csv - altered_70' : 'SURQ - Biorretention - Altered',
       'sw_hru95_biorretention.csv - altered_70' : 'SW - Biorretention - Altered',
       'wyld_hru95_biorretention.csv - altered_70' : 'WYLD - Biorretention - Altered',
       'prec_hru95_biorretention.csv - altered_70' : 'Precipitation',
       'da_st_hru95_biorretention.csv - altered_70' : 'DA_ST - Swales - Altered',
       'sa_st_hru95_biorretention.csv - altered_70' : 'SA_ST - Swales - Altered',
       
       
       'dailycn_hru95_biorretention.csv- calibrated': 'Daily CN - Biorretention - Baseline',
       'gwq_hru95_biorretention.csv- calibrated'  : 'GWQ - Biorretention - Baseline',
       'latq_hru95_biorretention.csv- calibrated' : 'LATQ - Biorretention - Baseline',
       'percolated_hru95_biorretention.csv- calibrated' : 'PERC - Biorretention - Baseline',
       'surq_hru95_biorretention.csv- calibrated' : 'SURQ - Biorretention - Baseline',
       'sw_hru95_biorretention.csv- calibrated' :   'SW - Biorretention - Baseline',
       'wyld_hru95_biorretention.csv- calibrated' : 'WYLD - Biorretention - Baseline',
       'prec_hru95_biorretention.csv- calibrated' : 'Precipitation',
       'da_st_hru95_biorretention.csv- calibrated' : 'DA_ST - Swales - Baseline',
       'sa_st_hru95_biorretention.csv- calibrated' : 'SA_ST - Swales - Baseline',
        }

dic_seriesname_biorretention110= {
        
       'dailycn_hru110_biorretention.csv - altered_10' : 'Daily CN - Biorretention - Altered',
       'gwq_hru110_biorretention.csv - altered_10' : 'GWQ - Biorretention - Altered',
       'latq_hru110_biorretention.csv - altered_10' : 'LATQ - Biorretention - Altered',
       'percolated_hru110_biorretention.csv - altered_10' : 'PERC - Biorretention - Altered',
       'surq_hru110_biorretention.csv - altered_10' : 'SURQ - Biorretention - Altered',
       'sw_hru110_biorretention.csv - altered_10' : 'SW - Biorretention - Altered',
       'wyld_hru110_biorretention.csv - altered_10' : 'WYLD - Biorretention - Altered',
       'prec_hru110_biorretention.csv - altered_10' : 'Precipitation',
       'da_st_hru110_biorretention.csv - altered_10' : 'DA_ST - Swales - Altered',
       'sa_st_hru110_biorretention.csv - altered_10' : 'SA_ST - Swales - Altered',
        
       'dailycn_hru110_biorretention.csv - altered_30' : 'Daily CN - Biorretention - Altered',
       'gwq_hru110_biorretention.csv - altered_30' : 'GWQ - Biorretention - Altered',
       'latq_hru110_biorretention.csv - altered_30' : 'LATQ - Biorretention - Altered',
       'percolated_hru110_biorretention.csv - altered_30' : 'PERC - Biorretention - Altered',
       'surq_hru110_biorretention.csv - altered_30' : 'SURQ - Biorretention - Altered',
       'sw_hru110_biorretention.csv - altered_30' : 'SW - Biorretention - Altered',
       'wyld_hru110_biorretention.csv - altered_30' : 'WYLD - Biorretention - Altered',
       'prec_hru110_biorretention.csv - altered_30' : 'Precipitation',
       'da_st_hru110_biorretention.csv - altered_30' : 'DA_ST - Swales - Altered',
       'sa_st_hru110_biorretention.csv - altered_30' : 'SA_ST - Swales - Altered',
       
       'dailycn_hru110_biorretention.csv - altered_50' : 'Daily CN - Biorretention - Altered',
       'gwq_hru110_biorretention.csv - altered_50' : 'GWQ - Biorretention - Altered',
       'latq_hru110_biorretention.csv - altered_50' : 'LATQ - Biorretention - Altered',
       'percolated_hru110_biorretention.csv - altered_50' : 'PERC - Biorretention - Altered',
       'surq_hru110_biorretention.csv - altered_50' : 'SURQ - Biorretention - Altered',
       'sw_hru110_biorretention.csv - altered_50' : 'SW - Biorretention - Altered',
       'wyld_hru110_biorretention.csv - altered_50' : 'WYLD - Biorretention - Altered',
       'prec_hru110_biorretention.csv - altered_50' : 'Precipitation',
       'da_st_hru110_biorretention.csv - altered_50' : 'DA_ST - Swales - Altered',
       'sa_st_hru110_biorretention.csv - altered_50' : 'SA_ST - Swales - Altered',
       
       'dailycn_hru110_biorretention.csv - altered_70' : 'Daily CN - Biorretention - Altered',
       'gwq_hru110_biorretention.csv - altered_70' : 'GWQ - Biorretention - Altered',
       'latq_hru110_biorretention.csv - altered_70' : 'LATQ - Biorretention - Altered',
       'percolated_hru110_biorretention.csv - altered_70' : 'PERC - Biorretention - Altered',
       'surq_hru110_biorretention.csv - altered_70' : 'SURQ - Biorretention - Altered',
       'sw_hru110_biorretention.csv - altered_70' : 'SW - Biorretention - Altered',
       'wyld_hru110_biorretention.csv - altered_70' : 'WYLD - Biorretention - Altered',
       'prec_hru110_biorretention.csv - altered_70' : 'Precipitation',
       'da_st_hru110_biorretention.csv - altered_70' : 'DA_ST - Swales - Altered',
       'sa_st_hru110_biorretention.csv - altered_70' : 'SA_ST - Swales - Altered',
       
       'dailycn_hru110_biorretention.csv- calibrated': 'Daily CN - Biorretention - Baseline',
       'gwq_hru110_biorretention.csv- calibrated'  : 'GWQ - Biorretention - Baseline',
       'latq_hru110_biorretention.csv- calibrated' : 'LATQ - Biorretention - Baseline',
       'percolated_hru110_biorretention.csv- calibrated' : 'PERC - Biorretention - Baseline',
       'surq_hru110_biorretention.csv- calibrated' : 'SURQ - Biorretention - Baseline',
       'sw_hru110_biorretention.csv- calibrated' :   'SW - Biorretention - Baseline',
       'wyld_hru110_biorretention.csv- calibrated' : 'WYLD - Biorretention - Baseline',
       'prec_hru110_biorretention.csv- calibrated' : 'Precipitation',
       'da_st_hru110_biorretention.csv- calibrated' : 'DA_ST - Swales - Baseline',
       'sa_st_hru110_biorretention.csv- calibrated' : 'SA_ST - Swales - Baseline',
       
        }



#/*------------------------------ Fix Here -------------------------------------------/*

###############################

def plotsubbasin(folder, dic, outname = None):
    

     files = os.listdir(folder)
     arrays_list=[]

     for f in files:
        my_address = os.path.join(folder, f)
        my_data = np.genfromtxt(my_address, delimiter=',', dtype=str,encoding="utf8")
        arrays_list.append([f,my_data])

     final_array_list = arrays_list
     
     dfs_to_plot = {}
     title_keys = {
                    'subbasincal.csv' : 'Baseline scenario',
                    'subbasin10.csv': '10% Reduction scenario',
                    'subbasin30.csv': '30% Reduction scenario',
                    'subbasin50.csv': '50% Reduction scenario',
                    'subbasin70.csv': '70% Reduction scenario'          
                    }

     for f in final_array_list:
        
         header_array = f[1][0,:].tolist()
         
         for h in range(1,len(header_array)):
             new_cell = header_array[h] + " - " + f[0]
             header_array[h] = new_cell
             
         df = pd.DataFrame(f[1][1:,:], columns = header_array)
         df.set_index(pd.DatetimeIndex(df['date']),inplace=True)
         df = df.drop('date',axis=1).convert_objects(convert_numeric=True)
         startdate ='2008-2-1'
         enddate='2008-2-28'
         dfs_to_plot[f[0]] = df.loc[startdate:enddate]
         
     temp_counter = 0
     colors = ['#913CCD', '#F15F74', '#F7CD3C', '#2CA8C2', '#98CB4A', '#839098', '#5481E6']
     calibrated_df = dfs_to_plot['subbasincal.csv']
     for df_to_plot in dfs_to_plot:
         dates_list = dfs_to_plot[df_to_plot].index.tolist()             
         counter=0
         df_to_plot_data = dfs_to_plot[df_to_plot]
         
         fig = plt.figure(figsize=(17,12))
         fig.autofmt_xdate()
         header_array = f[1][0,:].tolist()       
         
         ax1 = plt.subplot(411)
         ax2 = plt.subplot(412)
         ax3 = plt.subplot(413)
         ax4 = plt.subplot(414)
         
         for col_cal in calibrated_df.reindex(sorted(calibrated_df.columns), axis=1):
             data_to_plot = np.array(calibrated_df[col_cal].tolist())
             
             if 'prec' in col_cal:
                 pass
             elif 'sw' in col_cal :
                 ax2.plot(dates_list, data_to_plot, label=dic[col_cal +"-"+ outname], color = colors[counter], linestyle= '--', lw=3.0,alpha=0.7)    
                 counter+=1
             elif 'perc' in col_cal:             
                 ax3.plot(dates_list, data_to_plot, label=dic[col_cal +"-"+ outname], color = colors[counter], linestyle= '--', lw=3.0,alpha=0.7)      
                 counter+=1
             else:             
                 ax4.plot(dates_list, data_to_plot, label=dic[col_cal +"-"+ outname], color = colors[counter], linestyle= '--', lw=3.0,alpha=0.7)
                 counter+=1
             
         counter=0   
         for col in df_to_plot_data.reindex(sorted(df_to_plot_data.columns), axis=1):
             data_to_plot = np.array(dfs_to_plot[df_to_plot][col].tolist())
             
             if 'prec' in col:
                 ax1.bar(dates_list, data_to_plot, label=dic[col +"-"+ outname], color = '#4b9ad5', edgecolor='#67a9db', lw=2)

             elif 'sw' in col :
                 ax2.plot(dates_list, data_to_plot, label=dic[col +"-"+ outname], color = colors[counter])    
                 counter+=1
             elif 'perc' in col:             
                 ax3.plot(dates_list, data_to_plot, label=dic[col +"-"+ outname], color = colors[counter])    
                 counter+=1
             else:             
                 ax4.plot(dates_list, data_to_plot, label=dic[col +"-"+ outname], color = colors[counter])    
                 counter+=1
                
         ax1.set_xticks(dates_list)

         xfmt = mdates.DateFormatter('%d-%m-%y')
         ax1.xaxis.set_major_formatter(xfmt)
         ax1.set_title(title_keys[df_to_plot] + ' - SubBasin Level', fontsize = 18)
        
         ax1.set_xlim(startdate,enddate)
         ax1.grid()
         ax1.legend(loc='best', ncol=1)
         ax1.xaxis.set_major_formatter(xfmt)
         ax1.set_ylabel('Precipitation (mm)', size=14)
         ax1.tick_params(axis='x', which='major', labelsize=0)
         ax1.tick_params(axis='y', which='major', labelsize=14)
         
         ax2.set_xticks(dates_list)
         ax2.set_xlim(startdate,enddate)
         ax2.grid()
         ax2.legend(loc='lower right', ncol=2)
         ax2.xaxis.set_major_formatter(xfmt)
         ax2.set_ylabel('Soil Water (mm)', size=14)
         ax2.tick_params(axis='x', which='major', labelsize=0)
         ax2.tick_params(axis='y', which='major', labelsize=14)
        
         ax3.set_xticks(dates_list)
         ax3.set_xlim(startdate,enddate)
         ax3.grid()
         ax3.legend(loc='upper right', ncol=2)    
         ax3.xaxis.set_major_formatter(xfmt)
         ax3.set_ylabel('Percolatad \n Water (mm)', size=14)
         ax3.tick_params(axis='x', which='major', labelsize=0)
         ax3.tick_params(axis='y', which='major', labelsize=14)
         
         
         ax4.set_xticks(dates_list)
         ax4.set_xlim(startdate,enddate)
         ax4.grid()
         ax4.legend(loc='upper right', ncol=2)
         ax4.xaxis.set_major_formatter(xfmt)
         ax4.set_ylabel('Other Variables (mm)', size=14)
         ax4.tick_params(axis='x', which='major', labelsize=12,labelrotation=15)
         ax4.tick_params(axis='y', which='major', labelsize=14)
         
         plt.tight_layout()
         plt.savefig(outname+"%s"%title_keys[df_to_plot]+".png", dpi=300)
         temp_counter +=1
         plt.show()
         print(r"/*----------------------------/*")

##########################             
def plotflowout(folder, dic):
    
    colors = ['#3269c1', '#66c132', '#c85bff', '#000000', '#5481E6','#2CA8C2']
    linewidths = [4.7,3.6, 2.0 ,0.6]
    zolist = [2,4,6,8,10]
    arrays=[]
    files = os.listdir(folder)
    dicarrays={}
    
    for f in files:
        my_address = os.path.join(folder, f)
        my_data = np.genfromtxt(my_address, delimiter=',', dtype=str)
        arrays.append([f,my_data])
        
        for l in arrays:

            header_list = l[1][0,:].tolist()
            array = l[1][1:,:]
            var = 0
            for element in header_list:
                element_temp = element + "-" + l[0]
                header_list[var]=element_temp
                var+=1
                
            array_header = np.array(header_list)
            array = np.vstack((array_header,array))
        
            dicarrays[l[0]] = array

    for i in dicarrays:
        to_plot = dicarrays[i]
        to_plot_header = to_plot[0,:]
        to_plot_df = pd.DataFrame(to_plot[1:,:], columns = to_plot_header)
        dateindex = to_plot_header.tolist()[0]
        to_plot_df.set_index(pd.DatetimeIndex(to_plot_df[dateindex]),inplace=True)
        to_plot_df = to_plot_df.drop(dateindex,axis=1).convert_objects(convert_numeric=True)
        
        
        dates_list = pd.DataFrame(to_plot[:,0][1:], columns = ['date'])
        dates_list.set_index(pd.DatetimeIndex(dates_list['date']),inplace=True)
        startdate ='2008-2-1'
        enddate='2008-2-28'
        
                 
        dates_list = dates_list.loc[startdate:enddate]
        to_plot_df =  to_plot_df.loc[startdate:enddate]
        
        dates_list = dates_list.index.tolist()            
        startdate = dates_list[0]
        enddate = dates_list[-1]
        
        fig,ax = plt.subplots(figsize=(17,7))
        
        counter=0
        for val in to_plot_df:
            data_to_plot = to_plot_df[val].tolist()
            
            if 'calib' in val:
                ax.scatter(dates_list, data_to_plot, label=dic[val][0], color='red', zorder=15)
            else:
                ax.plot(dates_list, data_to_plot, label=dic[val][0], lw=linewidths[counter], color=colors[counter], zorder=zolist[counter])
                #ax.scatter(dates_list, data_to_plot, label=val, lw=linewidths[counter], color=colors[counter], zorder=counter_counter)
                counter+=1

        xfmt = mdates.DateFormatter('%d-%m-%y')
        ax.xaxis.set_major_formatter(xfmt)
        plt.xticks(dates_list, rotation=35, fontsize=14)
        plt.yticks(fontsize=14)
        plt.xlim(startdate,enddate)
        plt.grid()
        plt.legend(loc='best', ncol=2, fontsize = 14)
        #plt.xaxis.major_formatter(xfmt)
        plt.ylabel(r'Reach Flow(FLOW_OUT_cms) - $m^3$/s', fontsize=18)
        plt.title(dic[val][1], fontsize=24)
        plt.tight_layout()
        plt.savefig('%s.jpg'%i,dpi=300)
        plt.show()


bio_hru_95 = r'E:\OneDrive\swat_results\biorretention_hru\95_1248'
bio_hru_110 = r'E:\OneDrive\swat_results\biorretention_hru\110_1480'

swa_hru_110 = r'E:\OneDrive\swat_results\swales_hru\110_1554'
swa_hru_95 = r'E:\OneDrive\swat_results\swales_hru\95_1312'

inf_hru_95 = r'E:\OneDrive\swat_results\InfBasins_hru\95_1352'
inf_hru_110 = r'E:\OneDrive\swat_results\InfBasins_hru\110_1621'

bio_subbasin_95 = r'E:\OneDrive\swat_results\biorretention_basin\95'
bio_subbasin_110 = r'E:\OneDrive\swat_results\biorretention_basin\110'

swa_subbasin_110 = r'E:\OneDrive\swat_results\swales_basin\95'
swa_subbasin_95 = r'E:\OneDrive\swat_results\swales_basin\111'

inf_subbasin_95 = r'E:\OneDrive\swat_results\InfBasins_basin\95'
inf_subbasin_110 = r'E:\OneDrive\swat_results\InfBasins_basin\111'

bio = "Biorretention"
swa = "Swales"
inf = "Inf. Basins"

#/*------------------------------ Folders -------------------------------------------/*

#plothru(bio_hru_95, dic_seriesname_biorretention95, bio)
#plothru(bio_hru_110, dic_seriesname_biorretention110, bio)
#plothru(swa_hru_95, dic_seriesname_swales95, swa)
#plothru(swa_hru_110, dic_seriesname_swales110, swa)
#plothru(inf_hru_95, dic_seriesname_infbasins95, inf)
#plothru(inf_hru_110, dic_seriesname_infbasins110, inf)


dic_bio_sub_hru95 = dic_bio_sub_hru110 = {
        "prec - subbasin10.csv-Biorretention" : "Precipitation",
        "sw - subbasin10.csv-Biorretention": "SW - Inf. Basins - Altered",
        "perc - subbasin10.csv-Biorretention": "PERC - Biorretention - Altered",
        "gwq - subbasin10.csv-Biorretention": "GWQ - Biorretention - Altered",
        "latq - subbasin10.csv-Biorretention": "LATQ - Biorretention - Altered",
        "surq - subbasin10.csv-Biorretention": "SURQ - Biorretention - Altered",
        "wyld - subbasin10.csv-Biorretention": "WYLD - Biorretention - Altered",
        
        "prec - subbasin30.csv-Biorretention" : "Precipitation",
        "sw - subbasin30.csv-Biorretention": "SW - Inf. Basins - Altered",
        "perc - subbasin30.csv-Biorretention": "PERC - Biorretention - Altered",
        "gwq - subbasin30.csv-Biorretention": "GWQ - Biorretention - Altered",
        "latq - subbasin30.csv-Biorretention": "LATQ - Biorretention - Altered",
        "surq - subbasin30.csv-Biorretention": "SURQ - Biorretention - Altered",
        "wyld - subbasin30.csv-Biorretention": "WYLD - Biorretention - Altered",
        
        "prec - subbasin50.csv-Biorretention" : "Precipitation",
        "sw - subbasin50.csv-Biorretention": "SW - Inf. Basins - Altered",
        "perc - subbasin50.csv-Biorretention": "PERC - Biorretention - Altered",
        "gwq - subbasin50.csv-Biorretention": "GWQ - Biorretention - Altered",
        "latq - subbasin50.csv-Biorretention": "LATQ - Biorretention - Altered",
        "surq - subbasin50.csv-Biorretention": "SURQ - Biorretention - Altered",
        "wyld - subbasin50.csv-Biorretention": "WYLD - Biorretention - Altered",

        "prec - subbasin70.csv-Biorretention" : "Precipitation",
        "sw - subbasin70.csv-Biorretention": "SW - Inf. Basins - Altered",
        "perc - subbasin70.csv-Biorretention": "PERC - Biorretention - Altered",
        "gwq - subbasin70.csv-Biorretention": "GWQ - Biorretention - Altered",
        "latq - subbasin70.csv-Biorretention": "LATQ - Biorretention - Altered",
        "surq - subbasin70.csv-Biorretention": "SURQ - Biorretention - Altered",
        "wyld - subbasin70.csv-Biorretention": "WYLD - Biorretention - Altered",
        
        "prec - subbasincal.csv-Biorretention" : "Precipitation",
        "sw - subbasincal.csv-Biorretention": "SW - Inf. Basins - Baseline",
        "perc - subbasincal.csv-Biorretention": "PERC - Biorretention - Baseline",
        "gwq - subbasincal.csv-Biorretention": "GWQ - Biorretention - Baseline",
        "latq - subbasincal.csv-Biorretention": "LATQ - Biorretention - Baseline",
        "surq - subbasincal.csv-Biorretention": "SURQ - Biorretention - Baseline",
        "wyld - subbasincal.csv-Biorretention": "WYLD - Biorretention - Baseline",
        
        }

dic_bio_swa_hru95 = dic_bio_swa_hru110 = {
        "prec - subbasin10.csv-Swales" : "Precipitation",
        "sw - subbasin10.csv-Swales": "SW - Inf. Basins - Altered",
        "perc - subbasin10.csv-Swales": "PERC - Swales - Altered",
        "gwq - subbasin10.csv-Swales": "GWQ - Swales - Altered",
        "latq - subbasin10.csv-Swales": "LATQ - Swales - Altered",
        "surq - subbasin10.csv-Swales": "SURQ - Swales - Altered",
        "wyld - subbasin10.csv-Swales": "WYLD - Swales - Altered",
        
        "prec - subbasin30.csv-Swales" : "Precipitation",
        "sw - subbasin30.csv-Swales": "SW - Inf. Basins - Altered",
        "perc - subbasin30.csv-Swales": "PERC - Swales - Altered",
        "gwq - subbasin30.csv-Swales": "GWQ - Swales - Altered",
        "latq - subbasin30.csv-Swales": "LATQ - Swales - Altered",
        "surq - subbasin30.csv-Swales": "SURQ - Swales - Altered",
        "wyld - subbasin30.csv-Swales": "WYLD - Swales - Altered",
        
        "prec - subbasin50.csv-Swales" : "Precipitation",
        "sw - subbasin50.csv-Swales": "SW - Inf. Basins - Altered",
        "perc - subbasin50.csv-Swales": "PERC - Swales - Altered",
        "gwq - subbasin50.csv-Swales": "GWQ - Swales - Altered",
        "latq - subbasin50.csv-Swales": "LATQ - Swales - Altered",
        "surq - subbasin50.csv-Swales": "SURQ - Swales - Altered",
        "wyld - subbasin50.csv-Swales": "WYLD - Swales - Altered",

        "prec - subbasin70.csv-Swales" : "Precipitation",
        "sw - subbasin70.csv-Swales": "SW - Inf. Basins - Altered",
        "perc - subbasin70.csv-Swales": "PERC - Swales - Altered",
        "gwq - subbasin70.csv-Swales": "GWQ - Swales - Altered",
        "latq - subbasin70.csv-Swales": "LATQ - Swales - Altered",
        "surq - subbasin70.csv-Swales": "SURQ - Swales - Altered",
        "wyld - subbasin70.csv-Swales": "WYLD - Swales - Altered",
        
        "prec - subbasincal.csv-Swales" : "Precipitation",
        "sw - subbasincal.csv-Swales": "SW - Inf. Basins - Baseline",
        "perc - subbasincal.csv-Swales": "PERC - Swales - Baseline",
        "gwq - subbasincal.csv-Swales": "GWQ - Swales - Baseline",
        "latq - subbasincal.csv-Swales": "LATQ - Swales - Baseline",
        "surq - subbasincal.csv-Swales": "SURQ - Swales - Baseline",
        "wyld - subbasincal.csv-Swales": "WYLD - Swales - Baseline",
        
        }

dic_bio_infb_hru95 = dic_bio_infb_hru110 = {
        "prec - subbasin10.csv-Inf. Basins" : "Precipitation",
        "sw - subbasin10.csv-Inf. Basins": "SW - Inf. Basins - Altered",
        "perc - subbasin10.csv-Inf. Basins": "PERC - Inf. Basins - Altered",
        "gwq - subbasin10.csv-Inf. Basins": "GWQ - Inf. Basins - Altered",
        "latq - subbasin10.csv-Inf. Basins": "LATQ - Inf. Basins - Altered",
        "surq - subbasin10.csv-Inf. Basins": "SURQ - Inf. Basins - Altered",
        "wyld - subbasin10.csv-Inf. Basins": "WYLD - Inf. Basins - Altered",
        
        "prec - subbasin30.csv-Inf. Basins" : "Precipitation",
        "sw - subbasin30.csv-Inf. Basins": "SW - Inf. Basins - Altered",
        "perc - subbasin30.csv-Inf. Basins": "PERC - Inf. Basins - Altered",
        "gwq - subbasin30.csv-Inf. Basins": "GWQ - Inf. Basins - Altered",
        "latq - subbasin30.csv-Inf. Basins": "LATQ - Inf. Basins - Altered",
        "surq - subbasin30.csv-Inf. Basins": "SURQ - Inf. Basins - Altered",
        "wyld - subbasin30.csv-Inf. Basins": "WYLD - Inf. Basins - Altered",
        
        "prec - subbasin50.csv-Inf. Basins" : "Precipitation",
        "sw - subbasin50.csv-Inf. Basins": "SW - Inf. Basins - Altered",
        "perc - subbasin50.csv-Inf. Basins": "PERC - Inf. Basins - Altered",
        "gwq - subbasin50.csv-Inf. Basins": "GWQ - Inf. Basins - Altered",
        "latq - subbasin50.csv-Inf. Basins": "LATQ - Inf. Basins - Altered",
        "surq - subbasin50.csv-Inf. Basins": "SURQ - Inf. Basins - Altered",
        "wyld - subbasin50.csv-Inf. Basins": "WYLD - Inf. Basins - Altered",

        "prec - subbasin70.csv-Inf. Basins" : "Precipitation",
        "sw - subbasin70.csv-Inf. Basins": "SW - Inf. Basins - Altered",
        "perc - subbasin70.csv-Inf. Basins": "PERC - Inf. Basins - Altered",
        "gwq - subbasin70.csv-Inf. Basins": "GWQ - Inf. Basins - Altered",
        "latq - subbasin70.csv-Inf. Basins": "LATQ - Inf. Basins - Altered",
        "surq - subbasin70.csv-Inf. Basins": "SURQ - Inf. Basins - Altered",
        "wyld - subbasin70.csv-Inf. Basins": "WYLD - Inf. Basins - Altered",
        
        "prec - subbasincal.csv-Inf. Basins" : "Precipitation",
        "sw - subbasincal.csv-Inf. Basins": "SW - Inf. Basins - Baseline",
        "perc - subbasincal.csv-Inf. Basins": "PERC - Inf. Basins - Baseline",
        "gwq - subbasincal.csv-Inf. Basins": "GWQ - Inf. Basins - Baseline",
        "latq - subbasincal.csv-Inf. Basins": "LATQ - Inf. Basins - Baseline",
        "surq - subbasincal.csv-Inf. Basins": "SURQ - Inf. Basins - Baseline",
        "wyld - subbasincal.csv-Inf. Basins": "WYLD - Inf. Basins - Baseline",
        
        }
#plotsubbasin(bio_subbasin_95, dic= dic_bio_sub_hru95, outname = "Biorretention")
#plotsubbasin(bio_subbasin_110, dic=dic_bio_sub_hru110, outname = "Biorretention")
#plotsubbasin(swa_subbasin_95, dic=dic_bio_swa_hru95, outname = "Swales")
#plotsubbasin(swa_subbasin_110, dic=dic_bio_swa_hru110, outname = "Swales")
#plotsubbasin(inf_subbasin_95, dic=dic_bio_infb_hru95, outname = "Inf. Basins")
#plotsubbasin(inf_subbasin_110, dic=dic_bio_infb_hru110, outname = "Inf. Basins")

dic_swa_flw = {
        'altered_10-swales155.csv': ['Swales 10% reduction', 'Swales - CX Station'],
        'altered_30-swales155.csv': ['Swales 30% reduction', 'Swales - CX Station'],
        'altered_50-swales155.csv': ['Swales 50% reduction', 'Swales - CX Station'],
        'altered_70-swales155.csv': ['Swales 70% reduction', 'Swales - CX Station'],
        'calibrated-swales155.csv': ['Swales-Calibrated', 'Swales - CX Station'],

        'altered_10-swales98.csv': ['Swales 10% reduction', 'Swales - SQ Station'],
        'altered_30-swales98.csv': ['Swales 30% reduction', 'Swales - SQ Station'],
        'altered_50-swales98.csv': ['Swales 50% reduction', 'Swales - SQ Station'],
        'altered_70-swales98.csv': ['Swales 70% reduction', 'Swales - SQ Station'],
        'calibrated-swales98.csv': ['Swales-Calibrated', 'Swales - SQ Station'],
        
        }

dic_inf_flw = {
        'altered_10-InfBasins155.csv': ['Inf. Basins 10% reduction', 'Inf. Basins - CX Station'],
        'altered_30-InfBasins155.csv': ['Inf. Basins 30% reduction', 'Inf. Basins - CX Station'],
        'altered_50-InfBasins155.csv': ['Inf. Basins 50% reduction', 'Inf. Basins - CX Station'],
        'altered_70-InfBasins155.csv': ['Inf. Basins 70% reduction', 'Inf. Basins - CX Station'],
        'calibrated-InfBasins155.csv': ['Inf. Basins-Calibrated', 'Inf. Basins - CX Station'],

        'altered_10-InfBasins99.csv': ['Inf. Basins 10% reduction', 'Inf. Basins - SQ Station'],
        'altered_30-InfBasins99.csv': ['Inf. Basins 30% reduction', 'Inf. Basins - SQ Station'],
        'altered_50-InfBasins99.csv': ['Inf. Basins 50% reduction', 'Inf. Basins - SQ Station'],
        'altered_70-InfBasins99.csv': ['Inf. Basins 70% reduction', 'Inf. Basins - SQ Station'],
        'calibrated-InfBasins99.csv': ['Inf. Basins-Calibrated', 'Inf. Basins - SQ Station'],
        }

dic_bio_flw = {
        'altered_10-biorretention155.csv': ['Biorretention 10% reduction', 'Biorretention - CX Station'],
        'altered_30-biorretention155.csv': ['Biorretention 30% reduction', 'Biorretention - CX Station'],
        'altered_50-biorretention155.csv': ['Biorretention 50% reduction', 'Biorretention - CX Station'],
        'altered_70-biorretention155.csv': ['Biorretention 70% reduction', 'Biorretention - CX Station'],
        'calibrated-biorretention155.csv': ['Biorretention-Calibrated', 'Biorretention - CX Station'],

        'altered_10-biorretention99.csv': ['Biorretention 10% reduction', 'Biorretention - SQ Station'],
        'altered_30-biorretention99.csv': ['Biorretention 30% reduction', 'Biorretention - SQ Station'],
        'altered_50-biorretention99.csv': ['Biorretention 50% reduction', 'Biorretention - SQ Station'],
        'altered_70-biorretention99.csv': ['Biorretention 70% reduction', 'Biorretention - SQ Station'],
        'calibrated-biorretention99.csv': ['Biorretention-Calibrated', 'Biorretention - SQ Station'],
        }

swa_flw = r'E:\OneDrive\swat_results\swales_flow_out'
bio_flw = r'E:\OneDrive\swat_results\biorretention_flow_out'
inf_flw = r'E:\OneDrive\swat_results\InfBasins_flow_out'

plotflowout(swa_flw, dic_swa_flw)
plotflowout(inf_flw, dic_inf_flw)
plotflowout(bio_flw, dic_bio_flw)
