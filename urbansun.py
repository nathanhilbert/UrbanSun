# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 09:33:13 2012

@author: hilbert.34
"""

# Import arcpy module


from datetime import datetime
from astral import Astral
import os
import shutil
import numpy as np
import time
import arcpy
arcpy.CheckOutExtension("3D")


from osgeo import gdal




ONEWEEK = 604800




starttime = 1336536000
endtime = 1348977600


a = Astral()

city = a['columbus']

BASEDIR = "D:/GIS Project Data/Lidar/UrbanSunFinal/"

OUPUTDIR = BASEDIR + "finaloutput/"
PROCESSING = BASEDIR + "Processing/"
INPUTRASTER = BASEDIR + "FeatureRaster/"


outdirList = os.listdir(OUPUTDIR)

dirList = os.listdir(INPUTRASTER)

counter = 0
for fname in dirList:
    namesplit = fname.split('.')
    if namesplit[1] == "tif" and len(namesplit) != 2:
        print "skipping", fname
        continue
    elif namesplit[1] != "tif":
        print "skipping", fname
        continue   
    
    print "doing", fname
    counter +=1
    
    currentweektime = starttime


    
    while currentweektime < endtime:
        readabletime = datetime.fromtimestamp(int(currentweektime))
        outputfile = OUPUTDIR + namesplit[0] + "_" + str(readabletime.year) + "_" + str(readabletime.month) + "_" + str(readabletime.day) + ".tif"
        outputname = namesplit[0] + "_" + str(readabletime.year) + "_" + str(readabletime.month) + "_" + str(readabletime.day) + ".tif"
        #print outputfile
        
        if outputname in outdirList:
            print "skipping this because it exists"
            currentweektime += ONEWEEK
            continue
        
        #print "Copying File"
        shutil.copyfile(PROCESSING + fname, outputfile)
        
        #print "using gdal to open file"
        srcout = gdal.Open(outputfile, gdal.GA_Update)
        bandout = srcout.GetRasterBand(1)
        #print "reading file as array"
        arout = bandout.ReadAsArray()
        
        currenttime = currentweektime
        #print "now working on the week stuff"
        while currenttime < currentweektime + ONEWEEK:
            thetime = datetime.fromtimestamp(currenttime, city.tz)
            
            azimuth = city.solar_azimuth(thetime)
            
            #print "azimuth", azimuth
            
            
            elevation = city.solar_elevation(thetime)
            if elevation < 0:
                currenttime += 3600
                continue

            
            #print "solar elevation", elevation
            
            tempfile = OUPUTDIR + "hillshade" + str(counter) + "_" + str(int(currenttime)) + ".tif"
            #print "running hillshade", INPUTRASTER + fname, tempfile, azimuth, elevation
            #subprocess.call(["C:/GDAL/gdaldem.exe", "hillshade", INPUTRASTER + fname, tempfile, "-az", str(azimuth), "-alt", str(elevation)])
            #subprocess.call(["C:/python26/ArcGIS10.0/python.exe", "C:/Users/hilbert.34/Google Drive/BenUrbanSun/script/urbansun_support.py", INPUTRASTER + fname, tempfile, str(azimuth), str(elevation)])
            arcpy.HillShade_3d(INPUTRASTER + fname, tempfile, str(azimuth), str(elevation), "SHADOWS", "1")   
            #print "done with hillsahde"
            
            
            srcin = gdal.Open(tempfile, gdal.GA_ReadOnly)
            bandin = srcin.GetRasterBand(1)
            arin = bandin.ReadAsArray()
            #now shadows will be zero
            #arin = arin - 1
            tempin = np.array(arin, np.bool)
            #print tempin
            arout = tempin + arout
            #print arout
            del srcin, bandin,arin
            try:
                stemp = tempfile.strip(".tif")
                os.remove(stemp + ".tfw")
                os.remove(stemp + ".tif.aux.xml")
                os.remove(stemp + ".tif")
                os.remove(stemp + ".tif.vat.dbf")
                os.remove(stemp + ".tif.xml")
            except:
                time.sleep(2)
                try:
                    os.remove(stemp + ".tfw")
                    os.remove(stemp + ".tif.aux.xml")
                    os.remove(stemp + ".tif")
                    os.remove(stemp + ".tif.vat.dbf")
                    os.remove(stemp + ".tif.xml")
                except:
                    print "file failed", tempfile
            
            print "finished", str(datetime.fromtimestamp(currenttime).strftime('%Y-%m-%d %H:%M:%S'))        
            
            #add one hour
            currenttime += 3600
        #print arout
        print "writing bandout"
        print arout
        bandout.WriteArray(arout)
        del srcout, bandout, arout
        currentweektime += ONEWEEK






