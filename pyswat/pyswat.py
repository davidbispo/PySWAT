# -*- coding: utf-8 -*-

class instance:
    
    def __init__(self,TxtInOut):
        self. TxtInOut = TxtInOut
              
        def change(self, parameter, method, value, sb = 'all' , lulc = 'all', hru = None, log= r'E:\log.txt'):
            
            import os
            import dic_par 
            from assets import dic_par
            from assets import lisstype
            from distutils.dir_util import copy_tree
            
            
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
            
            def log_end(parameter,method,value,files_done,total_files):
                print("Writing to log file...")
                if os.path.isfile(log) == True:
                    openfile = open(log, 'r')
                    lines = openfile.readlines()
                    len_lines = len(lines)
                    openfile.close()
            
                    timenow = datetime.datetime.now()
                    line_to_append = ("\n"+ str([len_lines,parameter,method,value,timenow]))
            
                    spamwriter = open(log, 'a+')
                    spamwriter.write(line_to_append)
                    spamwriter.close()  
    
                else:
                    choice = input("You don't have a logfile. Do you want to create one? [y/n]: ")
                    if choice == "y":
                        spamwriter = open(log, 'w')
                        timenow = datetime.datetime.now()
                        spamwriter.write(str([0,parameter,method,value,timenow]))
                        spamwriter.close()  
                        if choice == "n":
                            pass
                            print("Warning! You did not print this change to the log!")
                print ('Program complete! -> %.0f files altered in a total of %.0f' %(files_done,total_files))
                print ('You have successfully changed %s %s with a value of %s'%(parameter,method,value))
            print("###Starting parameter changer...")
#Locates the file extension and line number in a dictionary
           
    
    
#CHANGE MAIN CODE
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
                    try:
                        parser = openfile.readlines()
                        openfile.close()
                        LULC_type, sub_number, hru_number = self.inforeader(parser)   
                    except:
                        print ('Your file %s has problems') % filename
                        exit()
                           
                    if hru == None and lulc == 'all'and (sb == sub_number or sub_number in sb)\
                    or hru == None and (lulc == 'all') and (sb == 'all')\
                    or hru == None and (lulc == LULC_type or LULC_type in lulc) and sb == 'all'\
                    or hru == None and (lulc == LULC_type or LULC_type in lulc) and (sb == sub_number or sub_number in sb)\
                    or (hru != None and type(hru) == int and  hru_number == hru)\
                    or (hru != None and type(hru) == list and (hru_number in hru or hru_number == hru)):
                    
                        line = parser[linenumber]
    
                            
                        linesplit = line.split()
                        #linesplit_data_str = linesplit[3:]
                        list_line = list(line)
                        if parameter == 'SOL_AWC':
                            linesplit_data = linesplit[6:]
                        elif parameter == 'SOL_K':
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
                                print('Have a backup folder set up before starting')
                                exit()
                                #copy_tree(address, address_backup)  
                            elif os.path.isdir(folder_backup) == True:  
                                
                                openfile_bkp = open(address_backup, 'r')
                                parser_bkp = openfile_bkp.readlines()
                                openfile_bkp.close()
                                try:
                                   line_bkp = parser_bkp[linenumber]
                                   linesplit_bkp = line_bkp.split()
                                   if parameter == 'SOL_AWC':
                                       linesplit_data_bkp = linesplit_bkp[6:]
    
                                   elif parameter == 'SOL_K':
                                       linesplit_data_bkp = linesplit_bkp[3:]
                                        
                                except:
                                     print("Your file %s has problems" %address_backup)
    #Multiplies all values in list by the desired value
                                for i in range(len(list(linesplit_data_bkp))):
                                   linesplit_data_bkp[i] = (float(linesplit_data_bkp[i]))*(1+value)   
    #Finds the end and beggining of string
                                for k in range(len(linesplit_data_bkp)):
                                    end_old = 38 + 12* k
                                    start_old = end_old - len(str(linesplit_data[k]))+1
    #Replaces the string positions        
                                    for j in range(start_old,end_old+1):
                                        list_line[j] = ''
                                    end_new = end_old
                                    string = '%.3f'%(linesplit_data_bkp[k])
                                    startwrite = end_new - len(string)+1
                                    #spaces = len(string) # Variable inspection
                                    list_line[startwrite:end_new+1] = list(string)
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
                    openfile.close()
                    LULC_type, sub_number, hru_number = self.inforeader(parser)
    
    #Routine for rte or sub files 
                    if target_file == '.rte' or target_file == '.sub':
                        
                        if sub_number == sb or sub_number in sb:
                            
                            try:
                                line = parser[linenumber]
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
                                if parameter == 'CH_N1' or parameter == parameter == 'ALPHA_BNK' or parameter=='CH_K2':
                                    list_line_to_str = list_line_to_str.replace(" ", "", 2)
                                    list_line_to_str = list_line_to_str.replace("|", " |", 1)
                                    list_line_to_str = list_line_to_str.replace("|", " |", 1)
                                    
                                elif parameter == 'CH_N2':
                                    a=2
                                
                                parser[linenumber] = list_line_to_str
                                spamwriter = open(address, 'w')
                                for linhe in parser:
                                    spamwriter.write(linhe)
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
                                    
                                    if parameter == 'CH_N2':
                                        first_position = 14 - len(list_replace)+1
                                        final_position = 14
                                    else:
                                        first_position = 16 - len(list_replace)+1
                                        final_position = 16
    #Clears all spaces in line as list from file
                                    
                                    if parameter == 'CH_N2':
                                        erase=17
                                    else:
                                        erase=20
                                    for i in range(erase): 
                                        list_line[i] = ' ' 
                                    j = 0
                                    
                                    for k in range(first_position-1, final_position):
                                        list_line[k] = list_replace[j]
                                        j +=1
                    
                                    list_line_to_str = ''.join(list_line)
                                    parser[linenumber] = list_line_to_str
                            
                                    spamwriter = open(address, 'w')
                                    for linesa in parser:
                                        spamwriter.write(linesa)
                                    spamwriter.close()  
                                    files_done +=1
                    else:#CHECKER FOR NON SUBBASIN FILES
    #Condition checker
                        if hru == None and lulc == 'all' and (str(sb) == str(sub_number) or type(sb) == list and sub_number in sb)\
                        or hru == None and (lulc == 'all') and (sb == 'all')\
                        or hru == None and (lulc == LULC_type or LULC_type in lulc) and sb == 'all'\
                        or hru == None and (lulc == LULC_type or LULC_type in lulc) and (str(sb) == str(sub_number) or sub_number in sb)\
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
                                for line_unit in parser:
                                    spamwriter.write(line_unit)
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
                                    try:
                                        openfile = open(address_backup, 'r')
                                        parser_bkp = openfile.readlines()
                                        openfile.close()
                                    except:
                                        print ('Your backup file %s has problems and could not be opened') % filename
                                        exit()
                                    try:
                                        line_bkp = parser_bkp[linenumber]
                                        par_orig_value = line_bkp[:16]
                                        par_orig_value = float(par_orig_value)
                                        par_new_value = par_orig_value * (1+value)
        
                                    except:
                                        print ('The parsing operation on file %  could not be performed') % filename
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
                                    for line_units in parser:
                                        spamwriter.write(line_units)
                                    spamwriter.close()  
                                    files_done +=1
            log_end(parameter,method,value,files_done,total_files)
        
            """                                
TXTInOut = r'D:\TxtInOut'     
instance = par_handler(TXTInOut)
fileadress = os.path.join(TXTInOut,'output.rch')
variables = ["FLOW_OUTcms"]
observed = r'D:\OneDrive\Planilha-mestra_geral_v2_test.csv'
rel_table = {"tmd":39, "stq":98, "cax":155}

#instance.change(parameter = 'CN2', method = 'relative', value = -0.083233, sb=1)#1
#instance.change(parameter = 'CN2', method = 'relative', value = -0.083233, sb=list(range(1,40)),log = 'D:\log.txt')
"""
        
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
        
        


        def get_par_hru(sb=all, lulc=all):
                    
            import numpy as np 
            import dic_par #importing the dictionary code
            import listtype
            import os
                
                
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

    
    
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################
                
        class output_parser:
        
            def __init__(self):
            
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
            
            def getns():
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

            
            
            def read_rch():
            
                
                """Takes an output.rch file and parses it for reach number and desired parameters
                fileadress = the file address as string
                rch_filter = takes integer, list of integers and 'all' as arguments
                par_silter = takes string, list of strings and 'all' as arguments
                observed_input = Numpy array with header: "GDAY", "STATION1_FLOW", "STATION2_FLOW", ..."STATIONn_FLOW"
                rel_table = nx2 array with first collumn "RCH_NUMBER", "STATION NAME"
            
                returns numpy array 
                
                Methods: read_rch(), print_allinone(output_folder), print_manyinfolder(output_folder)
                """
                
                import numpy as np
                import datetime
                import matplotlib.pyplot as plt
                
            #Function local parameter definition        
                rch_filter = self.rch_filter
                par_filter = self.par_filter
                observed_input = self.observed_input 
                rel_table = self.rel_table
            #Reads personal data 
                if observed_input != None and rel_table != None:
                    my_data = pd.read_csv(observed_input, delimiter=',',index_col = "GDAY")
                    flag_pdata = True            
                else:
                    print("Please input both observed inputs and relational tables correctly!")
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
                result_array = np.array(result_list_parse1) #Creates array from only data array 
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
                        result_array_filtered=result_array[result_array[:,rch_address] == str(rch_filter)]
                    elif type(rch_filter) == list :
                        for k in rch_filter:
                            if k == rch_filter[0]:
                                array_filtered = result_array[result_array[:,rch_address] == str(k)]
                            else:
                                array_filtered_temp = result_array[result_array[:,rch_address] == str(k)]
                                array_filtered = np.vstack((array_filtered,array_filtered_temp))
                        
                        result_array_filtered = array_filtered
                    
                    if ("MO") in header:        
                        
                        dayArray = result_array_filtered[:,day_address]
                        monthArray = result_array_filtered[:,mo_address]
                        yearArray = result_array_filtered[:,year_address]
                        
                        date_zero = (datetime.date(int(yearArray[0]),int(monthArray[0]),int(dayArray[0])))
                        gdays = []
                        date_list = []
                        date_list_string = []
                        
                        for i in range(result_array_filtered.shape[0]):
                            date_temp = (datetime.date(int(yearArray[i]),int(monthArray[i]),int(dayArray[i])))
                            gdays.append((date_temp - date_zero).days)
                            date_list.append(date_temp)
                            date_list_string.append(date_temp.strftime('%m/%d/%Y'))
                        
                        date_array = np.array(gdays)
                        days_sim = date_array
                        result_array_filtered = np.insert(result_array_filtered,2,days_sim,axis = 1) #inserts gday simday array
                        header.insert(2,"SDG") #inserts on the header the Simulation Gregorian days Collumn header
                    
                    else:
                        gdays = list(range(1,result_array_filtered.shape[0]+1))
                        date_array = np.array(gdays)
                        days_sim = date_array
                        result_array_filtered = np.insert(result_array_filtered,2,days_sim,axis = 1) #inserts gday simday array
                        header.insert(2,"SDG") #inserts on the header the Simulation Gregorian days Collumn header
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
            #Parses and filters the par_filter parameter - Takes string, list of strings as parameters and 'all'
                    if par_filter != 'all':
                        if type(par_filter) == list:
                            for i in par_filter:
                                col_interest = header.index(i) #Fetches the parameter filter as a collumn number
                                col_index_list.append(col_interest)
                        if type(par_filter) == str:
                            col_interest = header.index(par_filter)#Fetches the parameter filter as multiple collumn numbers
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
                
                
                def print_allinone(array, figsize):
                    rch_filter = rch_filter
                    rel_table = rel_table
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
                            plt.plot(temp_array_date, temp_array_var, lw = 0.7, label = r"Rch # %s"%(rch), color = rgb, alpha = 0.9)
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
                                    
                                    o = mydata[list(rel_table.keys())[list(rel_table.values()).index(i)]].values
                                    
                                    mydata_length = o.shape[0]
                                    
                                    if expected_mydata_length != mydata_length:
                                        print('''The simulation has %.0f days. Your data has %.0f days. Please correct that. Please notices that text files with 
                                              empty values still count as cells, so check them!'''%(expected_mydata_length,mydata_length))
                                    
                                    eff_array = np.insert(s, 1, o, axis=1)
                                    eff_array = eff_array[~np.isnan(eff_array).any(axis=1)]
                                    ns = NS(eff_array[:,1],eff_array[:,2])
            #CREATE ANNOTATION ON PLOT 
                                    string_to_annotate += 'NS for station %s = %.3f \n'%(i,ns)
                            plt.annotate(string_to_annotate, xy=(0.80, 0.95),  xycoords='figure fraction',
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
                                        plt.plot(temp_array_date, series_array, dashes = [6,2],lw = 0.6, label = r"%s"%(i), color = 'red', alpha = 0.8)
                                    else: 
                                        error_rows = series_array.shape[0]
                                        print("Your series %s has %.0d rows and it should have %.0f rows.\
                                        You will have a problematic execution, but Matoplit lib will carry on" %(i,error_rows,nrows_series))
            #Puts grid and saves figure 
                        plt.grid()
                        plt.savefig('%s.png'%var, dpi = 200)        
                        #plt.show()
                    print('Finished!')
                        
                def print_many_infolder(self):
                #Single parameters
                #Multiple parameters
                    a = 2
            
            class read_hru:
            
                def __init__(self,output_hru_fileadress,subbasin = 'all', lulc = 'all', hru_range = 'all',get_output = 'all'):
                
                    self.fileadress = output_hru_fileadress
                    self.subasin = subbasin
                    self.lulc = lulc
                    self.hru_range = hru_range
                    self.get_output = get_output
                
                def print_hru(array):
                    p=2
            
                def read_hru(self):
                    
                    import numpy as np
                    
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
            
            #################################### OUTPUT FOR SIMULATION ARRAY #########################    
            
            class output_simarray:
                
                def __init__(self,simarray_address):
                    
                    import numpy as np
                    import pandas as pd                    
                    self.simarray_address = simarray_address
                    self.array = np.loadtxt(simarray_address, dtype = str)
            
                    
                def print_allinone(self, figoutput, figsize = (26,18), observed=None, rel_table=None, xlim=None, ylim=None):
                    
                    print('Printing simulation results all in one...')
                    array = self.array
                    
                    flag_pdata = False
                    
                    if observed != None:
                        if rel_table != None:
                            flag_pdata = True
                            my_data = pd.read_csv(observed, delimiter=',',index_col = "Datetime")
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
                    colors = ['#e95b4f', 'red', '#001871','blue','#7B0099','red', 'cyan', 'green', 'black', 'gray']
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
                            
                            plt.plot(temp_array_date, temp_array_rch_filtered, lw = 1.5, label = r"Rch # %s"%(rch), 
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
        
        
#hru_file = r'C:\Barigui\SwatBarigui6\Scenarios\Default\TxtInOut\output.hru'
#instance = output_hru(hru_file)
#table = instance.read_hru()
   
#observed = r'D:\OneDrive\Planilha-mestra_geral_v2_test.csv'
#rel_table = {"tmd":39, "stq":98, "cax":155}
#fileadress = r'C:\Barigui\SwatBarigui8\Scenarios\Default\TxtInOut\output.rch'
#instance_go = output_rch(fileadress,[39],["FLOW_OUTcms"],observed_input = observed, rel_table = rel_table)
#array = instance_go.read_rch()
#instance_go.print_allinone(array,figsize=(20,10))