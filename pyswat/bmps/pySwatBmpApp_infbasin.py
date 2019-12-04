# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 16:41:59 2019

@author: david
"""
import archook 
archook.get_arcpy()
import arcpy
import arcgisscripting, sys, traceback
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
###########################################################################################
################   TITULO  #################################
def adjustinfbasin(env, inf_basins_feature, streets, output):
   
    arcpy.env.workspace=env
    arcgisscripting.LogHistory = False
    #Input data#
    boundaries = streets
    polygons = inf_basins_feature
    out_feature_class = output
    
    
#Change to match your desired size of polygon, ok difference and step in buffer radius increase
#size = 200 # For pre-defined sizing turn on
    ok_diff = 1    
#creates the output feature
    arcpy.CreateFeatureclass_management(out_path=arcpy.env.workspace, out_name=out_feature_class, 
                                       geometry_type='POLYGON', 
                                       spatial_reference=arcpy.Describe(polygons).spatialReference)
    
#creates a boundary layer with a feature -> 'blyr'
    arcpy.MakeFeatureLayer_management(in_features=boundaries, out_layer='blyr')
    feature_counter = 1
#creates a cursor for the bmp polygon
    with arcpy.da.SearchCursor(polygons,['OID@','SHAPE@']) as cursor:
        for row in cursor:
            flag_deuruim = False
            iterationcounter = 0
            bufferlower = 0.
            bufferupper = 1000.
    
#query to select item 
            sql = """{0} = {1}""".format(
                arcpy.AddFieldDelimiters(polygons,arcpy.Describe(polygons).OIDFieldName),row[0])
            print(sql) #REMOVE IN RUNTIME
    
#creates temporary feature layer for the bmp layer ->'polygonlyr' using sql clause
            arcpy.MakeFeatureLayer_management(in_features=polygons, out_layer='polygonlyr',
                                              where_clause=sql)
    
#selects in the boundary layer the parcel that contains the bmp
            arcpy.SelectLayerByLocation_management(in_layer='blyr', overlap_type='CONTAINS', 
                                                  select_features='polygonlyr')
#fetches the area of the selected parcel 
            try:                
                boundary_area = [i[0] for i in arcpy.da.SearchCursor('blyr','SHAPE@AREA')][0]
                print("Boundary Area = {0}".format(boundary_area))#REMOVE IN RUNTIME
                
                bmp_area = [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]
                print("BMP Area = {0}".format(bmp_area))

#conditionals for bmp sizing 
                if boundary_area <= 5000:
                    max_area_for_bmp = boundary_area*0.95
                elif boundary_area > 5000 and boundary_area < 10000:
                    max_area_for_bmp = boundary_area*0.85
                elif boundary_area > 10000 and boundary_area < 20000:
                    max_area_for_bmp = boundary_area*0.70
                elif boundary_area > 20000 and boundary_area < 30000:
                    max_area_for_bmp = boundary_area*0.60
                elif boundary_area > 30000:
                    max_area_for_bmp = 0.55
        
                print("Max BMP Area = {0}".format(max_area_for_bmp))
        
                wq_area_for_bmp = 0.4*bmp_area/0.003
                
                print("WQ Area = {0}".format(wq_area_for_bmp))
            
                if wq_area_for_bmp < max_area_for_bmp:
                    target_area_bmp = wq_area_for_bmp
                elif wq_area_for_bmp > max_area_for_bmp:
                    target_area_bmp = max_area_for_bmp
                    
                print("Target area = {0}".format(target_area_bmp))
########if final parcel area is smaller than the target area  
                if [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0] < target_area_bmp: 
                    polygon_area = [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]
                    
                    print("Starting BMP area = {0}".format(polygon_area))#REMOVE IN RUNTIME
                    print("Target BMP area = {0}".format(target_area_bmp))#REMOVE IN RUNTIME
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
                    feature_counter +=1
                    print("##############Feature {0} done************#############".format(feature_counter))
                    arcpy.Append_management(inputs=r'in_memory\clipbuffer', target=out_feature_class, schema_type='NO_TEST')

########if final parcel area is larger than target area
                elif [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0] > target_area_bmp:
                    print("Parcel Area = {0}".format(boundary_area))
                    polygon_area = [i[0] for i in arcpy.da.SearchCursor('polygonlyr','SHAPE@AREA')][0]
                    
                    print("Starting BMP area = {0}".format(polygon_area))
                    print("Target BMP area = {0}".format(target_area_bmp))
                    bufferlower = bufferupper *-1
                    bufferupper = 0
                    bufferstart = ((bufferlower + bufferupper)/2)
                    
                    while abs(polygon_area-target_area_bmp)>ok_diff:
                        
                            bufferstart = (bufferlower + bufferupper)/2
                            print("Difference = {0}".format(polygon_area-target_area_bmp))
            
                            print("Min = {0}, Max = {1}".format(bufferlower,bufferupper))
                            print("Buffer = {0}".format(bufferstart))
                            
                            arcpy.Buffer_analysis(in_features='polygonlyr', out_feature_class=r'in_memory\polygon', 
                                                 buffer_distance_or_field="{0} Meters".format(bufferstart))
                            
                            arcpy.Clip_analysis(in_features=r'in_memory\polygon', clip_features='blyr',
                                                out_feature_class=r'in_memory\clipbuffer')
                            try:
                                polygon_area = [i[0] for i in arcpy.da.SearchCursor(r'in_memory\clipbuffer','SHAPE@AREA')][0]
                                print("Iteration BMP area = {0}".format(polygon_area))
                                
                                if polygon_area > target_area_bmp:
                                    bufferupper = bufferstart                        
                                elif polygon_area < target_area_bmp:
                                    bufferlower = bufferstart
                            except:
                                print("Buffer Failed. Reducing buffer...")
                                if bufferstart <=-100:
                                    bufferlower += 50
                                elif bufferstart >-100 and bufferstart <=-50:
                                    bufferlower += 10
                                elif bufferstart >-50 and bufferstart <=-10:
                                    bufferlower += 5
                                elif bufferstart > -10:
                                    bufferlower += 0.25
                            iterationcounter+=1
                            if iterationcounter >70:
                                flag_deuruim = True
                                break
                                print("Deu ruim! Pulando...")
                    if flag_deuruim == False:
                        feature_counter +=1
                        print("##############Feature {0} done************#############".format(feature_counter))
                        arcpy.Append_management(inputs=r'in_memory\clipbuffer', target=out_feature_class, schema_type='NO_TEST')
                    else:
                        pass
            except:
                print("&*&*&*&*&*&Deleting object -> {0} &*&*&*&*&".format(sql))
                #arcpy.SelectLayerByAttribute_management(polygons, "NEW_SELECTION", sql)
                #arcpy.DeleteRows_management(polygons)
                pass
    print("Finished!")

env = r'C:\Default_4.gdb'
InfBasins = r'C:\Default_4.gdb\inf_basins_72001_80654'

boundaries = r'C:\Default_4.gdb\lotes_basin_swat_clip'
out_feature_class = r'\inf_basins_72001_80654_done'

adjustinfbasin(env, InfBasins, boundaries, out_feature_class)