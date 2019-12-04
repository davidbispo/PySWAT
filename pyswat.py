# -*- coding: utf-8 -*-
"""
PYSWAT
PySWAT is a Command Line Interface(CLI) 
for Input/Output manipulation and analysis 
of the Soil and Water Assessment Tool(SWAT)

version:0.5

Author: David Bispo Ferreira - Federal University of Parana
davidbispo@hotmail.com
"""

class connect:

    def __init__(self,TxtInOut):
        import os
        self.TxtInOut = TxtInOut
        os.chdir(self.TxtInOut)

    def progressBar(self,value, endvalue, bar_length=20): # Barra de progresso da escrita de arquivos
        import sys

        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\rPer cent done: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()

    def open_connection(self,output):
        import sqlite3
        import os
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        print("Opening Connection on SQLITE...")
        print("File:  %s" % output)

        try:
            conn = sqlite3.connect(os.path.join(os.getcwd(),output))
            print('Connection successful')
            return conn
        except Error as e:
            print(e)

    def run(self, swat_version="664_rel_64"):
        """
        Runs a connected swat model
        :swat_version => Release to run. Accepted values:
            '664_rel_32', '664_debug_32',
            '664_rel_64','664_debug_64,
            '670_rel_32','670_debug_32',
            '670_rel_64','670_debug_64'
        """
        import os
        import subprocess
        import shutil

        dic_versions = {
            '664_rel_32': 'rev664_32rel.exe',
            '664_debug_32': 'rev664_32debug.exe',
            '664_rel_64': 'rev664_64rel.exe',
            '664_debug_64': 'rev664_64debug.exe',

            '670_rel_32': 'rev670_32rel.exe',
            '670_debug_32': 'rev670_32debug.exe',
            '670_rel_64': 'rev670_64rel.exe',
            '670_debug_64': 'rev670_64debug.exe',
                }

        print("PySWAT - Run Cycle")
        print("Reading SWAT version...")

        try:
            swat_filename = dic_versions[swat_version]
            print("Ok")

        except:
            print("""Invalid SWAT Version! Please read the documentation.
                  Acceptable values are follow the '664_rel_32' (Release +
                  debug or release + bits of processor architecture""")
            exit()

        this_filedir = os.path.dirname(os.path.abspath(__file__))
        exec_dir = os.path.join(this_filedir,'swat_execs',swat_filename)
        shutil.copy2(exec_dir, os.getcwd())

        def execute(self,cmd):

            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
            for stdout_line in iter(popen.stdout.readline, ""):
                yield stdout_line
            popen.stdout.close()
            return_code = popen.wait()
            if return_code:
                raise subprocess.CalledProcessError(return_code, cmd)

        os.chdir(self.TxtInOut)
        print("Running Swat..")
        for path in execute(self,[swat_filename]):
            print(path, end="")

        if os.path.exists(os.path.join(self.TxtInOut,swat_filename)):
            os.remove(os.path.join(self.TxtInOut,swat_filename))
        else:
            print("Failed to remove SWAT executable from folder. Please remove it Manually and verify folder permisssions")
        print('Run Succesful!')


    def resultFile_toSQL(self, output="swat_db.sqlite", fetch_tables=['hru','rch']):
        """
        Creates a sqlite table in the same folder as TXTInOut
        :output => Output name for the database - Must end with .ssqlite,db3, or other SQLite extensions
        *Default -> swat_db.sqlite
        :fetch_tables => What tables should be fetched. Can be a string or a list with strings(e.g.: ['hru','rch'])
        *Acceptable values -> 'hru', 'sub', 'rch', 'all'
        *Default -> 'all'
        """
        import os
        import sys
        from sqlite3 import Error
        sys.path.insert(1,os.path.join(os.path.dirname(os.path.abspath(__file__))))#Add dic_par folder to path list
        from assets import dic_par #This method calls the parameter SQLITE types for input

        dic_output_files = {
        'hru': 'output.hru',
        'sub': 'output.sub',
        'rch': 'output.rch',
        'mgt': 'output.mgt',
        }

        def countLines(self,filename):
            def blocks(files, size=65536):
                while True:
                    b = files.read(size)
                    if not b: break
                    yield b

            with open(filename, "r") as f:
                k = sum(bl.count("\n") for bl in blocks(f))
                return k

        def createTableFromQuery(self,create_table_sql,tableName):
            """ create a table from the create_table_sql statement
            :param create_table_sql: a CREATE TABLE statement
            :return:
            """
            #Replacers for names not accepted by SQLITE -> CREATE***
            create_table_sql = create_table_sql.replace('#','_')
            create_table_sql = create_table_sql.replace('TOT Nkg','TOT_Nkg')
            create_table_sql = create_table_sql.replace('TOT Pkg','TOT_Pkg')
            create_table_sql = create_table_sql.replace('WTAB CLIm','WTAB_CLIm')
            create_table_sql = create_table_sql.replace('WTAB SOLm','WTAB_SOLm')
            create_table_sql = create_table_sql.replace('DOXQ mg/L','DOXQ_mg_L')
            create_table_sql = create_table_sql.replace('LAT Q(mm)','LAT_Q_mm')
            create_table_sql = create_table_sql.replace('CBODU mg/L','CBODU_mg_L')
            create_table_sql = create_table_sql.replace('/','_')
            create_table_sql = create_table_sql.replace('-','_')

            conn = self.open_connection(os.path.join(os.getcwd(),output))

            print("Creating table '%s'..." % tableName)
            try:
                c = conn.cursor()
                c.execute(create_table_sql)
            except Error as e:
                error = str(e)
                if 'already exists' in error:
                    try:
                        c.execute("DROP TABLE %s" % (tableName))
                        c.execute(create_table_sql)
                    except:
                        print("Error on creating tables. Table already exists and cannot be dropped")
                        exit()
            conn.close()
            print("Done!")

        def getVariablesInFile(self,filename,tableName):
            """
            Fetches whatever variables in file header. Compares with the known
            values and returns a list with them. Prevents NOT-SPACED variables
            in the SWAT output. It uses a parser at the make table and insertDataToTable
            scripts to fix the queries
            """
            instance = dic_par.Parameters(tableName)
            variables_in_file = []
            with open(filename) as infile:

                for line in infile:
                    if 'GIS ' in line:
                        variablesInFile = line
                        break
                for item in instance.relParameterDBType:
                    if item in variablesInFile:
                        variables_in_file.append(item)
                    else:
                        pass
            infile.close()
            return variables_in_file

        def makeTable(self, variablesInFile,tableName):
            """
            Code generates a query for constructing a table
            and calls the method to execute the query
            :Requires a dictionary with variable type
            """
            instance = dic_par.Parameters(tableName)
            to_append = {}
            column_list = []
            for i in variablesInFile:
                to_append[i] = instance.returnVariableDBType(i)
            for j in to_append.keys():
                column_list.append('%s %s NOT NULL,'%(j, to_append[j]))

            sql_base = """CREATE TABLE %s (
                                        id integer PRIMARY KEY,"""%(tableName)
            for q in column_list:
                if q == column_list[0]:
                   sql = sql_base + q
                else:
                   sql = sql + q
            sql = sql[0:-1]
            sql = sql + ')'

            createTableFromQuery(self,create_table_sql = sql, tableName=tableName)

        def parseQuery(self, variablesInFile, parameters):
            """
            Little Procedural code for fixing SQL Query Syntax to insert to DB
            """
            #Creates list of Parameters with the first being a string, not numeric
            string = ""
            if variablesInFile[0] == 'LULC':
                string = "'" + parameters[0] + "'" + ','
                for p in range(1, len(parameters)):
                    string = string + str(parameters[p]) + ','
                string = string[0:-1]
            else:
                for p in range(0, len(parameters)):
                    string = string + str(parameters[p]) + ','
                string = string[0:-1]
            return string

        def insertDataToDB(self, variablesInFile,filename, tableName):
            import time
            """
            Inserts values from text file to the Database
            """
            print("Inserting Files to Table %s" % tableName)
            print("Counting Lines...")
            nlines = countLines(self, os.path.join(self.TxtInOut,'output.%s' % item))
            print("File Has " + str(nlines) + " Lines")
            start = time. time()
            conn = self.open_connection(os.path.join(os.getcwd(),output))
            try:
                c = conn.cursor()
            except Error as e:
                print(e)
                exit()
            with open(r"output." + tableName) as infile:

                for _ in range(9):
                    next(infile)
                counter=0
                c.execute('BEGIN TRANSACTION')

                composed_variablesInFile = ''
                for i in variablesInFile:
                    composed_variablesInFile += i +','
                composed_variablesInFile = composed_variablesInFile[0:-1]
                print("\nStarting Insert to DB...It may take a long time...")
                print("***PLEASE DO NOT EXIT THE PROCESS*** \n \n")

                for line in infile:

                    splitted = line.split()

                    if splitted[0] == 'REACH' or splitted[0] == 'BIGSUB':
                        splitted = splitted[1:]
                    #Replacers for names not accepted by SQLITE -> INSERT***
                    composed_variablesInFile = composed_variablesInFile.replace('#','_')
                    composed_variablesInFile = composed_variablesInFile.replace('TOT Nkg','TOT_Nkg')
                    composed_variablesInFile = composed_variablesInFile.replace('TOT Pkg','TOT_Pkg')
                    composed_variablesInFile = composed_variablesInFile.replace('WTAB CLIm','WTAB_CLIm')
                    composed_variablesInFile = composed_variablesInFile.replace('WTAB SOLm','WTAB_SOLm')
                    composed_variablesInFile = composed_variablesInFile.replace('DOXQ mg/L','DOXQ_mg_L')
                    composed_variablesInFile = composed_variablesInFile.replace('LAT Q(mm)','LAT_Q_mm')
                    composed_variablesInFile = composed_variablesInFile.replace('CBODU mg/L','CBODU_mg_L')
                    composed_variablesInFile = composed_variablesInFile.replace('/','_')
                    composed_variablesInFile = composed_variablesInFile.replace('-','_')

                    sql_parvalues = parseQuery(self,variablesInFile, splitted)
                    sentence =  """INSERT INTO %s (%s)
                    VALUES(%s);"""% (tableName,composed_variablesInFile,sql_parvalues)

                    try:
                        c.execute(sentence)
                    except Error as e:
                        error = str(e)
                        print(error)
                        print("Error on line %s" % (counter))
                        print("TRACEBACK >>>>>>" % (counter,sentence))
                        print("Error while executing: \n %s" % (sentence))
                        exit()
                    counter+=1
                    self.progressBar(counter, nlines, bar_length=20)

                c.execute('COMMIT')
                conn.close()
                end = time. time()
                timelength = end - start
                print("\nData sucessfully transferred \n Time: %.3f seconds "%(timelength))

#Verifies the validity of list or string argument
        if type(fetch_tables) == list:
            for item in fetch_tables:
                if item in dic_output_files.keys():
                    pass
                else:
                    print("""You Have wrong keys on the fetch_table
                          argument. Correct that to continue.
                          Wrong Key: %s
                          """ %(item))
                    print("Program Terminated")
                    exit()

        elif type(fetch_tables) == str:
            if item in dic_output_files.keys():
                pass
            else:
                print("""You Have wrong keys on the fetch_table
                      argument. Correct that to continue.
                      Wrong Key: %s""" %(item))
                print("Program Terminated")
                exit()
        else:
            print("Wrong File type for argument fetch_table")
            print("Program Terminated")
            exit()

#Runs SWAT under String or List Arguments
        if type(fetch_tables) == list:
            for item in fetch_tables:
                variablesInFile  = getVariablesInFile(self, filename = os.path.join(self.TxtInOut,
                                   'output.%s' %(item)), tableName=item)

                print("Setting data on table " + item)
                makeTable(self,variablesInFile,item)
                #print("Counting Lines...")
                insertDataToDB(self,variablesInFile = variablesInFile,
                               filename = output,
                               tableName = item)
        else:
            print("Setting data on table " + fetch_tables)
            variablesInFile  = getVariablesInFile(output)
            makeTable(variablesInFile)
            insertDataToDB(variablesInFile,output,variablesInFile)

######################################################
    def getModelQuery(self,query,file="swat_db.sqlite", pandas_output=False):
        import os
        """
        Returns the results of a query on SQLITE
        :query -> Query Itself. Use of Docstrings is recommended
        :file -> FilePath of the Database
        :pandas_output -> bolean that returns result on pandas dataframe.
        Keep in mind Pandas does not allow large Tables
        """
        print("Opening Connection on SQLITE...")
        conn = self.open_connection(os.path.join(os.getcwd(),file))
        try:
            c = conn.cursor()
        except Error as e:
            print(e)
            exit()
        try:
            print("Running Query on SQLITE...")
            c.execute(query)
            results = c.fetchall()
            header = list(map(lambda x: x[0], c.description))
            print("Query Successful")

            if pandas_output == True:
                import pandas as pd
                results = pd.DataFrame(results,columns=header)
                results.set_index("id", inplace=True)
                return results
            else:
                results.insert(0,tuple(header))
                return results
        except Error as e:
            print(e)

######################################################
    def plot_hru():
        def series():
            print('hru series')


######################################################
    def plot_sub():
        def series():
            print('sub series')

######################################################
    def plot_rch():
        def rch():
            print('rch series')

######################################################
    def changePar(self,parameter, method, value, sb = 'all' , lulc = 'all', hru = None, log= r'E:\log.txt'):

        import os
        from .assets import dic_par
        from .assets import listtype
        from distutils.dir_util import copy_tree
        import datetime

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
        soil_filenumber = len(listtype.listtype(self.TxtInOut,".sol"))
        sub_filenumber = len(listtype.listtype(self.TxtInOut,".sub"))-1 #minus 1: output.sub
        print ("You have %.0f hrus and %.0f subbasins this project" %
               (soil_filenumber,sub_filenumber))

        filelist = listtype.listtype(self.TxtInOut,target_file)
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

######################################################
    def getParHru(sb=all, lulc=all):

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

        #TXTInOut = self.TxtInOut

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
#Start - Gets data and filters in variablesInFile and body

        a_variablesInFile = a[0,:].T
        a_body = a[1:,:]
        lulc_col = int(np.where(a_variablesInFile == 'LULC')[0][0])
        sb_col = int(np.where(a_variablesInFile == 'Sub_number')[0][0])

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

        filtered_table = np.vstack((a_variablesInFile,a_body))
        full_table = a
        return filtered_table, full_table
        print("Success!")

