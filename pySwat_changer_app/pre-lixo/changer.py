# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 21:25:42 2018

@author: david
"""

import os 
import dic 
import listtype

def getlib():
    """Shows the programs dictionaries to files"""
    
def swat_parc(TXTInOut, parameter, method, sb, lulc, value):
    print("Starting...")
#Locates the file extension and line number in a dictionary
    instance = dic.param_dic()
    target_file, linenumber = instance.dic_query(parameter)
#gets a filelist for the specificed folder and format 
    soil_filenumber = len(listtype.listtype(TXTInOut,".sol"))
    sub_filenumber = len(listtype.listtype(TXTInOut,".sub"))-1 #minus 1: output.sub
    print ("You have %.0f hrus and %.0f subbasins this project" %
           (soil_filenumber,sub_filenumber))
    
    filelist = listtype.listtype(TXTInOut,target_file)
#Uses the fetched list to change values 
    total_files = len(filelist)
    files_done = 0
    for filename in filelist:
              
        adress = os.path.join(input_folder, filename)
        openfile = open(adress, 'r')
        parser = openfile.readlines()
        try:
            line = parser[linenumber]
            openfile.close()
        except:
            print 'Your file %s has problems' % filename
            exit()
#Information reader 
        FirstLine = parser[0]    
        firstline_read_single_list = list(FirstLine)
        
        SubBasinPos = FirstLine.find('Subbasin:')
        SubBasinStart = SubBasinPos + 9
        
        HRUPos = FirstLine.find('HRU:',26)
        SubBasinEnd = HRUPos + -1
        
        
        LULCPos = FirstLine.find('Luse:')
        LULCStart = FirstLine.find('Luse:')+5
        LULCEnd = LULCStart + 3
        LULC_scan = firstline_read_single_list[LULCStart:LULCEnd+1]
        LULC_type = ''.join(LULC_scan)
        
        sub_number = firstline_read_single_list[SubBasinStart:SubBasinEnd+1]
        
        sub_number = ''.join(sub_number)
        sub_number = int(sub_number)

        if lulc == 'all' and sb == sub_number or lulc == LULC_type and sb == 'all' or lulc == 'all' and sb == 'all' or lulc == LULC_type and sb == File_sub_number :
#Get file number 

#replace method        
            if method == 'replace':
           
                float_replace = float(value)
                str_replace = '%.3f' % float_replace
                list_replace = list(str_replace)
                #Position calculator     
                list_line = list(line)
                first_position = 16 - len(list_replace)
                
                for i in range(16):
                    list_line[i] = ' '
                j = 0
                
                for k in range(first_position, 16):
                    list_line[k+1] = list_replace[j]
                    j +=1

                list_line_to_str = ''.join(list_line)
                parser[linenumber] = list_line_to_str
        
                spamwriter = open(adress, 'w')
                for linha in parser:
                    spamwriter.write(linha)
                spamwriter.close()
                files_done +=1
                if files_done % 25 == 0:
                    print '%.0f' % files_done," files done        \r"
                    
#relative method  
            elif method == 'relative':
                str_value = line[0:16]
                value_rel = float(str_value)
                new_value = value_rel * (1+ value )
                    
                str_replace = '%.3f' % new_value
                list_replace = list(str_replace)
                #Position calculator     
                line = parser[linenumber]
                list_line = list(line)
                first_position = 16 - len(list_replace)+1
                
                for i in range(20): #clears all spaces in line as list from file
                    list_line[i] = ' ' 
                j = 0
                for k in range(first_position-1, 16):
                    list_line[k] = list_replace[j]
                    j +=1

                list_line_to_str = ''.join(list_line)
                parser[linenumber] = list_line_to_str
        
                spamwriter = open(adress, 'w')
                for linha in parser:
                    spamwriter.write(linha)
                spamwriter.close()  
                files_done +=1
                if files_done % 25 == 0:
                    print '%.0f' % files_done," files done         \r"
                   
    print 'Program complete!. %.0f files altered in a total of %.0f' %(files_done,total_files)
            
par = 'CN2'
input_folder = r"D:\Barigui_cal4\TxtInOut"
val = 0.2

swat_parc(TXTInOut = input_folder, parameter = par, method = 'relative', sb = 1, lulc='all', value = val )

#def par_rep(TXTInOut, parameter, sb, lulc):
    #Locates the file extension and line number in a dictionary
    #format_filter, linenumber = dic.dic(parameter)
    #filelist = listtype.listtype(TXTInOut,format_filter)
    #total_files = len(filelist)
    #files_done = 0
    #for filename in filelist: