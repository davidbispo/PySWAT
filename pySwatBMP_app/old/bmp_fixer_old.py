# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 11:10:52 2018

@author: david
"""

data = r"D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb"
arcpy.env.workspace=data
# Check out Production Mapping license
arcpy.CheckOutExtension("Foundation")

# Set environment

# Define variables
#inFeatures="ReferenceData/FacilitySite"
#inFeatureLyr="FaciltyLayer"
#where="FCODE='Park'"
minArea="5 SquareMeters"
bufferIncrease="1 Meter"

# Create a parks feature layer
arcpy.MakeFeatureLayer_management(test_basins,test_basinsFtLyr)
# Execute IncreasePolygonArea
arcpy.IncreasePolygonArea_production(test_basinsFtLyr,minArea,bufferIncrease)