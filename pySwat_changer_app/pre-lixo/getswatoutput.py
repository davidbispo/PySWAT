# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 20:25:04 2018

@author: David Bispo
"""
import get_output as go

TXTInOut = r'D:\TxtInOut'     
instance_cp = cp.par_handler(TXTInOut)
fileadress = os.path.join(TXTInOut,'output.rch')
variables = ["FLOW_OUTcms"]
observed = r'D:\OneDrive\Planilha-mestra_geral_v2_test.csv'
rel_table = {"tmd":39, "stq":98, "cax":155}

instance_go = go.output_rch(fileadress,[39,98,155],variables,observed_input = observed, rel_table = rel_table)