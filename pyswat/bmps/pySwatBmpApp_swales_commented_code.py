# -*- coding: utf-8 -*-
#Dependancies
import os
import archook 
archook.get_arcpy()
import arcpy
import arcgisscripting, sys, traceback
import math
import os
import numpy as np
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

################   PySwatBmpApp-Swales  #################################
"""The PySwatBmpApp-Swales Application is an ArcPy application for 
(i)mirroring(mirror function) and (ii)resizing (matchsize fuction) 
of curbside swales. 

AUTHOR: DAVID BISPO FERREIRA(davidbispo@hotmail.com)
SUPPORT: FEDERAL UNIVERSITY OF PARANA(UFPR)/WATER RESOURCES AND ENVIRONMENTAL 
ENGINEERING POST-GRADUATE PROGRAM(PPGERHA)/
INFRASTRUCTURE AND TRANSPORTATION TECHNOLOGY INSTITUTE(ITTI)

The mirror function requires as INPUTS
(i) a swale feature layer fileaddress As String
(ii) a street layout feature layer fileaddress As String
(iii) an output fileaddress As String
The mirror function (a)fetches the original polygon area (b)uses successive 
buffer+ERASE operations
to reconstruct the original BMP area on the other side of the street layout 
polygon(since swales must be
on a curb according to the theoretical formulation of the program).

*The mirror function returns as OUTPUTS: 
A mirrored swale feature layer As ArcGIS Feature gdb feature layer or shapefile

The matchsize function requires:
(i) a swale feature layer fileaddress As String
(ii) a street layout feature layer fileaddress As String
(iii) an output fileaddress As String
The matchsize function (a)fetches the target polygon area, using the 
formulation proposed by Ferreira(2019) and
(b)uses successive buffer+ERASE operations to reconstruct the target BMP area 
on the other side of the street layout polygon(since swales must be
on a curb according to the theoretical formulation of the program).
"""
#Overwrites previous homonimous files
arcpy.overwriteOutput = True

def mirror(swales_feature, streets, output, env, tolerance = 2):
    
    """ROUTINE FOR MIRRORING SWALES BASED ON A GIVEN BARRIER LAYER"""
#####START####
##Input data##
    
    arcpy.env.workspace=env
    boundaries = streets
    polygons = swales_feature
    output_feature_class = output
    ok_diff = tolerance
    gp = arcgisscripting.create()
    
#creates the final output feature class ->'swales_mirrored'
    arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace, 
        out_name=output_feature_class, geometry_type='POLYGON', 
        spatial_reference=arcpy.Describe(polygons).spatialReference)

#creates a street layout feature layer ->'blyr'
    arcpy.MakeFeatureLayer_management(in_features=boundaries, out_layer='blyr')
    counter = 1
#creates cursor in the bmp polygon
    with arcpy.da.SearchCursor(polygons,['OID@','SHAPE@']) as cursor:
        for row in cursor:
            gp.AddOutputsToMap = False
    
            bufferstart = 4.0
#sql query for creation of layer with the current row in cursor
            sql = """{0} = {1}""".format(
                arcpy.AddFieldDelimiters(polygons,
                arcpy.Describe(polygons).OIDFieldName),row[0])
        
#creates single bmp layer with current sql selection -> 'polygonlyr'
            arcpy.MakeFeatureLayer_management(in_features=polygons, 
                  out_layer='polygonlyr', where_clause=sql)
#gets original bmp area before crossing street
            original_bmp_area = [i[0] for i in arcpy.da.SearchCursor(
                'polygonlyr','SHAPE@AREA')][0]
            print("Original BMP Area = {0}".format(original_bmp_area))
            
            print("Buffer to enlarge = {0}".format(bufferstart))
            arcpy.Buffer_analysis(in_features='polygonlyr', 
                  out_feature_class=r'in_memory\buffered_swale', 
                  buffer_distance_or_field="{0} Meters".format(bufferstart))
            
            arcpy.Erase_analysis(in_features=r'in_memory\buffered_swale', 
                 erase_features='blyr',
                 out_feature_class=r'in_memory\clipswale_base')
#gets the buffered feature area
            buffered_bmp_area = [i[0] for i in arcpy.da.SearchCursor(
            r'in_memory\clipswale_base','SHAPE@AREA')][0]
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
                
                print("Difference for Iteration = {0} m2".format(
                    abs(polygon_this_area-target_area_bmp)))
                print("max= {0}, min = {1}. This Buffer = {2}".format(
                    bufferupper, bufferlower, bufferstart))

#Print iteration results
                arcpy.Buffer_analysis(in_features=r'in_memory\clipswale_base', 
                     out_feature_class=r'in_memory\swale_to_erase', 
                     buffer_distance_or_field="{0} Meters".format(bufferstart))
                
                if bufferstart>= 0:
                    pass
                arcpy.Erase_analysis(in_features=r'in_memory\swale_to_erase', 
                erase_features='blyr',
                out_feature_class=r'in_memory\adjusted_swale')
                
                try:                
                    polygon_this_area = [l[0] for l in arcpy.da.SearchCursor(
                    r'in_memory\adjusted_swale','SHAPE@AREA')][0]
                    
                    print("buffer successful")
                    
                    print("Iteration BMP area = {0}".format(polygon_this_area))

####Bissection method variable change
                    if polygon_this_area > target_area_bmp:
                        bufferlower = bufferstart
                        
                    elif polygon_this_area < target_area_bmp:
                        bufferupper = bufferstart 
                    
                    if polygon_this_area - bufferupper == 0.05:
                        bufferupper -= 1
                        print('too close to the limit')
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
#After successfully finding the buffer value, evolves loop for feature counter and appends it to output feature
            gp.AddOutputsToMap = True
            arcpy.Append_management(inputs=r'in_memory\adjusted_swale', 
                target=output_feature_class, schema_type='NO_TEST')
            print('*************Feature {0} done************!'.format(counter))
            counter += 1
#####END####
            
def matchsize(swales_feature, streets, output, env, tolerance = 2):
    """ROUTINE FOR INCREASING SWALE SIZE"""
#####START#####
#Input data ##
    arcpy.env.workspace=env
    Swales = swales_feature
    boundaries = streets
    polygons = Swales
    output_feature_class = output   
    ok_diff = tolerance
    gp = arcgisscripting.create()

#creates the final output feature class ->'swales_enlarged'
    arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace, 
        out_name=output_feature_class, geometry_type='POLYGON', 
        spatial_reference=arcpy.Describe(polygons).spatialReference)
#creates a street layout feature layer ->'blyr'
    arcpy.MakeFeatureLayer_management(in_features=boundaries, out_layer='blyr')
#creates cursor in the bmp polygon
    with arcpy.da.SearchCursor(polygons,['OID@','SHAPE@']) as cursor:
        for row in cursor:
            gp.AddOutputsToMap = False
            bufferlower = 0.
            bufferupper = 600.
#sql query for creation of layer with the current row in cursor
            sql = """{0} = {1}""".format(
                arcpy.AddFieldDelimiters(
                polygons,arcpy.Describe(polygons).OIDFieldName),row[0])
            
            print(sql)
#creates single bmp layer with current sql selection -> 'polygonlyr'
            arcpy.MakeFeatureLayer_management(in_features=polygons, 
              out_layer='polygonlyr',where_clause=sql)
#gets original bmp area before enlarging swale feature
            swale_initial_area = [i[0] for i in arcpy.da.SearchCursor(
                'polygonlyr','SHAPE@AREA')][0]
            print("Starting BMP area = {0}".format(swale_initial_area))
#gets target area for enlarging Swale feature
            wq_area_for_bmp = 0.15*swale_initial_area/0.004
            
            target_area_bmp = wq_area_for_bmp
            print("Target BMP area/WQ Area = {0}".format(target_area_bmp))
#loop initial settings        
            polygon_area = [k[0] for k in arcpy.da.SearchCursor('polygonlyr',
                'SHAPE@AREA')][0]    
            bufferstart = (bufferlower + bufferupper)/2
            feature_counter = 0
            counter = 0
        
            while abs(polygon_area-target_area_bmp)>ok_diff:
        
                if counter ==0:
#calculates the itertation buffer values        
                    bufferstart = (bufferlower + bufferupper)/2
                    
                    print("Difference = {0}".format(
                        abs(polygon_area-target_area_bmp)))
                    
                    print("Buffer for this iteration = {0}".format(
                            bufferstart))
                    
                    arcpy.Buffer_analysis(in_features='polygonlyr', 
                          out_feature_class=r'in_memory\polygon', 
                          buffer_distance_or_field="{0} Meters".format(
                          bufferstart))
                    
                    arcpy.Erase_analysis(in_features=r'in_memory\polygon', 
                         erase_features='blyr',
                         out_feature_class=r'in_memory\clipbuffer')
#gets the buffered feature area         
                    polygon_this_area = [l[0] for l in arcpy.da.SearchCursor(
                        'in_memory\clipbuffer','SHAPE@AREA')][0]
#Print iteration results   
                    print("Iteration BMP area = {0}".format(polygon_this_area))

####Bissection method variable change
                    if polygon_this_area < target_area_bmp:
                        bufferlower = bufferstart
                        
                    elif polygon_this_area > target_area_bmp:
                        bufferupper = bufferstart 
                        
                    polygon_area = polygon_this_area
                    
                    counter = counter+1
                
                else:
                
                    bufferstart = (bufferlower + bufferupper)/2
                    
                    print("Difference = {0}".format(abs(
                        polygon_area-target_area_bmp)))
                    print("Buffer for this iteration = {0}".format(
                        bufferstart))
                                   
                    arcpy.Buffer_analysis(in_features='polygonlyr', 
                        out_feature_class=r'in_memory\polygon', 
                        buffer_distance_or_field="{0} Meters".format(
                        bufferstart))
                    
                    arcpy.Erase_analysis(in_features=r'in_memory\polygon', 
                        erase_features='blyr',
                        out_feature_class=r'in_memory\clipbuffer')
                                    
                    polygon_this_area = [m[0] for m in arcpy.da.SearchCursor(
                        'in_memory\clipbuffer','SHAPE@AREA')][0]
                    
                    print("Iteration BMP area = {0}".format(polygon_this_area))
                    
####Bissection method variable change
                    if polygon_this_area < target_area_bmp:
                        bufferlower = bufferstart
                        
                    elif polygon_this_area > target_area_bmp:
                        bufferupper = bufferstart 
                    
                    polygon_area = polygon_this_area
                    
                    counter += 1
#After successfully finding the buffer value, evolves loop for feature counter
#and appends it to output feature
            feature_counter +=1
            gp.AddOutputsToMap = True
            arcpy.Append_management(inputs=r'in_memory\clipbuffer', 
                target=output_feature_class, schema_type='NO_TEST')
            
            print('*************Feature {0} done************'.format(
                feature_counter))
            counter += 1
#####END####

#Commands for mirror App
env = r'C:\Database.gdb'
Swales = r'C:\Default.gdb\swales_tomirror'
boundaries = r'C:\parcels'
output_feature_class = r'\swales_mirrored'
mirror(Swales,boundaries, output_feature_class)

#Commands for matchsize App
########################################################################
mirrored_swales = r'C:\swales_mirrored'
output_feature_class_enlarged = r'\swales_mirrored_enlarged'
matchsize(mirrored_swales, boundaries, output_feature_class_enlarged)