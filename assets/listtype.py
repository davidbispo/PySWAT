# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:53:45 2018

@author: david
"""
import os

def listtype(TXTInOut, format_filter):#Gets a list of files to consult and change from
    filelist = []
    for filename in os.listdir(TXTInOut):
        if filename.endswith(format_filter):
            filelist.append(filename)
    return filelist