# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:16:19 2018

@author: david
"""

class param_dic:
    
    def __init__(self,):
        
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
        
        #'CH_K1': ['.sub', 27 , ['output.sub']],
        #'CH_N1': ['.sub', 28 , ['output.sub']],
        
        'ALPHA_BNK': ['.rte', 10 , []],
        'CH_K2': ['.rte', 6 , []],
        'CH_N2': ['.rte', 5 , []],
        
        #'URBCN': ['.sub', 27 , ['.dat']],
        
        } 
                 
    def dic_keys(self):
        return list(self.dictionary.keys())          
    
    def dic_query(self,key):
        dic = self.dictionary
        query = dic[key]
        return query[0], query[1],query[2]
    
# =============================================================================
#     def dic_hru_parser(self):
#         hru_header_list = ["LULC",
#         'HRU','GIS', 'SUB','MGT','MO', 'DA',   'YR',   'AREAkm2',  'PRECIPmm', 'SNOFALLmm' ,'SNOMELTmm',    
#         'IRRmm', 'PETmm','ETmm', 'SW_INITmm', 'SW_ENDmm','PERCmm','GW_RCHGmm', 'DA_RCHGmm', 'REVAPmm',  
#         'SA_IRRmm', 'DA_IRRmm',  'SA_STmm',  'DA_STmm','SURQGENmm', 'SURQ_CNTmm', 'TLOSSmm','LATQGENmm',    
#         'GW_Qmm',    'WYLDmm',   'DAILYCN', 'TMP_AVdgC', 'TMP_MXdgC', 'TMP_MNdg','CSOL_TMPdg','CSOLARMJ/m2', 
#         'SYLDt/ha', 'USLEt/ha','N_APPkg/ha','P_APPkg/ha','NAUTOkg/ha''PAUTOkg/ha','NGRZkg/ha ','PGRZkg/ha',
#         'NCFRTkg/ha','PCFRTkg/ha','NRAINkg/ha', 'NFIXkg/ha', 'F-MNkg/ha','A-MNkg/ha', 'A-SNkg/ha', 'F-MPkg/ha',
#         'AO-LPkg/ha','L-APkg/ha', 'A-SPkg/ha', 'DNITkg/ha',  'NUPkg/ha',  'PUPkg/ha','ORGNkg/ha', 'ORGPkg/ha', 
#         'SEDPkg/ha','NSURQkg/ha','NLATQkg/ha','NO3Lkg/ha','NO3GWkg/ha','SOLPkg/ha', 'P_GWkg/ha', 'W_STRS',  
#         'TMP_STRS',   'N_STRS',    'P_STRS',  'BIOMt/ha',       'LAI',   'YLDt/ha',  'BACTPct',  'BACTLPct', 
#         'WTAB','CLIm','WTAB','SOLm',     'SNOmm', 'CMUPkg/ha','CMTOTkg/ha',  'QTILEmm','TNO3kg/ha', 'LNO3kg/ha', 
#         'GW_Q_Dmm', 'LATQCNTmm', 'TVAPkg/ha',]
#           
#         return hru_header_list
# =============================================================================


class Parameters:
    
    def __init__(self, filetype):
        
        if filetype == 'hru':
            self.relParameterDBType = {
            'LULC':'TEXT',
            'HRU': 'NUMERIC',
            'GIS': 'NUMERIC',
            'SUB': 'NUMERIC',
            'MGT': 'NUMERIC',
            'MO': 'NUMERIC',
            'DA': 'NUMERIC',
            'YR': 'NUMERIC',
            'AREAkm2': 'NUMERIC',
            'PRECIPmm': 'NUMERIC',
            'SNOFALLmm' : 'NUMERIC',
            'SNOMELTmm': 'NUMERIC',
            'IRRmm': 'NUMERIC',
            'PETmm': 'NUMERIC',
            'ETmm': 'NUMERIC',
            'SW_INITmm': 'NUMERIC',
            'SW_ENDmm': 'NUMERIC',
            'PERCmm': 'NUMERIC',
            'GW_RCHGmm': 'NUMERIC',
            'DA_RCHGmm': 'NUMERIC',
            'REVAPmm': 'NUMERIC',
            'SA_IRRmm': 'NUMERIC',
            'DA_IRRmm': 'NUMERIC',
            'SA_STmm': 'NUMERIC',
            'DA_STmm': 'NUMERIC',
            'SURQ_GENmm': 'NUMERIC',
            'SURQ_CNTmm': 'NUMERIC',
            'TLOSSmm': 'NUMERIC',
            'LATQGENmm': 'NUMERIC',
            'GW_Qmm': 'NUMERIC',
            'WYLDmm': 'NUMERIC',
            'DAILYCN': 'NUMERIC',
            'TMP_AVdgC': 'NUMERIC',
            'TMP_MXdgC': 'NUMERIC',
            'TMP_MNdgC': 'NUMERIC',
            'CSOL_TMPdgC': 'NUMERIC',
            'SOLARMJ/m2': 'NUMERIC',
            'SYLDt/ha': 'NUMERIC',
            'USLEt/ha': 'NUMERIC',
            'N_APPkg/haP': 'NUMERIC',
            'P_APPkg/ha': 'NUMERIC',
            'NAUTOkg/ha': 'NUMERIC',
            'PAUTOkg/ha': 'NUMERIC',
            'NGRZkg/ha ': 'NUMERIC',
            'PGRZkg/ha': 'NUMERIC',
            'NCFRTkg/ha': 'NUMERIC',
            'PCFRTkg/ha': 'NUMERIC',
            'NRAINkg/ha': 'NUMERIC',
            'NFIXkg/ha': 'NUMERIC',
            'F-MNkg/ha': 'NUMERIC',
            'A-MNkg/ha': 'NUMERIC',
            'A-SNkg/ha': 'NUMERIC',
            'F-MPkg/ha': 'NUMERIC',
            'AO-LPkg/ha': 'NUMERIC',
            'L-APkg/ha': 'NUMERIC',
            'A-SPkg/ha': 'NUMERIC',
            'DNITkg/ha': 'NUMERIC',
            'NUPkg/ha': 'NUMERIC',
            'PUPkg/ha': 'NUMERIC',
            'ORGNkg/ha': 'NUMERIC',
            'ORGPkg/ha': 'NUMERIC',
            'SEDPkg/ha': 'NUMERIC',
            'NSURQkg/ha': 'NUMERIC',
            'NLATQkg/ha': 'NUMERIC',
            'NO3Lkg/ha': 'NUMERIC',
            'NO3GWkg/ha': 'NUMERIC',
            'SOLPkg/ha': 'NUMERIC',
            'P_GWkg/ha': 'NUMERIC',
            'W_STRS': 'NUMERIC',
            'TMP_STRS': 'NUMERIC',
            'N_STRS': 'NUMERIC',
            'P_STRS': 'NUMERIC',
            'BIOMt/ha': 'NUMERIC',
            'LAI': 'NUMERIC',
            'YLDt/ha': 'NUMERIC',
            'BACTPct': 'NUMERIC',
            'BACTLPct': 'NUMERIC',
            'WTAB CLIm': 'NUMERIC',
            'WTAB SOLm': 'NUMERIC',
            'SNOmm': 'NUMERIC',
            'CMUPkg/ha': 'NUMERIC',
            'CMTOTkg/ha': 'NUMERIC',
            'QTILEmm': 'NUMERIC',
            'TNO3kg/ha': 'NUMERIC',
            'LNO3kg/ha': 'NUMERIC',
            'GW_Q_Dmm': 'NUMERIC',
            'LATQCNTmm': 'NUMERIC',
            'TVAPkg/ha': 'NUMERIC'
            }
        elif filetype == 'rch':
            self.relParameterDBType = {
            #RCH VARIABLES
           'RCH ':'NUMERIC',
           'GIS' :'NUMERIC',
           'MO' :'NUMERIC',
           'DA' :'NUMERIC',
           'YR'  :'NUMERIC',
           'AREAkm2' :'NUMERIC',
           'FLOW_INcms':'NUMERIC',
           'FLOW_OUTcms':'NUMERIC',
           'EVAPcms'    :'NUMERIC',
           'TLOSScms'  :'NUMERIC',
           'SED_INtons' :'NUMERIC',
           'SED_OUTtons' :'NUMERIC',
           'SEDCONCmg/L':'NUMERIC',   
           'ORGN_INkg'  :'NUMERIC',
           'ORGN_OUTkg'   :'NUMERIC',
           'ORGP_INkg'  :'NUMERIC',
           'ORGP_OUTkg'    :'NUMERIC',
           'NO3_INkg'   :'NUMERIC',
           'NO3_OUTkg'    :'NUMERIC',
           'NH4_INkg'   :'NUMERIC',
           'NH4_OUTkg'    :'NUMERIC',
           'NO2_INkg'   :'NUMERIC',
           'NO2_OUTkg'  :'NUMERIC',
           'MINP_INkg' :'NUMERIC',
           'MINP_OUTkg'   :'NUMERIC',
           'CHLA_INkg'  :'NUMERIC',
           'CHLA_OUTkg'   :'NUMERIC',
           'CBOD_INkg'  :'NUMERIC',
           'CBOD_OUTkg'  :'NUMERIC',
           'DISOX_INkg' :'NUMERIC',
           'DISOX_OUTkg' :'NUMERIC',
           'SOLPST_INmg':'NUMERIC',
           'SOLPST_OUTmg':'NUMERIC',
           'SORPST_INmg':'NUMERIC',
           'SORPST_OUTmg':'NUMERIC',
           'REACTPSTmg'  :'NUMERIC',
           'VOLPSTmg' :'NUMERIC',
           'SETTLPSTmg':'NUMERIC',
           'RESUSP_PSTmg':'NUMERIC',
           'DIFFUSEPSTmg':'NUMERIC',
           'REACBEDPSTmg'  :'NUMERIC',
           'BURYPSTmg'   :'NUMERIC',
           'BED_PSTmg':'NUMERIC',
           'BACTP_OUTct':'NUMERIC',
           'BACTLP_OUTct':'NUMERIC',
           'CMETAL#1kg' :'NUMERIC',
           'CMETAL#2kg':'NUMERIC',
           'CMETAL#3kg'    :'NUMERIC',
           'TOT Nkg'   :'NUMERIC',
           'TOT Pkg':'NUMERIC',  
           'NO3ConcMg/l':'NUMERIC',  
           'WTMPdegc':'NUMERIC',

}
        elif filetype == 'sub':
            self.relParameterDBType = {
        #SUB VARIABLES
            'SUB':'NUMERIC',
            'GIS':'NUMERIC',
            'MO':'NUMERIC',
            'DA':'NUMERIC',
            'YR':'NUMERIC',
            'AREAkm2':'NUMERIC', 
            'PRECIPmm':'NUMERIC', 
            'SNOMELTmm':'NUMERIC',
            'PETmm':'NUMERIC',
            'ETmm':'NUMERIC',
            'SWmm':'NUMERIC', 
            'PERCmm':'NUMERIC', 
            'SURQmm':'NUMERIC',  
            'GW_Qmm':'NUMERIC',  
            'WYLDmm':'NUMERIC', 
            'SYLDt/ha':'NUMERIC',
            'ORGNkg/ha':'NUMERIC',
            'ORGPkg/ha':'NUMERIC',
            'NSURQkg/ha':'NUMERIC',
            'SOLPkg/ha':'NUMERIC',
            'SEDPkg/ha':'NUMERIC',
            'LAT Q(mm)':'NUMERIC',
            'LATNO3kg/h':'NUMERIC',
            'GWNO3kg/ha':'NUMERIC',
            'CHOLAmic/L':'NUMERIC', 
            'CBODU mg/L':'NUMERIC', 
            'DOXQ mg/L':'NUMERIC', 
            'TNO3kg/ha':'NUMERIC',  
            'QTILEmm':'NUMERIC', 
            'TVAPkg/ha':'NUMERIC'
        }

    def returnVariableDBType(self,key):
        return self.relParameterDBType[key]

