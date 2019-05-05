# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 17:28:50 2018

@author: david
"""


class swat_partable:
    import numpy as np 
    import dic_par #importing the dictionary code
    import listtype
    import os
    
    def __init__(self, TXTInOut,sb, lulc):
        self.TXTInOut,self.sb, self.lulc, = TXTInOut, sb, lulc
          
    def get_par_hru(self):
        
        dic_instance = dic_par.param_dic() #opening an instance of dic
        keys = dic_instance.dic_keys() # fetching the keys
        if 'SOL_K' in keys:
            x = keys.index('SOL_K')
            del keys[x]
        if 'CH_K1' in keys:
            x = keys.index('CH_K1')
            del keys[x]
        if 'ALPHA_BNK' in keys:
            x = keys.index('ALPHA_BNK')
            del keys[x]
        if 'CH_K2' in keys:
            x = keys.index('CH_K2')
            del keys[x]
        if 'SOL_AWC' in keys:
            x = keys.index('SOL_AWC')
            del keys[x]
        if 'CH_N2' in keys:
            x = keys.index('CH_N2')
            del keys[x]
            
        TXTInOut, sb, lulc = self.TXTInOut, self.sb, self.lulc
        
        print("Starting hru parameter fetcher...")
 #gets a filelist for the specificed folder and format 
        soil_filenumber = len(listtype.listtype(TXTInOut,".sol"))
        sub_filenumber = len(listtype.listtype(TXTInOut,".sub"))-1 #minus 1: output.sub
        print ("You have %.0f hrus and %.0f subbasins this project" %
           (soil_filenumber,sub_filenumber))
        
        for k in keys:
            target_file,line,exceptions = dic_instance.dic_query(k)
            filelist = listtype.listtype(TXTInOut,target_file)
            
            for exception in exceptions:
                flag = exception in filelist
                if flag == True:#checks if output file has indeed been printed
                    index_exception = filelist.index(exception)
                    del filelist[index_exception]
            
            for i in filelist:
                #gets the paramater data in file 
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
                try :
                    HRU_number = int(HRU_number)
                except:
                    print (('Failed to red HRU number on file %s, key %s') %(i, k))
                    exit()
                
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
                
                    
                    #inputs a single or all subbasins and lulcs        
                parsed = parser[line]
                parameter = list(parsed)
                parameter = parameter[:16]
                parameter = ''.join(parameter)
                try :
                    parameter = float(parameter)
                except:
                    print (('Failed to convert to float on file %s, key %s' %(i, k)))
                    exit()
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
                    
                    elif i == filelist [-1] and k != keys[-1] :
                        array = np.append(array,parameter)
                        a = np.column_stack((a,array))

                    elif i == filelist [-1] and k == keys[-1] :
                        array = np.append(array,parameter)
                        a = np.column_stack((a,array))
                        print("Concluido")
                    elif k == keys[-1] and i == filelist[-1]:
                        a = np.column_stack((a,array))
####Filters by land use and subbasin number
#Start - Gets data and filters in header and body
                        
        a_header = a[0,:].T
        a_body = a[1:,:]
        lulc_col = int(np.where(a_header == 'LULC')[0][0])
        sb_col = int(np.where(a_header == 'Sub_number')[0][0])
        
        if type(sb) == int:
            a_body = a_body[a_body[:,sb_col] == str(sb)]    
            
        elif type(sb) == list:
            for o in sb:
                if len(sb) == 1 and o == sb[0]:
                    a_body_filtered = a_body[a_body[:,sb_col] == str(o)]   
                    a_body = a_body_filtered
                elif len(sb) != 1 and o == sb[0]:
                    a_body_filtered = a_body[a_body[:,sb_col] == str(o)] 
                elif len(sb) != 1 and o != sb[0] and o != sb[-1]:
                    new_a_body_filtered = a_body[a_body[:,sb_col] == str(o)]   
                    a_body_filtered = np.vstack((a_body_filtered,new_a_body_filtered))
                elif len(sb) != 1 and o == sb[-1]:
                    new_a_body_filtered = a_body[a_body[:,sb_col] == str(o)]   
                    a_body_filtered = np.vstack((a_body_filtered,new_a_body_filtered))
                    a_body = a_body_filtered
                    
        elif sb == 'all':
            pass
        
        if type(lulc) == str and lulc != 'all':
            a_body = a_body[a_body[:,0] == str(lulc)]
        
        elif type(lulc) == list:
            for p in lulc:
                if p == lulc[0]:
                    a_body_filtered = a_body[a_body[:,lulc_col] == str(p)]   
                    if len(lulc) == 1:
                        a_body = a_body_filtered
                elif p != lulc[0] and p != lulc[-1]:
                    new_a_body_filtered = a_body[a_body[:,lulc_col] == str(p)]   
                    a_body_filtered = np.vstack((a_body_filtered,new_a_body_filtered))
                elif p == lulc[-1]:
                    new_a_body_filtered = a_body[a_body[:,lulc_col] == str(p)]   
                    a_body_filtered = np.vstack((a_body_filtered,new_a_body_filtered))
                    a_body = a_body_filtered
                            
        filtered_table = np.vstack((a_header,a_body))
        full_table = a
        return filtered_table, full_table
        print("Concluido!")
                                        
#input_folder = r'C:\Barigui_InfBasins\Scenarios\Altered\TxtInOut'
#instance = swat_partable(TXTInOut = input_folder, sb = 95, lulc='all')
#table, original_table = instance.get_par_hru()