# -*- coding: utf-8 -*-
import arcgisscripting, sys, traceback
import os
import archook 
archook.get_arcpy()
import arcpy
import math
import os
import numpy as np
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
###########################################################################################
################   TITLE  #################################
   
env = r"D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb"
arcpy.env.workspace=env
arcpy.overwriteOutput = True

#Input data# 
#Swales = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\swales_ready'
Swales = r'C:\Users\david\Documents\ArcGIS\to_go.gdb\to_go_1500_2081'
boundaries = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\lotes_basin_swat_clip'
polygons = Swales

output_feature_class = r'\bmps_to_swat\swales_enlarged_1500_2081'

#Change to match your desired size of polygon, ok difference and step in buffer radius increase
#size = 200 # For pre-defined sizing turn on
ok_diff = 2
increment = 0.001

gp = arcgisscripting.create()
                
######ROUTINE FOR INCREASING SWALE SIZE###########
#####START####

#Input data# 
arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace, out_name=output_feature_class, 
                                   geometry_type='POLYGON', 
                                   spatial_reference=arcpy.Describe(polygons).spatialReference)
with arcpy.da.SearchCursor(polygons,['OID@','SHAPE@']) as cursor:
    for row in cursor:
        gp.AddOutputsToMap = False
        bufferlower = 0.
        bufferupper = 600.
    
        sql = """{0} = {1}""".format(
            arcpy.AddFieldDelimiters(polygons,arcpy.Describe(polygons).OIDFieldName),row[0])
        
        print(sql)
        
        arcpy.MakeFeatureLayer_management(in_features=polygons, out_layer='polygonlyr',
                                          where_clause=sql)
        
        swale_initial_area = [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]
        print("Starting BMP area = {0}".format(swale_initial_area))
        
        wq_area_for_bmp = 0.15*swale_initial_area/0.004
        
        target_area_bmp = wq_area_for_bmp
        print("Target BMP area/WQ Area = {0}".format(target_area_bmp))
    
        polygon_area = [k[0] for k in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]

        bufferstart = (bufferlower + bufferupper)/2
        feature_counter = 0
        counter = 0
    
        while abs(polygon_area-target_area_bmp)>ok_diff:
    
            if counter ==0:
            
                bufferstart = (bufferlower + bufferupper)/2
                
                print("Difference = {0}".format(abs(polygon_area-target_area_bmp)))
                
                print("Buffer for this iteration = {0}".format(bufferstart))
                
                arcpy.Buffer_analysis(in_features='polygonlyr', out_feature_class=r'in_memory\polygon', 
                                     buffer_distance_or_field="{0} Meters".format(bufferstart))
                
                arcpy.Erase_analysis(in_features=r'in_memory\polygon', erase_features='blyr',out_feature_class=r'in_memory\clipbuffer')
                
                polygon_this_area = [l[0] for l in arcpy.da.SearchCursor('in_memory\clipbuffer','SHAPE@AREA')][0]
                
                print("Iteration BMP area = {0}".format(polygon_this_area))
                
                if polygon_this_area < target_area_bmp:
                    bufferlower = bufferstart
                    
                elif polygon_this_area > target_area_bmp:
                    bufferupper = bufferstart 
                    
                polygon_area = polygon_this_area
                
                counter = counter+1
            
            else:
            
                bufferstart = (bufferlower + bufferupper)/2
                
                print("Difference = {0}".format(abs(polygon_area-target_area_bmp)))
                print("Buffer for this iteration = {0}".format(bufferstart))
                               
                arcpy.Buffer_analysis(in_features='polygonlyr', out_feature_class=r'in_memory\polygon', 
                                     buffer_distance_or_field="{0} Meters".format(bufferstart))
                
                arcpy.Erase_analysis(in_features=r'in_memory\polygon', erase_features='blyr',out_feature_class=r'in_memory\clipbuffer')
                                
                polygon_this_area = [m[0] for m in arcpy.da.SearchCursor('in_memory\clipbuffer','SHAPE@AREA')][0]
                
                print("Iteration BMP area = {0}".format(polygon_this_area))
                
                if polygon_this_area < target_area_bmp:
                    bufferlower = bufferstart
                    
                elif polygon_this_area > target_area_bmp:
                    bufferupper = bufferstart 
                
                polygon_area = polygon_this_area
                
                counter += 1
    
        feature_counter +=1
        gp.AddOutputsToMap = True
        print("appending...")
        arcpy.Append_management(inputs=r'in_memory\clipbuffer', target=output_feature_class, schema_type='NO_TEST')
        print('*************Feature {0} done************!'.format(feature_counter))
        counter += 1
#####END####