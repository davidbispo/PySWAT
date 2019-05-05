# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 17:28:50 2018

@author: david
"""
import numpy as np 
import dic #importing the dictionary code
import listtype
import os

class swat_table:
    
    def __init__(self, TXTInOut,sb, lulc):
        self.TXTInOut,self.sb, self.lulc, = TXTInOut, sb, lulc
          
    def get_par_hru(self):
        
        dic_instance = dic.param_dic() #opening an instance of dic
        keys = dic_instance.dic_keys() # fetching the keys
        TXTInOut, sb, lulc = self.TXTInOut, self.sb, self.lulc
        
        print("Starting...")
 #gets a filelist for the specificed folder and format 
        soil_filenumber = len(listtype.listtype(TXTInOut,".sol"))
        sub_filenumber = len(listtype.listtype(TXTInOut,".sub"))-1 #minus 1: output.sub
        print ("You have %.0f hrus and %.0f subbasins this project" %
           (soil_filenumber,sub_filenumber))

        for k in keys:
            target_file,line,exceptions = dic_instance.dic_query(k)
            filelist = listtype.listtype(TXTInOut,target_file)
            
            for exception in exceptions:
               index_exception = filelist.index(exception)
               del filelist[index_exception]
            
            for i in filelist:
                
                adress = os.path.join(TXTInOut, i)
                openfile = open(adress, 'r')
                parser = openfile.readlines()
                
                FirstLine = parser[0]    
                firstline_read_single_list = list(FirstLine)
        
                SubBasinPos = FirstLine.find('Subbasin:')
                SubBasinStart = SubBasinPos + 9
        
                HRUPos = FirstLine.find('HRU:')
                HRU_Start = HRUPos+4
                HRU_End = SubBasinPos - 1
            
                HRU_number = firstline_read_single_list[HRU_Start:HRU_End+1]
                HRU_number = ''.join(HRU_number)
                HRU_number = int(HRU_number)
                #dummy = list(FirstLine)
                
                SecondHRUPos = FirstLine.find('HRU:',26)

                
                SubBasinEnd = SecondHRUPos + -1
                
                LULCStart = FirstLine.find('Luse:')+5
                LULCEnd = LULCStart + 3
                LULC_scan = firstline_read_single_list[LULCStart:LULCEnd+1]
                LULC_type = ''.join(LULC_scan)
                
                SecondHRU_Start = SecondHRUPos+4
                SecondHRU_End = FirstLine.find('Luse:') - 1
            
                SecondHRU_number = firstline_read_single_list[SecondHRU_Start:SecondHRU_End+1]
                SecondHRU_number = ''.join(SecondHRU_number)
                SecondHRU_number = int(SecondHRU_number)
        
                sub_number = firstline_read_single_list[SubBasinStart:SubBasinEnd+1]
            
                sub_number = ''.join(sub_number)
                sub_number = int(sub_number)
                
                #HRU_Area_line = parser[1]   
                #HRU_Area = HRU_Area_line[:16]
                #HRU_Area = float(HRU_Area)
                               
                if lulc == 'all' and sb == sub_number or lulc == LULC_type and sb == 'all' or lulc == 'all' and sb == 'all' or lulc == LULC_type and sb == sub_number :

                    parsed = parser[line]
                    parameter = list(parsed)
                    parameter = parameter[:16]
                    parameter = ''.join(parameter)
                    parameter = float(parameter)
                    openfile.close()
                                                
                    if k == keys[0]:
                            
                        if i == filelist[0]:
                            par_name = k
                            a = np.array(["LULC","Sub_number","HRU_Number_ABS", "HRU_Number_REL", par_name]).T
                            new_table = np.array([LULC_type,sub_number,HRU_number, SecondHRU_number, parameter])
                            a = np.vstack((a,new_table))
                        else:
                            new_table = np.array([LULC_type,sub_number,HRU_number, SecondHRU_number, parameter])
                            a = np.vstack((a,new_table))
                    else:
                        if i == filelist[0]:
                            par_name = k
                            array = np.array([par_name,parameter]).T
                                
                        elif i != filelist[0] and i != filelist[-1]:
                            array = np.append(array,parameter)
                        
                        elif i == filelist [-1] and k == keys[-1] :
                            array = np.append(array,parameter)
                            a = np.column_stack((a,array))
                            return a
                else:
                    if k == keys[-1] and i == filelist[-1]:
                        a = np.column_stack((a,array))
                        return a                
                    
par = 'CN2'
input_folder = r"C:\Barigui\SwatBarigui7\Scenarios\Default\TxtInOut"
v = swat_table(TXTInOut = input_folder, sb = 'all', lulc='all')
table = v.get_info_hru()
c=2