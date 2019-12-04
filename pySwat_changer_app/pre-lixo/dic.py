# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:16:19 2018

@author: david
"""

class param_dic:
    
    def __init__(self):
        
        self.dictionary = {
        'CANMX': ['.hru', 8, ['output.hru']],
        'SLSUBBSN': ['.hru', 2,'output.hru'],
        'HRU_SLP': ['.hru', 3,'output.hru'], 
        'OV_N': ['.hru', 4,'output.hru'], 
        'LAT_TTIME': ['.hru', 5,'output.hru'],
        'SLSOIL': ['.hru', 5,'output.hru'],
        'ESCO': ['.hru', 9,'output.hru'],
        'EPCO': ['.hru', 10,'output.hru'],
        'SURLAG': ['.hru', 43,'output.hru'],
        'R2ADJ': ['.hru', 44,'output.hru'],
        
        'CN2': ['.mgt', 10, []], 
        
        'SHALLST': ['.gw', 1, []], 
        'DEEPST': ['.gw', 2, []],
        'GW_DELAY': ['.gw', 3, []],
        'ALPHA_BF': ['.gw', 4, []],
        'GWQMN': ['.gw', 5, []],
        'GW_REVAP': ['.gw', 6, []],
        'REVAPMN': ['.gw', 7, []],
        'RCHRG_DP': ['.gw', 8, []],
        'GW_SPYLD': ['.gw', 10, []],
        'ALPHA_BF_D': ['.gw', 16, []],
        
        } 
                           
    
    def dic_query(self,key):
        dic = self.dictionary
        query = dic[key]
        return query[0], query[1],query[2]
    
    def dic_keys(self):
        return list(self.dictionary.keys())
    