# -*- coding: utf-8 -*-
import os
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

#Input data#
InfBasins = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\InfiltrationBasin_raw_Inters'
InfBasinsTest = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\test_inf'   
Swales = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\Swales_optimistic_unreviewed'

boundaries = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\brg_swat_masked\lotes_basin_swat'
polygons = Swales

out_feature_class = r'\bmps_to_swat\test_swales_done'


#Change to match your desired size of polygon, ok difference and step in buffer radius increase
#size = 200 # For pre-defined sizing turn on
ok_diff = 2
increment = 0.001

arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace, out_name=out_feature_class, 
                                   geometry_type='POLYGON', 
                                   spatial_reference=arcpy.Describe(polygons).spatialReference)

arcpy.MakeFeatureLayer_management(in_features=boundaries, out_layer='blyr')

with arcpy.da.SearchCursor(polygons,['OID@','SHAPE@']) as cursor:
    for row in cursor:
        bufferlower = 0.
        bufferupper = 30.
        sql = """{0} = {1}""".format(
            arcpy.AddFieldDelimiters(polygons,arcpy.Describe(polygons).OIDFieldName),row[0])
        print(sql)
        arcpy.MakeFeatureLayer_management(in_features=polygons, out_layer='polygonlyr',
                                          where_clause=sql)
        
        arcpy.SelectLayerByLocation_management(in_layer='blyr', overlap_type='CONTAINS', 
                                              select_features='polygonlyr')
        
        boundary_area = [i[0] for i in arcpy.da.SearchCursor('blyr','SHAPE@AREA')][0]
        if boundary_area <= 5000:
            max_area_for_bmp = boundary_area*0.35
        elif boundary_area > 5000 and boundary_area < 10000:
            max_area_for_bmp = boundary_area*0.30
        elif boundary_area > 10000 and boundary_area < 20000:
            max_area_for_bmp = boundary_area*0.15
        elif boundary_area > 20000 and boundary_area < 30000:
            max_area_for_bmp = boundary_area*0.10
        elif boundary_area > 30000:
            max_area_for_bmp = boundary_area*0.07
        
        print("Max BMP Area = {0}".format(max_area_for_bmp))

        wq_area_for_bmp = 1.2*boundary_area/0.002
        print("WQ Area = {0}".format(wq_area_for_bmp))
    
        if wq_area_for_bmp < max_area_for_bmp:
            target_area_bmp = wq_area_for_bmp
        elif wq_area_for_bmp > max_area_for_bmp:
            target_area_bmp = max_area_for_bmp
        
        if [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0] < target_area_bmp: #if final parcel area is smaller than polygon
            print("Parcel Area = {0}".format(boundary_area))
            polygon_area = [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]
            
            print("Starting BMP area = {0}".format(polygon_area))
            print("Target BMP area = {0}".format(target_area_bmp))
            bufferstart = (bufferlower + bufferupper)/2
            while abs(polygon_area-target_area_bmp)>ok_diff:
                bufferstart = (bufferlower + bufferupper)/2
                print("Difference = {0}".format(abs(polygon_area-target_area_bmp)))

                print("Min = {0}, Max = {1}".format(bufferlower,bufferupper))
                print("Buffer = {0}".format(bufferstart))
                
                arcpy.Buffer_analysis(in_features='polygonlyr', out_feature_class=r'in_memory\polygon', 
                                     buffer_distance_or_field="{0} Meters".format(bufferstart))
                arcpy.Clip_analysis(in_features=r'in_memory\polygon', clip_features='blyr',out_feature_class=r'in_memory\clipbuffer')
                polygon_area = [i[0] for i in arcpy.da.SearchCursor(r'in_memory\clipbuffer','SHAPE@AREA')][0]
                print("Iteration BMP area = {0}".format(polygon_area))
                
                if polygon_area < target_area_bmp:
                    bufferlower = bufferstart
                    
                elif polygon_area > target_area_bmp:
                    bufferupper = bufferstart

            arcpy.Append_management(inputs=r'in_memory\clipbuffer', target=out_feature_class, schema_type='NO_TEST')
       
        elif [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0] > target_area_bmp: #if final parcel area is smaller than polygon
            print("Parcel Area = {0}".format(boundary_area))
            polygon_area = [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]
            
            print("Starting BMP area = {0}".format(polygon_area))
            print("Target BMP area = {0}".format(target_area_bmp))
            bufferlower = bufferupper *-1
            bufferupper = 0
           
            bufferstart = ((bufferlower + bufferupper)/2)
            while abs(polygon_area-target_area_bmp)>ok_diff:
                bufferstart = (bufferlower + bufferupper)/2
                print("Difference = {0}".format(abs(polygon_area-target_area_bmp)))

                print("Min = {0}, Max = {1}".format(bufferlower,bufferupper))
                print("Buffer = {0}".format(bufferstart))
                
                arcpy.Buffer_analysis(in_features='polygonlyr', out_feature_class=r'in_memory\polygon', 
                                     buffer_distance_or_field="{0} Meters".format(bufferstart))
                arcpy.Clip_analysis(in_features=r'in_memory\polygon', clip_features='blyr',out_feature_class=r'in_memory\clipbuffer')
                polygon_area = [i[0] for i in arcpy.da.SearchCursor(r'in_memory\clipbuffer','SHAPE@AREA')][0]
                print("Iteration BMP area = {0}".format(polygon_area))
                
                if polygon_area > target_area_bmp:
                    bufferupper = bufferstart
                    
                elif polygon_area < target_area_bmp:
                    bufferlower = bufferstart

            arcpy.Append_management(inputs=r'in_memory\clipbuffer', target=out_feature_class, schema_type='NO_TEST')
