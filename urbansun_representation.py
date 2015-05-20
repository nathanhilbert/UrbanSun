# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 09:33:13 2012

@author: hilbert.34
"""


from astral import Astral
from datetime import datetime
#import subprocess
import arcpy
arcpy.CheckOutExtension("3D")


starttime = 1325394000
endtime = 1356939000


teststarttime = 1341129600
endtesttime = 1341216000

a = Astral()

city = a['columbus']

OUPUTDIR = "D:/GIS Project Data/Lidar Testing/Ben/representation/"
INPUTRASTER = "D:/GIS Project Data/Lidar Testing/Ben/output/tempraster82.tif"

currenttime = teststarttime
while currenttime < endtesttime:
    thetime = datetime.fromtimestamp(currenttime, city.tz)
    
    azimuth = city.solar_azimuth(thetime)
    
    print "azimuth", azimuth
    
    
    elevation = city.solar_elevation(thetime)
    if elevation < 0:
        currenttime += 3600
        continue
    
    print "solar elevation", elevation
    
    
    #subprocess.call(["C:/GDAL/gdaldem.exe", "hillshade", INPUTRASTER, OUPUTDIR + "hillshade" + str(int(currenttime)) + ".tif", "-az", str(azimuth), "-alt", str(elevation)])
    arcpy.HillShade_3d(INPUTRASTER, OUPUTDIR + "hillshade" + str(int(currenttime)) + ".tif", str(azimuth), str(elevation), "SHADOWS", "1")  
    print "finished", str(datetime.fromtimestamp(currenttime).strftime('%Y-%m-%d %H:%M:%S'))        
    
    #add one hour
    currenttime += 3600








#31536000 = 1 year
#604800 seconds = 1 week
#86400 = 1 day
#3600 = 1 hour



