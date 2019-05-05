# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 21:16:30 2018

@author: david
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dic_par

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

class output_rch:
    
    def __init__(self,fileadress,rch_filter,par_filter,observed_input = None, rel_table = None):
        self.rch_filter = rch_filter
        self.observed_input = observed_input
        self.rel_table = rel_table
        self.par_filter = par_filter
        
    """Takes an output.rch file and parses it for reach number and desired parameters
    fileadress = the file address as string
    rch_filter = takes integer, list of integers and 'all' as arguments
    par_silter = takes string, list of strings and 'all' as arguments
    observed_input = Numpy array with header: "GDAY", "STATION1_FLOW", "STATION2_FLOW", ..."STATIONn_FLOW"
    rel_table = nx2 array with first collumn "RCH_NUMBER", "STATION NAME"

    returns numpy array 
    
    Methods: read_rch(), print_allinone(output_folder), print_manyinfolder(output_folder)
    """
    def read_rch(self):
#Function local parameter definition        
        rch_filter = self.rch_filter
        par_filter = self.par_filter
        observed_input = self.observed_input 
        rel_table = self.rel_table
#Opens file and gets header
        from_file = open(fileadress, 'r')   
        lines = from_file.readlines()
        result_list=lines[9:]
        header = lines[8].split()
#Creates list of lists for result array array 
        result_list_parse1 = []
        for i in result_list:
            a = i.split()[1:]
            result_list_parse1.append(a)
#Creates array with the result array list of lists
        result_array = np.array(result_list_parse1,dtype = float) #Creates array from only data array 
        days_g_address = header.index("MON")# Address for gregorian day 
        rch_address = header.index("RCH")#Address for rch collumn
#Parses data from the rch_filter parameter - Takes integer and list or all###
        if rch_filter != 'all':
            if type(rch_filter) == int :
                result_array_filtered=result_array[result_array[:,rch_address] == rch_filter]
            elif type(rch_filter) == list :
                for k in rch_filter:
                    result_array_filtered=result_array[result_array[:,rch_address] == k]
                
        days_g = result_array_filtered[:,days_g_address]#Fetches the dates from file
        days_sim = np.array(np.arange(1,days_g.shape[0]+1),dtype = float)#Counts them from 1 to sim end
    
        result_array_filtered = np.insert(result_array_filtered,2,days_sim,axis = 1) #inserts gday simday array
        header.insert(2,"SDG") #inserts on the header the Simulation Gregorian days Collumn header
#Finds the number of collumns to be fetched     
        if type(par_filter) == list:
            coln_final_array = len(par_filter)
        if type(par_filter) == str:
            coln_final_array = 1

        a = np.zeros((result_array_filtered.shape[0], int(coln_final_array)))
        a = np.insert(a,0,result_array_filtered[:,2], axis = 1)
    
        col_index_list = []
#Parses and filters the par_filter parameter - Takes string, list of strings as parameters and 'all'
        if par_filter != 'all':
            if type(par_filter) == list:
                for i in par_filter:
                    col_interest = header.index(i)#Fetches the parameter filter as a collumn number
                    col_index_list.append(col_interest)
            if type(par_filter) == str:
                col_interest = header.index(par_filter)#Fetches the parameter filter as multiple collumn numbers
                col_index_list.append(col_interest)
#Creates the final array with the desired variables
        count = 0
        for i in col_index_list:
            analysis_array = result_array_filtered[:,i]
            a[:,count] = analysis_array
            count = count+1
        
        if type(par_filter) == list:
            a_header = ["GDAY"]
            for i in par_filter:
                a_header.append(i)
            a_header_array = np.array(a_header).T
            a = np.insert(a, a_header_array, 0, axis=0)
            return a 
        
        elif type(par_filter) == str:
            a_header = ["GDAY"]
            a_header.append(par_filter)
            a_header_array = np.array(a_header).T
            a = np.insert(a, a_header_array, 0, axis=0)
            return a 
    
    def print_allinone(self):
        #Single parameters
        #Multiple parameters
        
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
        
        def print_many_infolder(self):
        #Single parameters
        #Multiple parameters
            a = 2

class output_hru:

    def __init__(self,output_hru_fileadress,subbasin = 'all', lulc = 'all', hru_range = 'all',get_output = 'all'):
    
        self.fileadress = output_hru_fileadress
        self.subasin = subbasin
        self.lulc = lulc
        self.hru_range = hru_range
        self.get_output = get_output
    
    def print_hru(array):
        p=2

    def read_hru(self):
        
        instance = dic_par.param_dic()
        
#Parses the get output as either all or a given list
        if self.get_output != 'all':
            try:
                hru_header_list = self.get_output
            except:
                print("Your get_output parameter has problems. It takes either all or an \
                  integer list")
                exit()
        else:
            try:
                hru_header_list = instance.dic_hru_parser()
            except:
                print ("Your dictionary is not returning keys. Please make sure \
                       you have the dictionary in the working folder")
                
        #Fetches a header and a data list
        from_file = open(self.fileadress, 'r')
        lines = from_file.readlines()
        data = lines[9:]
        header = lines[8]
        len_line_first = len(data[0].split())
        first_line_coln = [list(range(len_line_first))]
#Creates a data list from readlines
        for line in data:
            temp = line.split()
            first_line_coln.append(temp)
        
#Creates an indexed list of lists for the data
        data_indexed_list = first_line_coln
        data_indexed_array = np.array(data_indexed_list)
        header_temp= data_indexed_array[0,:]
        z = np.argsort(header_temp)
        data_indexed_array_sorted = data_indexed_array[:,z]
        
#Creates an indexed list of lists for the header
        k=-1
        pos_dic = {}
        for item in hru_header_list:
    
                sep_item = list(header)
                item_start = header.find(item)
                if item_start != -1:
                    k = k+1
                    len_item = len(item)
                    item_end = item_start+len_item
                    header_to_list = sep_item[item_start:item_end]
                    header_to_list = ''.join(header_to_list)
                    pos_dic[header_to_list] = k
                else:
                    pass           
        header_array = np.array(pos_dic.items()).T
#Sorts the header array 
        header_array_temp = header_array[1,:]
        w = np.argsort(header_array_temp)
        header_array_sorted = header_array[:,w]
#Joins header and data arrays by index
        final_array = np.vstack((header_array_sorted,data_indexed_array_sorted))
#Deletes the index lines
        final_array = np.delete(final_array,(1,2), axis=0)
        
#filters array by subbasin - Takes list, integer or all
        if self.subasin != 'all':
            if type(self.subbasin) == list:
                header_text = final_array[0,:]
                sub_index = np.where(header_text == 'SUB')
                for i in self.subbasin:
                    final_array = final_array[final_array[:,sub_index] == i]
            elif type(self.subbasin) == int:
                header_text = final_array[0,:]
                sub_index = np.where(header_text == 'SUB')
                final_array = final_array[final_array[:,sub_index] == i]
                
#filters array by hru number range - Takes list, integer or all
        if self.hru_range != 'all':
            if type(self.hru_range) == list:
                header_text = final_array[0,:]
                hru_index = np.where(header_text == 'HRU')
                for i in self.hru_range:
                    final_array = final_array[final_array[:,hru_index] == i]
            elif type(self.hru_range) == int:
                header_text = final_array[0,:]
                hru_index = np.where(header_text == 'HRU')
                final_array = final_array[final_array[:,hru_index] == i]
#filters array by lulc - Takes list of string, or a single string
        if self.lulc != 'all':
            if type(self.lulc) == list:
                header_text = final_array[0,:]
                lulc_index = np.where(header_text == 'LULC')
                for i in self.lulc:
                    final_array = final_array[final_array[:,lulc_index] == i]
            elif type(self.lulc) == str:
                final_array = final_array[final_array[:,lulc_index] == i]
        return final_array 
    
hru_file = r'C:\Barigui\SwatBarigui6\Scenarios\Default\TxtInOut\output.rch'
instance = output_hru(hru_file)
table = instance.read_hru()
        
#fileadress = r'D:\OneDrive\output.rch'
#instance = output_rch(fileadress,39,["FLOW_INcms","FLOW_OUTcms"])
#array = instance.read_rch()
#print_rch(a)   "FLOW_OUTcms"