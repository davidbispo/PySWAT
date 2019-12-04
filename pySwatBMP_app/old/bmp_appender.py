import arcpy
from arcpy import env

def mergeswales(lulc, bmps, output_feature):
    
    arcpy.env.overwriteOutput = True
    env.workspace = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb'
    arcpy.Union_analysis([lulc, bmps], output_feature)
    print('Concluido')

def appendBMP(lulc, bmp, erase_output, final_output, field_to_recalc, lulc_code, output_raster, cellsize = 0.05):
        
    arcpy.Erase_analysis(lulc, bmp, erase_output)
    print("Starting....")
    print("Erasing features...")
    # Set environment settings
    
    arcpy.env.overwriteOutput = True
    
    
    # Use Merge tool to move features into single dataset
    print("Merging Features...")
    arcpy.Merge_management([lulc, bmp], final_output)
    arcpy.Delete_management(erase_output)
    print("BMP polygon created successfully!")
    
    usosolo_swales = final_output
    query = "def classify(field):\\n    if field is None:\\n        return %.0f\\n    else:\\n        return field" % (lulc_code)
    
    print("Recalculating Fields for raster composition...")
    arcpy.CalculateField_management(usosolo_swales, "%s"%(field_to_recalc), "classify(!%s!)"%(field_to_recalc), "PYTHON_9.3", query)
    print("Converting Polygon to raster...")
    #arcpy.PolygonToRaster_conversion(usosolo_swales, field_to_recalc, output_raster, cellsize = cellsize)
    
    print("Done!")

lulc = r'E:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\usosolo_bmps'
bmps = r'E:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\Swales_optimistic_unreviewed'
erase_output = r'E:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\erase_output'
output = r'E:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\usosolo_swales_raster'
output_feature = r'E:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\bmps_to_swat\usosolo_swales_feature'
usosolo_feature = 'E:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\barigui\brg_usosolo'
field_to_recalc = "SOLOUSO_CO"
output_raster = r'E:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\swales_raster'

mergeswales(lulc = usosolo_feature, bmps=bmps, output_feature = output_feature)
#appendBMP(lulc, bmps, erase_output, output, field_to_recalc, 51, output_raster)


