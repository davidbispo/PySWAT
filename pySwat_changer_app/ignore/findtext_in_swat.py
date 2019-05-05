# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 10:10:38 2019

@author: David
"""

import matplotlib.pyplot as plt 
import numpy as np 
import os

string = 'qdr(j) = '
directory = r'E:\Users\David\Downloads\SWAT'


a = os.listdir(directory)
foundfiles = []
for i in a:
    fileaddress = os.path.join(directory, i)
    openfile = open(fileaddress)
    filelines = openfile.readlines()
    
    for linenumber in range(len(filelines)):
        line = filelines[linenumber]

        if string in line:
            foundfiles.append([i,linenumber, line])

            