# -*- coding: utf-8 -*-
import os
import archook 
archook.get_arcpy()
import arcgisscripting, sys, traceback
import arcpy
import math
import os
import numpy as np
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
###########################################################################################
################   TITULO  #################################
#def adjust_size(env=None, boundaries = None ,polygons = None):
   
env = r"D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb"
arcpy.env.workspace=env
arcpy.overwriteOutput = True

#Input data# 
#Swales = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\swales_ready'
Swales = r'C:\Users\david\Documents\ArcGIS\Default.gdb\swales_tomirror_2_799'
boundaries = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\lotes_basin_swat_clip'
polygons = Swales

output_feature_class = r'\bmps_to_swat\swales_mirrored_2_799'

#Change to match your desired size of polygon, ok difference and step in buffer radius increase
#size = 200 # For pre-defined sizing turn on
ok_diff = 2
increment = 0.001

######ROUTINE FOR MIRRORING SWALES BASED ON A GIVEN BARRIER LAYER###########
#####START####

gp = arcgisscripting.create()
#creates the final output feature class ->'swales_enlarged'
arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace, out_name=output_feature_class, 
                                   geometry_type='POLYGON', 
                                   spatial_reference=arcpy.Describe(polygons).spatialReference)

arcpy.MakeFeatureLayer_management(in_features=boundaries, out_layer='blyr')
counter = 1

#creates cursor in the bmp polygon
with arcpy.da.SearchCursor(polygons,['OID@','SHAPE@']) as cursor:
    for row in cursor:
        gp.AddOutputsToMap = False

        bufferstart = 4.0
#sql query for creation of layer with the current row in cursor
        sql = """{0} = {1}""".format(
            arcpy.AddFieldDelimiters(polygons,arcpy.Describe(polygons).OIDFieldName),row[0])
    
#creates single bmp layer with current sql selection -> 'polygonlyr'
        arcpy.MakeFeatureLayer_management(in_features=polygons, out_layer='polygonlyr',
                                          where_clause=sql)
#gets original bmp area before crossing street
        original_bmp_area = [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]
        print("Original BMP Area = {0}".format(original_bmp_area))
        
        print("Buffer to enlarge = {0}".format(bufferstart))
        arcpy.Buffer_analysis(in_features='polygonlyr', out_feature_class=r'in_memory\buffered_swale', 
                                     buffer_distance_or_field="{0} Meters".format(bufferstart))
        arcpy.Erase_analysis(in_features=r'in_memory\buffered_swale', erase_features='blyr',out_feature_class=r'in_memory\clipswale_base')
#gets the buffered feature area
        buffered_bmp_area = [i[0] for i in arcpy.da.SearchCursor(r'in_memory\clipswale_base','SHAPE@AREA')][0]
        print("Buffered BMP Area = {0}".format(buffered_bmp_area))
        
#loop initial settings
        target_area_bmp = original_bmp_area
        polygon_this_area = buffered_bmp_area

        bufferlower = 0.
        bufferupper = -6.
        print("Starting to reconstruct Swale")
        while abs(polygon_this_area-target_area_bmp)>ok_diff:
#calculates the itertation buffer values

            bufferstart = (bufferlower + bufferupper)/2
            
            print("Difference for Iteration = {0} m2".format(abs(polygon_this_area-target_area_bmp)))
            print("max= {0}, min = {1}. This Buffer = {2}".format(bufferupper, bufferlower, bufferstart))
#Print iteration results
            arcpy.Buffer_analysis(in_features=r'in_memory\clipswale_base', out_feature_class=r'in_memory\swale_to_erase', 
                                 buffer_distance_or_field="{0} Meters".format(bufferstart))
            
            if bufferstart>= 0:
                pass
            arcpy.Erase_analysis(in_features=r'in_memory\swale_to_erase', erase_features='blyr',out_feature_class=r'in_memory\adjusted_swale')
            try:                
                polygon_this_area = [l[0] for l in arcpy.da.SearchCursor(r'in_memory\adjusted_swale','SHAPE@AREA')][0]
                
                print("buffer successful")
                
                print("Iteration BMP area = {0}".format(polygon_this_area))
            
                if polygon_this_area > target_area_bmp:
                    bufferlower = bufferstart
                    
                elif polygon_this_area < target_area_bmp:
                    bufferupper = bufferstart 
                
                if polygon_this_area - bufferupper == 0.05:
                    bufferupper -= 1
                    print('too close to the limit')
                
                    
                current_polygon_area = polygon_this_area
            except:
                print('Buffer failed')
                if abs(bufferstart) <= 1.0:    
                    bufferupper += 0.04
                if abs(bufferstart) <= 0.5:    
                    bufferupper += 0.025
                    print('Buffer reduced 0.04')
                else:
                    print('Buffer reduced 0.25')
                    bufferupper += 0.20
                if bufferstart>= 0:
                    pass
                        
        gp.AddOutputsToMap = True
        arcpy.Append_management(inputs=r'in_memory\adjusted_swale', target=output_feature_class, schema_type='NO_TEST')
        print('*************Feature {0} done************!'.format(counter))
        counter += 1
#####END####
                
######ROUTINE FOR INCREASING SWALE SIZE###########
#####START####
""""

#Input data# 
Swales = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\swales_test_enlarge'
boundaries = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\brg_swat_masked\lotes_basin_swat'
polygons = Swales

out_feature_class = r'\bmps_to_swat\swales_enlarged'

#Change to match your desired size of polygon, ok difference and step in buffer radius increase
#size = 200 # For pre-defined sizing turn on
ok_diff = 2
increment = 0.001

arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace, out_name=out_feature_class, 
                                   geometry_type='POLYGON', 
                                   spatial_reference=arcpy.Describe(polygons).spatialReference)

    with arcpy.da.SearchCursor(polygons,['OID@','SHAPE@']) as cursor:
        for row in cursor:
            bufferlower = 0.
            bufferupper = 10    
        
            swale_initial_area = [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]
            print("Starting BMP area = {0}".format(swale_initial_area))
            
            wq_area_for_bmp = 0.4*swale_initial_area/0.003
            
            target_area_bmp = wq_area_for_bmp
            print("Target BMP area/WQ Area = {0}".format(target_area_bmp))
        
            polygon_area = [k[0] for k in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]
    
            bufferstart = (bufferlower + bufferupper)/2
            counter = 0
        
            while abs(polygon_area-target_area_bmp)>ok_diff:
        
                if counter ==0:
                
                    bufferstart = (bufferlower + bufferupper)/2
                    
                    print("Difference = {0}".format(abs(polygon_area-target_area_bmp)))
                    print("Buffer for this iteration = {0}".format(bufferstart))
                    
                    arcpy.Buffer_analysis(in_features='polygonlyr', out_feature_class=r'in_memory\polygon', 
                                         buffer_distance_or_field="{0} Meters".format(bufferstart))
                                    
                    polygon_this_area = [l[0] for l in arcpy.da.SearchCursor('in_memory\polygon','SHAPE@AREA')][0]
                    
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
                    
                    #arcpy.Delete_management('in_memory\polygon')
                    
                    arcpy.Buffer_analysis(in_features='polygonlyr', out_feature_class=r'in_memory\polygon', 
                                         buffer_distance_or_field="{0} Meters".format(bufferstart))
                                    
                    polygon_this_area = [m[0] for m in arcpy.da.SearchCursor('in_memory\polygon','SHAPE@AREA')][0]
                    print("Iteration BMP area = {0}".format(polygon_area))
                    
                    if polygon_this_area < target_area_bmp:
                        bufferlower = bufferstart
                        
                    elif polygon_this_area > target_area_bmp:
                        bufferupper = bufferstart 
                    
                    polygon_area = polygon_this_area
                    
                    counter = counter+1
            
        arcpy.Append_management(inputs=r'in_memory\polygon', target=out_feature_class, schema_type='NO_TEST')
        """
#####END####