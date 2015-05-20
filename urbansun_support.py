import sys

inputname = sys.argv[1]
outputname = sys.argv[2]
azimuth = sys.argv[3]
elevation = sys.argv[4]
print inputname, outputname,azimuth, elevation


import arcpy
arcpy.CheckOutExtension("3D")
arcpy.HillShade_3d(inputname, outputname, str(azimuth), str(elevation), "SHADOWS", "1") 
print "finished"
