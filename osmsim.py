#简化osm道路网
#参考https://zhuanlan.zhihu.com/p/384373379
#author:Grimme
#time:20221118
import ogr

#缓冲区
def createBuffer(inShp, outbuffershap, distance):
    """
    :param inShp: 输入的矢量路径
    :param outbuffershap: 输出的矢量路径
    :param distance: 缓冲区距离
    :return:
    """
    ogr.UseExceptions()
    in_ds = ogr.Open(inShp)
    in_lyr = in_ds.GetLayer()
    # 创建输出文件
    driver = ogr.GetDriverByName('ESRI Shapefile')
    out_ds = driver.CreateDataSource(outbuffershap)
    out_lyr = out_ds.CreateLayer(
        outbuffershap, in_lyr.GetSpatialRef(), ogr.wkbPolygon)
    def_feature = out_lyr.GetLayerDefn()
    # 读取Shapefile每个要素进行Buffer操作
    for feature in in_lyr:
        geometry = feature.GetGeometryRef()
        buffer = geometry.Buffer(distance)
        out_feature = ogr.Feature(def_feature)
        out_feature.SetGeometry(buffer)
        out_lyr.CreateFeature(out_feature)
        out_feature = None
    out_ds.FlushCache()
    del in_ds, out_ds
