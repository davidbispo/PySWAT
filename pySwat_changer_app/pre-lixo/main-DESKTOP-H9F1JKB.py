# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:21:20 2018

@author: David Bispo
"""

#import get_output as go
import change_par as cp 
import get_par as gp
import get_output as go

output_rch = r'D:\Default_test_python\TxtInOut\output.rch'
TXTINOut = r"D:\Default_test_python\TxtInOut"
observed = 'D:\OneDrive\Planilha-mestra_geral_v2.csv'
rel_table = {"tmd":39, "stq":98, "cax":155}

#instance_gp = gp.swat_partable(TXTInOut = TXTINOut, sb = 1, lulc='all')
#instance_cp = cp.par_handler(TXTINOut)

#table, original_table = instance_gp.get_par_hru()
#array = instance_go.read_rch()
#a = instance_go.print_allinone(array,figsize=(100,20))


#instance_cp.change(parameter = 'CN2', method = 'relative', value = -0.083233, sb= list(range(1,40)))#1
#instance_cp.change(parameter = 'GWQMN', method = 'replace', value = 3321.755, sb= list(range(1,40)))#2
#instance_cp.change(parameter = 'RCHRG_DP', method = 'replace', value = 0.8061, sb= list(range(1,40)))#3
#instance_cp.change(parameter = 'HRU_SLP', method = 'relative', value = -0.147, sb= list(range(1,40)))#4
#instance_cp.change(parameter = 'OV_N', method = 'relative', value = -0.3484, sb= list(range(1,40)))#5#
#instance_cp.change(parameter = 'LAT_TTIME', method = 'replace', value = 18.199, sb= list(range(1,40)))#6
#instance_cp.change(parameter = 'CH_K1', method = 'replace', value = 312.289, sb= list(range(1,40)))#7
#instance_cp.change(parameter = 'ALPHA_BNK', method = 'replace', value = 0.3555, sb= list(range(1,40)))#8
#instance_cp.change(parameter = 'CH_K2', method = 'replace', value = 300.123, sb= list(range(1,40)))#9
#instance_cp.change(parameter = 'SOL_K', method = 'relative', value = 0.0800, sb= list(range(1,40)))#10


instance = go.output_rch(output_rch,[39],["FLOW_INcms"],observed_input = observed, rel_table = rel_table)
array = instance.read_rch()
instance.print_allinone(array,figsize=(20,1ttetea0))