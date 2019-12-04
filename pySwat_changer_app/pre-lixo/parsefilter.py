# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 17:31:07 2018

@author: david
"""
def parsefilter(string):
    dicarg = {}
    if string.find('subbasin') != -1 :
        subbasin_pos = string.find('subbasin')
        subbasin_start = subbasin_pos + 8
        subbasin_end = string.find(' ',subbasin_start)
    elif string.find('Subbasin') != -1:
        subbasin_pos = string.find('Subbasin')
        subbasin_start = subbasin_pos + 8
        subbasin_end = string.find(' ',subbasin_start)
    elif string.find('sb') != -1:
        subbasin_pos = string.find('sb')
        subbasin_start = subbasin_pos + 2
        subbasin_end = string.find(' ',subbasin_start)
        arg_value = string[subbasin_start:subbasin_end]
    else:
        dicarg['subbasin'] = None
        
        
    if string.find('lulc') != -1 :
        
        lulc_pos = string.find('lulc')
        lulc_start = subbasin_pos + 4
        
        lulc_end = string.find('',lulc_start)
        arg_value = string[lulc_start:lulc_end]
        dicarg['lulc'] = argvalue
    else:
        dicarg['lulc'] = None
        
    return dicarg
    