import os, sys
import landsatxplore.api
from landsatxplore.earthexplorer import EarthExplorer
import geopandas as gpd
import warnings
import subprocess

warnings.filterwarnings(action="ignore")

username = 'Grimmesyj'  # 输入EE账号
password = 'Grimmesyj_1016'  # 输入账号密码
# 初始化API接口获取key
api = landsatxplore.api.API(username, password)


# 影像查询
def search_image(search_file, dataset, start_date, end_date, max_cloud_cover):
    # 输入要查询的边界
    data = gpd.read_file(search_file)
    # 输入轨道矢量
    if dataset.lower() == "sentinel_2a":
        grid_file = r'G:\Data\Landsat8\GridFile\sentinel2_grid.shp'
    elif dataset.lower() == "landsat_8_c1":
        # 输入landsat轨道矢量
        grid_file = r'G:\Data\Landsat8\GridFile\WRS2_descending.shp'
    wrs = gpd.GeoDataFrame.from_file(grid_file)
    # 查询边界覆盖的轨道中心坐标
    wrs_intersection = wrs[wrs.intersects(data.geometry[0])]
    longitude = (wrs_intersection.centroid).x.values
    latitude = (wrs_intersection.centroid).y.values
    # print(longitude, latitude)

    # 查询
    all_scene = []
    for i in range(len(latitude)):
        scenes = api.search(dataset=dataset, latitude=latitude[i], longitude=longitude[i],
                            start_date=start_date, end_date=end_date, max_cloud_cover=max_cloud_cover)
        all_scene += scenes
    print('{} scenes found.'.format(len(all_scene)))
    api.logout()
    return all_scene


# 下载影像数据
def Download_from_Landsatexplore(dataset, scene_list,username, password):
    if len(scene_list) > 0:
        ee = EarthExplorer(username, password)
        # 根据ID下载影像
        if dataset.lower() == "landsat_8_c1":
            output_dir = r'G:\Data\Landsat8\Data\Landsat8'  # 输入下载路径
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        elif dataset.lower() == "sentinel_2a":
            output_dir = r'G:\Data\Landsat8\Data\Sentinel2'  # 输入下载路径
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        for scene in scene_list:
            output_dir_demon = output_dir + '\\' + str(scene['acquisition_date'].year)
            if not os.path.isdir(output_dir_demon):
                os.mkdir(output_dir_demon)
            # ee = EarthExplorer(username, password)

            print("Downloading: " + scene['display_id'])
            # url = ee.download(identifier=scene['entity_id'], output_dir=output_dir_demon)
            # cmd = "wget --http-user="+str(username)+" --http-password="+ str(password)+ " " + str(url)
            # subprocess.call(cmd)
            ee.download(identifier=scene['entity_id'], output_dir=output_dir_demon)


        ee.logout()


if __name__ == '__main__':
    """Landsat 5 TM Collection 1 Level 1-->landsat_tm_c1
        Landsat 5 TM Collection 2 Level 1-->landsat_tm_c2_l1
        Landsat 5 TM Collection 2 Level 2-->landsat_tm_c2_l2
        Landsat 7 ETM+ Collection 1 Level 1-->landsat_etm_c1
        Landsat 7 ETM+ Collection 2 Level 1-->landsat_etm_c2_l1
        Landsat 7 ETM+ Collection 2 Level 2-->landsat_etm_c2_l2
        Landsat 8 Collection 1 Level 1-->landsat_8_c1
        Landsat 8 Collection 2 Level 1-->landsat_ot_c2_l1
        Landsat 8 Collection 2 Level 2-->landsat_ot_c2_l2
        Sentinel 2A-->sentinel_2a"""
    # 输入查询条件
    """ 
    dataset = sys.argv[1]#'landsat_8_c1' # 数据集
    start_date = sys.argv[2]#'2021-05-01' # 开始日期
    end_date = sys.argv[3]#'2021-05-20' # 结束日期
    cloud_cover = sys.argv[4]#15 # 云量(%)
    """
    dataset = 'LANDSAT_8_C1'  # 数据集
    start_date = '2020-12-01'  # 开始日期
    end_date = '2020-12-30'  # 结束日期
    cloud_cover = 20  # 云量（%）
    # 输入查询文件
    search_file = "G:/Data/Landsat8/areashp/WuhanArea.shp"  # 输入查询矢量

    # 查询数据
    search_list = search_image(search_file, dataset, start_date, end_date, cloud_cover)

    # 下载数据
    Download_from_Landsatexplore(dataset, search_list, username, password)
