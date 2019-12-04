# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 21:25:42 2018

@author: david
"""

import os 
import dic_par 
import listtype
import datetime
from distutils.dir_util import copy_tree
class par_handler:
    
    def __init__(self,TXTInOut):
    
        self.TXTInOut = TXTInOut
        
    def inforeader(self, parser):
#Information reader 
        FirstLine = parser[0]    
        firstline_read_single_list = list(FirstLine)
        check_sub = FirstLine.find("sub")
        check_rte = FirstLine.find("rte")
        
        if check_sub != -1 or check_rte != -1:
            HRU_number = None
            LULC_type = None
            FirstLineSplit = FirstLine.split()
            SubBasinPos = FirstLineSplit.index('Subbasin:')
            sub_number = int(FirstLineSplit[SubBasinPos+1])
            
            return LULC_type, sub_number,HRU_number
            
        else:
            SubBasinPos = FirstLine.find('Subbasin:')
            SubBasinStart = SubBasinPos + 9
            
            HRUPos = FirstLine.find('HRU:',26)
            SubBasinEnd = HRUPos + -1
            
            
            LULCPos = FirstLine.find('Luse:')
            LULCStart = LULCPos+5
            LULCEnd = LULCStart + 3
            LULC_scan = firstline_read_single_list[LULCStart:LULCEnd+1]
            LULC_type = ''.join(LULC_scan)
            
            
            sub_number = firstline_read_single_list[SubBasinStart:SubBasinEnd+1]
            
            sub_number = ''.join(sub_number)
            sub_number = int(sub_number)
            
            HRU_abs_Pos = FirstLine.find('HRU:')
            HRU_abs_Start = HRU_abs_Pos+4
            HRU_abs_End = SubBasinPos-1
            HRU_scan = firstline_read_single_list[HRU_abs_Start:HRU_abs_End+1]
            HRU_scan = ''.join(HRU_scan)
            HRU_number = HRU_scan.replace(" ", "")
            HRU_number = int(HRU_number)
            
            return LULC_type, sub_number,HRU_number

        
    def change(self, parameter, method, value, sb = 'all' , lulc = 'all', hru = None):
        
        def log_end(parameter,method,value,files_done,total_files):
            print("Writing to log file...")
            if os.path.isfile("log.txt") == True:
                openfile = open("log.txt", 'r')
                lines = openfile.readlines()
                len_lines = len(lines)
                openfile.close()
        
                timenow = datetime.datetime.now()
                line_to_append = ("\n"+ str([len_lines,parameter,method,value,timenow]))
        
                spamwriter = open('log.txt', 'a+')
                spamwriter.write(line_to_append)
                spamwriter.close()  

            else:
                choice = raw_input("You don't have a logfile. Do you want to create one? [y/n]: ")
                if choice == "y":
                    spamwriter = open("log.txt", 'w')
                    timenow = datetime.datetime.now()
                    spamwriter.write(str([0,parameter,method,value,timenow]))
                    spamwriter.close()  
                    if choice == "n":
                        pass
                        print("Warning! You did not print this change to the log!")
            print ('Program complete! -> %.0f files altered in a total of %.0f' %(files_done,total_files))
        
        print("Starting...")
#Locates the file extension and line number in a dictionary
        instance = dic_par.param_dic()
        target_file, linenumber, exceptions = instance.dic_query(parameter)
#gets a filelist for the specificed folder and format 
        soil_filenumber = len(listtype.listtype(self.TXTInOut,".sol"))
        sub_filenumber = len(listtype.listtype(self.TXTInOut,".sub"))-1 #minus 1: output.sub
        print ("You have %.0f hrus and %.0f subbasins this project" %
               (soil_filenumber,sub_filenumber))
        
        filelist = listtype.listtype(self.TXTInOut,target_file)       
#Uses the fetched list to change values 
        total_files = len(filelist)
        files_done = 0
        
        for exception in exceptions:
            flag = exception in filelist
            if flag == True:#checks if output file has indeed been printed
                index_exception = filelist.index(exception)
                del filelist[index_exception]
#####Routine for sol files      ####
        if target_file == '.sol':
            for filename in filelist:
                address = os.path.join(self.TXTInOut, filename)
                openfile = open(address, 'r')
                parser = openfile.readlines()
                LULC_type, sub_number, hru_number = self.inforeader(parser)                
                       
                if hru == None and lulc == 'all'and (sb == sub_number or sub_number in sb)\
                or hru == None and (lulc == LULC_type or LULC_type in lulc) and sb == 'all'\
                or hru == None and (lulc == 'all' and sb == 'all')\
                or (hru == None and lulc == LULC_type and sb == sub_number)\
                or (hru != None and type(hru) == int and  hru_number == hru)\
                or (hru != None and type(hru) == list and (hru_number in hru or hru_number == hru)):
                
                    try:
                        line = parser[linenumber]
                        openfile.close()
                    except:
                        print ('Your file %s has problems') % filename
                        exit()
                        
                    linesplit = line.split()
                    #linesplit_data_str = linesplit[3:]
                    list_line = list(line)
                    linesplit_data = linesplit[3:]
                    for i in range(len(linesplit_data)):
                        linesplit_data[i] = float(linesplit_data[i])
#Replace
                    if method == 'replace':
                        print('Dont redo replace in soil files, you will screw your model! Exiting program!')
                        break
                        exit()
#Relative
                    if method == 'relative':
#Gets a parameter list from the backup folder
                        folder_backup = os.path.join(self.TXTInOut, 'Backup')
                        address_backup = os.path.join(folder_backup, filename)
                        
                        if os.path.isdir(folder_backup) == False:
                            os.makedirs(address_backup)
                            copy_tree(address, address_backup)  
                        elif os.path.isdir(folder_backup) == True:  
                            
                            openfile_bkp = open(address_backup, 'r')
                            parser_bkp = openfile_bkp.readlines()
                            openfile_bkp.close()
                            try:
                               line_bkp = parser_bkp[linenumber]
                               linesplit_bkp = line_bkp.split()
                               linesplit_data_str_bkp = linesplit_bkp[3:]
                               linesplit_data_bkp = linesplit[3:]
                                    
                            except:
                                 print("Your file %s has problems" %address_backup)
#Multiplies all values in list by the desired value
                            for i in range(len(list(linesplit_data_bkp))):
                               linesplit_data_bkp[i] = (float(linesplit_data_bkp[i]))*(1+value)   
#Finds the end and beggining of string
                            for k in range(len(linesplit_data_bkp)):
                                end = 38 + 12* k
                                start = end - len(str(linesplit_data_str_bkp[k]))+1
#Replaces the string positions        
                                for j in range(start,end+1):
                                    list_line[j] = ''
                                string = '%.3f'%(linesplit_data_bkp[k])
                                startwrite = end - len(string)+1
                                #spaces = len(string) # Variable inspection
                                list_line[startwrite:end+1] = list(string)
                            list_line.insert(39, '')
                            list_line = ''.join(list_line)
                            parser[linenumber] = list_line
#Writes output file            
                            spamwriter = open(address, 'w')
                            for line in parser:
                                spamwriter.write(line)
                            spamwriter.close()  
                            files_done +=1
            log_end(parameter,method,value,files_done,total_files)
#####Routine for non-sol files####
        elif target_file != '.sol':
#Open file 
            for filename in filelist:
                address = os.path.join(self.TXTInOut, filename)
                openfile = open(address, 'r')
                parser = openfile.readlines()
                LULC_type, sub_number, hru_number = self.inforeader(parser)

#Routine for rte or sub files 
                if target_file == '.rte' or target_file == '.sub':
                    
                    if sub_number == sb or sub_number in sb:
                        
                        try:
                            line = parser[linenumber]
                            openfile.close()
                        except:
                            print ('Your file %s has problems') % filename
                            exit()
                    
                        if method == 'replace':
               
                            float_replace = float(value)
                            str_replace = '%.3f' % float_replace
                            list_replace = list(str_replace)
#Position calculator     
                            list_line = list(line)
                            list_other_line = list(parser[4])
                            first_position = 15 - len(list_replace)+1
                            
                            for i in range(16):
                                list_line[i] = ' '
    
                            list_line[first_position:16] = list_replace
    
                            list_line_to_str = ''.join(list_line)
                            parser[linenumber] = list_line_to_str
                    
                            spamwriter = open(address, 'w')
                            for linha in parser:
                                spamwriter.write(linha)
                            spamwriter.close()
                            files_done +=1
#relative method  
                        elif method == 'relative':
                    
#Parses the File in the Backup folder for value
                            folder_backup = os.path.join(self.TXTInOut, 'Backup')
                            address_backup = os.path.join(folder_backup, filename)
                            
                            if os.path.isdir(folder_backup) == False:
                                os.makedirs(address_backup)
                                copy_tree(address, address_backup)  
                            elif os.path.isdir(folder_backup) == True:  
                                
                                openfile = open(address_backup, 'r')
                                parser = openfile.readlines()
                                try:
                                    line_bkp = parser[linenumber]
                                    par_orig_value = line_bkp[:16]
                                    par_orig_value = float(par_orig_value)
                                    if par_orig_value == 0:
                                        print("Your file file %s has a starting value for %s of zero. Please check\
                                              for relative references"%(filename, parameter))
                                    par_new_value = par_orig_value * (1+value)
                                    openfile.close()
                                except:
                                    print ('Your file %s has problems') % filename
                                    exit()
#Replaces the parameter with a new calculated value
                                str_replace = '%.3f' % par_new_value
                                list_replace = list(str_replace)
#Position calculator     
                                line = parser[linenumber]
                                list_line = list(line)
                                first_position = 16 - len(list_replace)+1
                    
#Clears all spaces in line as list from file
                                for i in range(20): 
                                    list_line[i] = ' ' 
                                j = 0
                                for k in range(first_position-1, 16):
                                    list_line[k] = list_replace[j]
                                    j +=1
                
                                list_line_to_str = ''.join(list_line)
                                parser[linenumber] = list_line_to_str
                        
                                spamwriter = open(address, 'w')
                                for linha in parser:
                                    spamwriter.write(linha)
                                spamwriter.close()  
                                files_done +=1
                else:#CHECKER FOR NON SUBBASIN FILES
#Condition checker
                    if hru == None and lulc == 'all'and (sb == sub_number or sub_number in sb)\
                    or hru == None and (lulc == LULC_type or LULC_type in lulc) and sb == 'all'\
                    or hru == None and (lulc == 'all' and sb == 'all')\
                    or (hru == None and lulc == LULC_type and sb == sub_number)\
                    or (hru != None and type(hru) == int and  hru_number == hru)\
                    or (hru != None and type(hru) == list and (hru_number in hru or hru_number == hru)):
                    
            
                        try:
                            line = parser[linenumber]
                            openfile.close()
                        except:
                            print ('Your file %s has problems') % filename
                            exit()
#replace method        
                        if method == 'replace':
               
                            float_replace = float(value)
                            str_replace = '%.3f' % float_replace
                            list_replace = list(str_replace)
#Position calculator     
                            list_line = list(line)
                            list_other_line = list(parser[4])
                            first_position = 15 - len(list_replace)+1
                            
                            for i in range(16):
                                list_line[i] = ' '
    
                            list_line[first_position:16] = list_replace
    
                            list_line_to_str = ''.join(list_line)
                            parser[linenumber] = list_line_to_str
                    
                            spamwriter = open(address, 'w')
                            for linha in parser:
                                spamwriter.write(linha)
                            spamwriter.close()
                            files_done +=1
                        
#relative method  
                        elif method == 'relative':
                    
#Parses the File in the Backup folder for value
                            folder_backup = os.path.join(self.TXTInOut, 'Backup')
                            address_backup = os.path.join(folder_backup, filename)
                            
                            if os.path.isdir(folder_backup) == False:
                                os.makedirs(address_backup)
                                copy_tree(address, address_backup)  
                            elif os.path.isdir(folder_backup) == True:  
                                
                                openfile = open(address_backup, 'r')
                                parser = openfile.readlines()
                                try:
                                    line_bkp = parser[linenumber]
                                    par_orig_value = line_bkp[:16]
                                    par_orig_value = float(par_orig_value)
                                    par_new_value = par_orig_value * (1+value)
                                    openfile.close()
                                except:
                                    print ('Your file %s has problems') % filename
                                    exit()
#Replaces the parameter with a new calculated value
                                str_replace = '%.3f' % par_new_value
                                list_replace = list(str_replace)
#Position calculator     
                                line = parser[linenumber]
                                list_line = list(line)
                                first_position = 16 - len(list_replace)+1
                    
#Clears all spaces in line as list from file
                                for i in range(20): 
                                    list_line[i] = ' ' 
                                j = 0
                                for k in range(first_position-1, 16):
                                    list_line[k] = list_replace[j]
                                    j +=1
                
                                list_line_to_str = ''.join(list_line)
                                parser[linenumber] = list_line_to_str
                        
                                spamwriter = open(address, 'w')
                                for linha in parser:
                                    spamwriter.write(linha)
                                spamwriter.close()  
                                files_done +=1
            log_end(parameter,method,value,files_done,total_files)
                                
"""
        
    def undo(specifics):
        #LAST, A NUMBER, ALL
        if specifics == 'last':
            b=2
        
        elif (specifics) == 'all':
            b=2
        elif type(specifics) == list:
            b=2
        elif type(specifics) == int:
            b=2

"""
                       
#TXTInOut = r"D:\Default_test_python\TxtInOut"
#instance = par_handler(TXTInOut)
#instance.change(parameter = 'CN2', method = 'relative', sb= 1, lulc = 'all', value = 0.2)
#instance.change(parameter = 'GWQMN', method = 'replace', value = 3, sb= 'hru', lulc = 'hru', hru = list(range(1,15)))
