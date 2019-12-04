# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 22:59:47 2018

@author: David Bispo
"""
import get_output as go
import os

output_simlog = r'E:\sim_result_InfBasins.txt'

TXTInOut = r'E:\Barigui_InfBasins\TxtInOut'
fileadress = os.path.join(TXTInOut,'output.rch')
variables = ["FLOW_OUTcms"]
observed = r'D:\OneDrive\Planilha-mestra_geral_v2_test.csv'
rel_table = {"stq":98, "cax":155}

instance_output_simarray = go.output_simarray(output_simlog)
#instance_output_simarray.print_allinone(r'D:\results.png', figsize = (20,10),observed = observed, rel_table = rel_table)
instance_output_simarray.print_allinone(r'E:\results_infbasins.png', figsize = (25.7,17), xlim =(250,300))