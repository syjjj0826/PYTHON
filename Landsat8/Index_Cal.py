import gdal
import numpy as np

''' 对应波段
Band1可见  沿海、气溶胶（0.43-0.45 µm）30 m
Band2可见  蓝色（0.450-0.51 µm）30 m
Band3可见  绿色（0.53-0.59 µm）30 m
Band4可见  红色（0.64-0.67 µm）30 m
Band5近红外  NIR （0.85-0.88 µm）30 m
Band6短波长红外1  SWIR1（1.57-1.65 µm）30 m
Band7短波长红外2  SWIR2（2.11-2.29 µm）30 m
Band8全色（PAN）（0.50-0.68 µm）15 m
Band9卷云（1.36-1.38 µm）30 m
Band10 TIRS 长波长红外1（10.6-11.19 µm）100 m
Band11 TIRS 长波长红外2（11.5-12.51 µm）100 m
'''


def read_image(input_path):
    try:
        gdal.SetConfigOption("GDAL_file_name_IS_UTF8", "YES")  # 用于处理gdal中文乱码
        dataset = gdal.Open(input_path, 0)
        if dataset is None:
            print('could not open')
        else:
            im_width = dataset.RasterXSize  # 栅格数据的宽度(栅格矩阵的列数)
            im_height = dataset.RasterYSize  # 栅格数据的高度(栅格矩阵的行数)
            im_data = dataset.ReadAsArray(0, 0, im_width, im_height).astype(np.float32)  # 将数据写成数组
            im_geotrans = dataset.GetGeoTransform()  # 栅格数据的六参数(仿射矩阵)
            im_proj = dataset.GetProjection()  # 栅格数据的投影（地图投影信息）
            nodata = dataset.GetRasterBand(1).GetNoDataValue()

        del dataset  # 关闭对象

        return im_width, im_height, im_data, im_geotrans, im_proj, nodata
    except BaseException as e:  # 抛出异常的处理
        print(str(e))


def write_img(im_data, im_geotrans, im_proj, nodata, output_path):
    try:
        gdal.SetConfigOption("GDAL_file_name_IS_UTF8", "YES")
        # 判断栅格数据的数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32
        # 判读数组维数
        if len(im_data.shape) <= 2:
            im_bands, (im_height, im_width) = 1, im_data.shape
        else:
            im_bands, im_height, im_width = im_data.shape

        # 创建文件
        driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
        dataset = driver.Create(output_path, im_width, im_height, im_bands, datatype)
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影

        if im_bands == 1:
            dataset.GetRasterBand(1).SetNoDataValue(nodata)
            dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i + 1).SetNoDataValue(nodata)
                dataset.GetRasterBand(i + 1).WriteArray(im_data[i])

        del dataset

    except BaseException as e:
        print(str(e))


def GetNDVI(nir_data, red_data):
    try:
        denominator = np.array(nir_data + red_data, dtype=np.float32)
        numerator = np.array(nir_data - red_data, dtype=np.float32)
        nodata = np.full((nir_data.shape[0], nir_data.shape[1]), -999.0, dtype=np.float32)
        ndvi = np.divide(numerator, denominator, out=nodata, where=denominator != 0.0)
        # mask = np.greater(nir_data + red_data, 0.0)
        # ndvi = np.choose(mask,(-999.0,(nir_data-red_data)*1.0/(nir_data+red_data)))
        return ndvi

    except BaseException as e:
        print(str(e))


def GetEVI(nir_data, red_data, blue_data):
    try:
        # (2.5*(NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1 + 1E-6))
        denominator = np.array(nir_data + 6 * red_data - 7.5 * blue_data + 1, dtype=np.float32)
        numerator = np.array(2.5 * (nir_data - red_data), dtype=np.float32)
        nodata = np.full((nir_data.shape[0], nir_data.shape[1]), -999.0, dtype=np.float32)
        EVI = np.divide(numerator, denominator, out=nodata, where=denominator != 0.0)
        # mask = np.greater(nir_data + red_data, 0.0)
        # ndvi = np.choose(mask,(-999.0,(nir_data-red_data)*1.0/(nir_data+red_data)))
        return EVI

    except BaseException as e:
        print(str(e))


def GetNDBI(nir_data, swir1_data):
    try:
        denominator = np.array(swir1_data + nir_data, dtype=np.float32)
        numerator = np.array(swir1_data - nir_data, dtype=np.float32)
        nodata = np.full((nir_data.shape[0], nir_data.shape[1]), -999.0, dtype=np.float32)
        ndbi = np.divide(numerator, denominator, out=nodata, where=denominator != 0.0)
        # mask = np.greater(nir_data + red_data, 0.0)
        # ndvi = np.choose(mask,(-999.0,(nir_data-red_data)*1.0/(nir_data+red_data)))
        return ndbi

    except BaseException as e:
        print(str(e))


def GetMNDWI(nir_data, green_data):
    try:
        denominator = np.array(green_data + nir_data, dtype=np.float32)
        numerator = np.array(green_data - nir_data, dtype=np.float32)
        nodata = np.full((nir_data.shape[0], nir_data.shape[1]), -999.0, dtype=np.float32)
        ndwi = np.divide(numerator, denominator, out=nodata, where=denominator != 0.0)
        # mask = np.greater(nir_data + red_data, 0.0)
        # ndvi = np.choose(mask,(-999.0,(nir_data-red_data)*1.0/(nir_data+red_data)))
        return ndwi

    except BaseException as e:
        print(str(e))


if __name__ == '__main__':
    # 图像的输入路径以及输出路径
    input_path = r"G:\Data\Landsat8\Data\Landsat8\2020\Re\RE_LC08_L1TP_123039_20201225_20210310_ALL.tif"

    # 读取波段数据
    im_width, im_height, im_data, im_geotrans, im_proj, nodata = read_image(input_path)

    blue_data = im_data[1]
    green_data = im_data[2]
    red_data = im_data[3]
    nir_data = im_data[4]
    swir1_data = im_data[5]
    swir2_data = im_data[6]
    nodata = -999

    # 写NDVI数据
    ndvi_output_path = r"G:\Data\Landsat8\Data\Landsat8\2020\Re\NDVI.tif"
    ndvi_data = GetNDVI(nir_data, red_data)
    # ndvi_result = np.where(ndvi_data > 1, -999.0, ndvi_data)
    write_img(ndvi_data, im_geotrans, im_proj, nodata, ndvi_output_path)
    print("Cal NDVI :", ndvi_output_path, "Success.")

    # 写EVI数据
    evi_output_path = r"G:\Data\Landsat8\Data\Landsat8\2020\Re\EVI.tif"
    evi_data = GetEVI(nir_data, red_data, blue_data)
    write_img(evi_data, im_geotrans, im_proj, nodata, evi_output_path)
    print("Cal EVI :", evi_output_path, "Success.")

    # 写NDBI数据
    ndbi_output_path = r"G:\Data\Landsat8\Data\Landsat8\2020\Re\NDBI.tif"
    ndbi_data = GetNDBI(nir_data, swir1_data)
    write_img(ndbi_data, im_geotrans, im_proj, nodata, ndbi_output_path)
    print("Cal NDBI :", ndbi_output_path, "Success.")

    # 写MNDWI数据
    mndwi_output_path = r"G:\Data\Landsat8\Data\Landsat8\2020\Re\MNDWI.tif"
    mndwi_data = GetMNDWI(nir_data, green_data)
    write_img(mndwi_data, im_geotrans, im_proj, nodata, mndwi_output_path)
    print("Cal MNDWI :", mndwi_output_path, "Success.")
