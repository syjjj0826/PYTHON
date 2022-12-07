import cv2 as cv
import numpy as np
import os
from osgeo import gdal

src_img = r"G:\Data\test\VIIRS_vcmslcfg_201806.tif"
# src_img = r"G:\Data\LuoJia1-01\wuhan_20180613/LuoJia1-01_LR201806.tif"
count = 1
img_src = gdal.Open(src_img)
Geotransform = img_src.GetGeoTransform()
projection = img_src.GetProjection()
cols = img_src.RasterXSize
rows = img_src.RasterYSize
Band = img_src.GetRasterBand(1)
Data = Band.ReadAsArray(0, 0, cols, rows)
NoData = Band.GetNoDataValue()
print("OriImg Shape: ", cols," × ",rows,
      "\nOriImg MinValue_MaxValue: ", Data.min(), "~", Data.max())
print(Data)

save_dir = os.path.join(os.path.dirname(src_img), "OriDataset")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
for x in range(0, cols-32, 32):
    for y in range(0, rows-32, 32):
        print(x,y)
        wData = Data[x:x + 32, y:y + 32]
        print(wData)
        save_img = os.path.join(save_dir, "ntl_{}.tif".format(count))
        count += 1
        # wGeotransform = Geotransform
        Geotransformlist = list(Geotransform)
        Geotransformlist[0] = Geotransform[0] + Geotransform[1] * x
        Geotransformlist[3] = Geotransform[3] + Geotransform[5] * y
        wGeotransform = tuple(Geotransformlist)
        print(wGeotransform)

        format = "GTiff"
        driver = gdal.GetDriverByName(format)
        ds = driver.Create(save_img, 32, 32, 1, gdal.GDT_Float32)
        ds.SetGeoTransform(wGeotransform)

        ds.SetProjection(projection)
        ds.GetRasterBand(1).SetNoDataValue(-9999)
        ds.GetRasterBand(1).WriteArray(wData)
        ds = None