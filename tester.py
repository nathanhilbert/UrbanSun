from osgeo import gdal
import numpy

outputfile = "D:/GIS Project Data/Lidar Testing/Ben/finaloutput/tempraster1_1325394000.tif"

srcout = gdal.Open(outputfile, gdal.GA_Update)
bandout = srcout.GetRasterBand(1)
arout = bandout.ReadAsArray()