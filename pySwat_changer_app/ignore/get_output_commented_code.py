# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 21:16:30 2018

@author: david
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dic_par
import datetime

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
    
    def __init__(self,fileaddress,rch_filter,par_filter,observed_input = None, 
                 rel_table = None):
        self.rch_filter = rch_filter
        self.observed_input = observed_input
        self.rel_table = rel_table
        self.par_filter = par_filter
        self.fileaddress = fileaddress
        
    """Takes an output.rch file and parses it for reach number and desired 
    parameters
    fileadress = the file address as string
    rch_filter = takes integer, list of integers and 'all' as arguments
    par_silter = takes string, list of strings and 'all' as arguments
    observed_input = Numpy array with header: "GDAY", "STATION1_FLOW", 
    "STATION2_FLOW", ..."STATIONn_FLOW"
    rel_table = nx2 array with first collumn "RCH_NUMBER", "STATION NAME"

    returns numpy array 
    
    Methods: read_rch(), print_allinone(output_folder), 
    print_manyinfolder(output_folder)
    """
    
    def getns(self):
        if self.observed_input == None:
            print("Your observed series file is empty")
        else:
            nrows_series = temp_array_date.shape[0]
            keys = list(rel_table.keys())
            ns_dic = {}
            for i in keys:
                key_from_rch = rel_table[i]
                if key_from_rch in rch_filter:
                    series = mydata[i]
                    series_array = series.values
                    nrows_mydata = series_array.shape[0]
                    ns = NS(eff_array[:,0],eff_array[:,1])
        print (ns_dic)
        return ns_dic
    
    def read_rch(self):
#Function local parameter definition        
        rch_filter = self.rch_filter
        par_filter = self.par_filter
        observed_input = self.observed_input 
        rel_table = self.rel_table
#Reads personal data 
        if observed_input != None and rel_table != None:
            self.my_data = pd.read_csv(observed_input, delimiter=',',
                                       index_col = "GDAY")
            self.flag_pdata = True            
        else:
            print("Please input both observed inputs and relational tables 
                  correctly!")
#Opens file and gets header
        from_file = open(self.fileaddress, 'r')   
        lines = from_file.readlines()
        result_list=lines[9:]
        header = lines[8].split()
#Creates list of lists for result array array 
        result_list_parse1 = []
        for i in result_list:
            a = i.split()[1:]
            result_list_parse1.append(a)
#Creates array with the result array list of lists
        #Creates array from only data array 
        result_array = np.array(result_list_parse1) 
        #tests for printed calendar dates        
        if ("MO") in header:
    
            mo_address = header.index("MO")# Address for gregorian day 
            day_address = header.index("DA")
            year_address = header.index("YR")
    
        else:            
            mo_address = header.index("MON")      
        
        rch_address = header.index("RCH")#Address for rch collumn
        
#Parses data from the rch_filter parameter - Takes integer and list or all###
        if rch_filter != 'all':
            if type(rch_filter) == int :
                result_array_filtered=result_array[result_array[:,
                                            rch_address] == str(rch_filter)]
            elif type(rch_filter) == list :
                for k in rch_filter:
                    if k == rch_filter[0]:
                        array_filtered = result_array[result_array[:,
                                            rch_address] == str(k)]
                    else:
                        array_filtered_temp = result_array[result_array[:,
                                                        rch_address] == str(k)]
                        array_filtered = np.vstack((array_filtered,
                                                    array_filtered_temp))
                
                result_array_filtered = array_filtered
        
        if ("MO") in header:        
            
            dayArray = result_array_filtered[:,day_address]
            monthArray = result_array_filtered[:,mo_address]
            yearArray = result_array_filtered[:,year_address]
            
            date_zero = (datetime.date(int(yearArray[0]),int(monthArray[0]),
                                       int(dayArray[0])))
            gdays = []
            date_list = []
            date_list_string = []
            
            for i in range(result_array_filtered.shape[0]):
                date_temp = (datetime.date(int(yearArray[i]),int(monthArray[i]),
                                           int(dayArray[i])))
                gdays.append((date_temp - date_zero).days)
                date_list.append(date_temp)
                date_list_string.append(date_temp.strftime('%m/%d/%Y'))
            
            date_array = np.array(gdays)
            days_sim = date_array
            result_array_filtered = np.insert(result_array_filtered,2,
                                  days_sim,axis = 1) #inserts gday simday array
            header.insert(2,"SDG") 
            #inserts on the header the Simulation Gregorian days Collumn header
        
        else:
            gdays = list(range(1,result_array_filtered.shape[0]+1))
            date_array = np.array(gdays)
            days_sim = date_array
            result_array_filtered = np.insert(result_array_filtered,2,
                                days_sim,axis = 1) #inserts gday simday array
            header.insert(2,"SDG") 
            #inserts on the header the Simulation Gregorian days Collumn header
#Finds the number of collumns to be fetched     
        if type(par_filter) == list:
            coln_final_array = len(par_filter)
        if type(par_filter) == str:
            coln_final_array = 1

        a = np.empty((result_array_filtered.shape[0], int(coln_final_array)))
        gdays_row = np.array(result_array_filtered[:,2],dtype = int)
        a = np.insert(a,0,gdays_row, axis = 1)
        rch_row = np.array(result_array_filtered[:,0],dtype = int)
        a = np.insert(a,1,rch_row, axis = 1)
        #date_row = np.array(date_list_string)
        #a = np.insert(a,1,date_row, axis = 1)
        col_index_list = []
#Parses and filters the par_filter parameter - Takes string, list of strings as
     #parameters and 'all'
        if par_filter != 'all':
            if type(par_filter) == list:
                for i in par_filter:
    #Fetches the parameter filter as a collumn number
                    col_interest = header.index(i) 
                    col_index_list.append(col_interest)
            if type(par_filter) == str:
    #Fetches the parameter filter as multiple collumn numbers
                col_interest = header.index(par_filter)
                col_index_list.append(col_interest)
#Creates the final array with the desired variables
        count = 2
        for i in col_index_list:
            analysis_array = result_array_filtered[:,i]
            a[:,count] = analysis_array
            count = count+1
        
        if type(par_filter) == list:
            a_header = ["GDAY", "RCH"]
            for i in par_filter:
                a_header.append(i)
            a_header_array = np.array(a_header).T
            a = np.vstack((a_header_array,a))
            return a 
        
        elif type(par_filter) == str:
            a_header = ["GDAY","RCH"]
            a_header.append(par_filter)
            a_header_array = np.array(a_header).T
            a = np.vstack((a_header_array,a))
            return a 
    
    def print_allinone(self,array, figsize):
        rch_filter = self.rch_filter
        rel_table = self.rel_table
        colormap = plt.cm.inferno
        header = array[0,:].T
        rch_column = np.where(header == 'RCH')[0][0]
        gday_column = np.where(header == 'GDAY')[0][0]
        variables = np.unique(header[2:])
        rches = np.unique(array[2:,rch_column])
        
        colors = np.linspace(0,255,len(rches),dtype = int)
        for var in variables:
            fig = plt.figure(figsize = figsize)
            counter = 0
            for rch in sorted(rches):
                var_column = np.where(header == var)[0][0]
                temp_array = array[array[:,rch_column] == rch]
                temp_array_var = temp_array[:,var_column]
                temp_array_var = temp_array_var.astype(float)
                temp_array_date = temp_array[:,gday_column]
                temp_array_date = temp_array_date.astype(float)
                
                colors_counter = colors[counter]
                rgb = colormap(colors_counter)
                plt.plot(temp_array_date, temp_array_var, lw = 0.7, 
                         label = r"Rch # %s"%(rch), color = rgb, alpha = 0.9)
                counter = counter+1
                         
                plt.title('Simulated variables', fontsize=24)
                plt.xlim(0, len(temp_array_date))
                #plt.ylim(-0.3,np.amax(temp_array_var))
                plt.xlabel('Simulation days', fontsize=20)
                plt.ylabel('%s'%var, fontsize=18)
                plt.tick_params(axis='both', which='major', labelsize=20)
                plt.tick_params(axis='both', which='minor', labelsize=20)
                plt.legend(fontsize=18)
                plt.tight_layout()
                
                mydata = self.my_data
#Calculates NS from series if in dictionary and in myfiles
                string_to_annotate = ''
                for i in list(rel_table.values()):
                    i_string = '%.1f' % i
                    temp_array_ef = array[array[:,rch_column] == i_string]

                    if temp_array_ef.shape[0] != 0:
                        s = temp_array_ef[:,2]
                        expected_mydata_length = s.shape[0]
                        
                        s = s.astype(np.float).T
                        s_index = np.array(list(range(1,len(s)+1))).T
                        s = np.vstack((s_index,s)).T
                        
                        o = mydata[list(rel_table.keys())[list(
                                rel_table.values()).index(i)]].values)
                        
                        mydata_length = o.shape[0]
                        
                        if expected_mydata_length != mydata_length:
                            print('''The simulation has %.0f days. Your data 
      has %.0f days. Please correct that. Please notices that text files with 
  empty values still count as cells, so check them!'''%
  (expected_mydata_length,mydata_length))
                        
                        eff_array = np.insert(s, 1, o, axis=1)
                        eff_array = eff_array[~np.isnan(eff_array).any(axis=1)]
                        ns = NS(eff_array[:,1],eff_array[:,2])
#CREATE ANNOTATION ON PLOT 
                        string_to_annotate += 'NS for station %s = %.3f \n'%(i,ns)
                plt.annotate(string_to_annotate, xy=(0.80, 0.95),  
                             xycoords='figure fraction',
                xytext=(0.8, 0.95), textcoords='figure fraction')
                        
#Prints my data if necessary
            if self.flag_pdata == True:
                nrows_series = temp_array_date.shape[0]
                keys = list(rel_table.keys())
                for i in keys:
                    key_from_rch = rel_table[i]
                    if key_from_rch in rch_filter:
                        series = mydata[i]
                        series_array = series.values
                        nrows_mydata = series_array.shape[0]
                    
                        if nrows_mydata == nrows_series:
                            plt.plot(temp_array_date, series_array,
     dashes = [6,2],lw = 0.6, label = r"%s"%(i), color = 'red', alpha = 0.8)
                        else: 
                            error_rows = series_array.shape[0]
                        print("Your series %s has %.0d rows and it should \
                              have %.0f rows.\
                        You will have a problematic execution, but Matoplotlib\
                        will carry on" %(i,error_rows,nrows_series))
#Puts grid and saves figure 
            plt.grid()
            plt.savefig('%s.png'%var, dpi = 200)        
            #plt.show()
        print('Finished!')
            
        def print_many_infolder(self):
        #Single parameters
        #Multiple parameters
            a = 2

class output_hru:

    def __init__(self,output_hru_fileadress,subbasin = 'all', lulc = 'all', 
                 hru_range = 'all',get_output = 'all'):
    
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
                print("""Your get_output parameter has problems.It takes either 
                      'all' or an integer list""")
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
        first_line_coln = [range(len_line_first)]
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
        final_array = np.vstack((header_array_sorted,
                                 data_indexed_array_sorted))
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

#################################### OUTPUT FOR SIMULATION ARRAY #########################    

class output_simarray:
    
    def __init__(self,simarray_address):
        
        self.simarray_address = simarray_address
        self.array = np.loadtxt(simarray_address, dtype = str)

        
    def print_allinone(self, figoutput, figsize = (26,18), observed=None,
                       rel_table=None, xlim=None, ylim=None):
        
        print('Printing simulation results all in one...')
        array = self.array
        
        flag_pdata = False
        
        if observed != None:
            if rel_table != None:
                flag_pdata = True
                my_data = pd.read_csv(observed, delimiter=',',
                                      index_col = "Datetime")
            else:
                print('Please input a relational table as well!')
                exit()
        elif observed == None:
                flag_pdata = False
                
        else:
            print('Error! insert appropriate csv observer data!...Exiting')
            exit()
                    
        header = array[0,:].T
        rch_column = np.where(header == 'RCH')[0][0]
        gday_column = np.where(header == 'GDAY')[0][0]
        rches = np.unique(array[2:,rch_column])
        
        countdown = 3
        fig = plt.figure(figsize = figsize)
        counter = 0
        useful_columns = list(range(2,array.shape[1]))
        colors = ['#e95b4f', 'red', '#001871','blue','#7B0099','red', 'cyan', 
                  'green', 'black', 'gray']
        lws = [2.6, 2.6, 1.9, 1.9]
        ltp = ['-','-','-.','-.','-','-']
        #colors = np.linspace(0,255,len(rches) * (len(useful_columns)),dtype = int)
        for n in useful_columns:
            for rch in sorted(rches):
                temp_array = array[array[:,rch_column] == rch]
                
                temp_array_rch_filtered= temp_array[:,n]
                temp_array_rch_filtered = temp_array_rch_filtered.astype(float)
                
                temp_array_date = temp_array[:,gday_column]
                temp_array_date = temp_array_date.astype(float)
                
                plt.plot(temp_array_date, temp_array_rch_filtered, lw = 1.5,
                         label = r"Rch # %s"%(rch), 
                         color = colors[counter], alpha = 1, linestyle = '-')
                         
                counter = counter+1
        plt.title('Simulated variables', fontsize=24)
        if xlim == None:
            plt.xlim(0, len(temp_array_date))
        if xlim != None:
            plt.xlim(xlim)
        if ylim == None:
            plt.ylim()
        if ylim != None:
            plt.xlim(ylim)
        plt.xlabel('Simulation days', fontsize=20)
        plt.ylabel('%s'%header[2], fontsize=18)
        plt.tick_params(axis='both', which='major', labelsize=20)
        plt.tick_params(axis='both', which='minor', labelsize=20)
        plt.legend(fontsize=18)
        plt.tight_layout()
            

                
#Calculates NS from series if in dictionary and in myfiles

#########REMOVED SPOT - PLACEHOLDER IN CAUSE YOU DECIDE TO RE-INSERT THE NS ##############################

#CREATE ANNOTATION ON PLOT 
#########REMOVED SPOT - PLACEHOLDER IN CAUSE YOU DECIDE TO RE-INSERT THE NS ##############################
                    
#Prints my data if necessary
                
        if flag_pdata == True:
            
            rch_list_int = []
            keys = list(rel_table.keys())
            values = list(rel_table.values())
            nrows_series = temp_array_date.shape[0]
            
            for u in rches:
                rch_list_int.append(int(float(u)))
            
            rch_list_int = sorted(rch_list_int)               
            for i in keys:
                
                key_from_rch = rel_table[i]  
                #key_from_rch = "%.1f" % (key_from_rch)

                if key_from_rch in rch_list_int:
                    index = rch_list_int.index(key_from_rch)
                    index_to_get = keys[index]
                    series = my_data[index_to_get]
                    series_array = series.values
                    nrows_mydata = series_array.shape[0]
                    
                    if nrows_mydata == nrows_series:
                        plt.plot(temp_array_date, series_array, dashes = [6,2],lw = 1.0, label = r"%s"%(i), color = 'blue', alpha = 0.8)
                    else: 
                        error_rows = series_array.shape[0]
                        print("Your series %s has %.0d rows and it should have %.0f rows.\
                        You will have a problematic execution, but Matoplit lib will carry on" %(i,error_rows,nrows_series))
#Puts grid and saves figure 
        plt.grid()
        plt.savefig(figoutput, dpi = 200)        
        plt.show()
    print('Finished!')

####CODE EXECUTION EXAMPLES

#hru_file = r'C:\Barigui\SwatBarigui6\Scenarios\Default\TxtInOut\output.hru'
#instance = output_hru(hru_file)
#table = instance.read_hru()
       
#observed = r'D:\OneDrive\Planilha-mestra_geral_v2_test.csv'
#rel_table = {"tmd":39, "stq":98, "cax":155}
#fileadress = r'C:\Barigui\SwatBarigui8\Scenarios\Default\TxtInOut\output.rch'
#instance_go = output_rch(fileadress,[39],["FLOW_OUTcms"],observed_input = observed, rel_table = rel_table)
#array = instance_go.read_rch()
#instance_go.print_allinone(array,figsize=(20,10))
