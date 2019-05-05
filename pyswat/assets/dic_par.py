# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:16:19 2018

@author: david
"""

class param_dic:
    
    def __init__(self):
        
        self.dictionary = {
        'CANMX':     ['.hru', 8, ['output.hru']],
        'SLSUBBSN':  ['.hru', 2, ['output.hru']],
        'HRU_SLP':   ['.hru', 3, ['output.hru']], 
        'OV_N':      ['.hru', 4, ['output.hru']], 
        'LAT_TTIME': ['.hru', 5,['output.hru']],
        'SLSOIL':    ['.hru', 7,['output.hru']],
        'ESCO':      ['.hru', 9,['output.hru']],
        'EPCO':      ['.hru', 10,['output.hru']],
        'SURLAG':    ['.hru', 43,['output.hru']],
        'R2ADJ':     ['.hru', 44,['output.hru']],
        
        'CN2':       ['.mgt', 10, ['output.mgt']], 
        
        'SHALLST':   ['.gw', 1, []], 
        'DEEPST':    ['.gw', 2, []],
        'GW_DELAY':  ['.gw', 3, []],
        'ALPHA_BF':  ['.gw', 4, []],
        'GWQMN':     ['.gw', 5, []],
        'GW_REVAP':  ['.gw', 6, []],
        'REVAPMN':   ['.gw', 7, []],
        'RCHRG_DP':  ['.gw', 8, []],
        'GW_SPYLD':  ['.gw', 10, []],
        'ALPHA_BF_D': ['.gw', 16, []],#
        
        'SOL_K': ['.sol', 10 , []],
        'SOL_AWC': ['.sol', 9 , []],
        
        'CH_K1': ['.sub', 27 , ['output.sub']],
        'CH_N1': ['.sub', 28 , ['output.sub']],
        
        'ALPHA_BNK': ['.rte', 10 , []],
        'CH_K2': ['.rte', 6 , []],
        'CH_N2': ['.rte', 5 , []],
        
        #'URBCN': ['.sub', 27 , ['.dat']],
        
        } 
                           
    
    def dic_query(self,key):
        dic = self.dictionary
        query = dic[key]
        return query[0], query[1],query[2]
    
    def dic_hru_parser(self):
        hru_header_list = ["LULC",
        'HRU','GIS', 'SUB','MGT','MO', 'DA',   'YR',   'AREAkm2',  'PRECIPmm', 'SNOFALLmm' ,'SNOMELTmm',    
        'IRRmm', 'PETmm','ETmm', 'SW_INITmm', 'SW_ENDmm','PERCmm','GW_RCHGmm', 'DA_RCHGmm', 'REVAPmm',  
        'SA_IRRmm', 'DA_IRRmm',  'SA_STmm',  'DA_STmm','SURQGENmm', 'SURQ_CNTmm', 'TLOSSmm','LATQGENmm',    
        'GW_Qmm',    'WYLDmm',   'DAILYCN', 'TMP_AVdgC', 'TMP_MXdgC', 'TMP_MNdg','CSOL_TMPdg','CSOLARMJ/m2', 
        'SYLDt/ha', 'USLEt/ha','N_APPkg/ha','P_APPkg/ha','NAUTOkg/ha''PAUTOkg/ha','NGRZkg/ha ','PGRZkg/ha',
        'NCFRTkg/ha','PCFRTkg/ha','NRAINkg/ha', 'NFIXkg/ha', 'F-MNkg/ha','A-MNkg/ha', 'A-SNkg/ha', 'F-MPkg/ha',
        'AO-LPkg/ha','L-APkg/ha', 'A-SPkg/ha', 'DNITkg/ha',  'NUPkg/ha',  'PUPkg/ha','ORGNkg/ha', 'ORGPkg/ha', 
        'SEDPkg/ha','NSURQkg/ha','NLATQkg/ha','NO3Lkg/ha','NO3GWkg/ha','SOLPkg/ha', 'P_GWkg/ha', 'W_STRS',  
        'TMP_STRS',   'N_STRS',    'P_STRS',  'BIOMt/ha',       'LAI',   'YLDt/ha',  'BACTPct',  'BACTLPct', 
        'WTAB','CLIm','WTAB','SOLm',     'SNOmm', 'CMUPkg/ha','CMTOTkg/ha',  'QTILEmm','TNO3kg/ha', 'LNO3kg/ha', 
        'GW_Q_Dmm', 'LATQCNTmm', 'TVAPkg/ha',]
          
        return hru_header_list
    def dic_keys(self):
        return list(self.dictionary.keys())
    