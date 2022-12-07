from urllib.parse import quote
from urllib import request
import json
import os
import xlwt
import pandas as pd
from .transCoordinateSystem import gcj02_to_wgs84, gcj02_to_bd09
from .shp import trans_point_to_shp

'''
版本更新说明：

2019.10.05：
    1. 数据导出格式支持CSV格式以及XLS两种格式;
    2. 支持同时采集多个城市的POI数据;
    3. 支持同时采集多个POI分类数据

2019.10.10:
    1. 数据导出支持CSV以及XLS两种格式;
    2. CSV格式数据会生成.shp文件，可以直接在ARCGIS中使用

2020.06.19:
    1.清除了poi数据写入shp文件相关操作
    2.修改为根据POI分类关键字来爬取，而不是分类编码
'''
#27575d4349354309657877df2346fc63
#################################################需要修改###########################################################

# TODO 1.替换为从高德开放平台上申请申请的密钥
amap_web_key = 'b2324012020e39c37fd55fcd2050aded'

# TODO 2.分类关键字,最好对照<<高德地图POI分类关键字以及编码.xlsx>>来填写对应分类关键字(不是编码)，多个用逗号隔开
keyword = ['旅游专线车站','普通公交站','机场巴士','班车站','停车场相关','换乘停车场','公共停车场','专用停车场','路边停车场','停车场入口','停车场出口','停车场出入口','过境口岸','出租车','轮渡站','索道站','金融保险机构','银行','中国人民银行','国家开发银行','中国进出口银行','中国银行','中国工商银行','中国建设银行','中国农业银行','交通银行','招商银行','华夏银行','中信银行','中国民生银行','中国光大银行','上海银行','上海浦东发展银行','平安银行','兴业银行','北京银行','广发银行','农村商业银行','香港恒生银行','东亚银行','花旗银行','渣打银行','汇丰银行','荷兰银行','美国运通银行','瑞士友邦银行','美国银行','蒙特利尔银行','纽约银行','苏格兰皇家银行','法国兴业银行','德意志银行','日本三菱东京日联银行','巴克莱银行','摩根大通银行','中国邮政储蓄银行','香港星展银行','南洋商业银行','上海商业银行','永亨银行','香港永隆银行','创兴银行','大新银行','中信银行(国际)','大众银行(香港)','北京农商银行','上海农商银行','广州农商银行','深圳农村商业银行','银行相关','自动提款机','中国银行ATM','中国工商银行ATM','中国建设银行ATM','中国农业银行ATM','交通银行ATM','招商银行ATM','华夏银行ATM','中信银行ATM','中国民生银行ATM','中国光大银行ATM','上海银行ATM','上海浦东发展银行ATM','平安银行ATM','兴业银行ATM','北京银行ATM','广发银行ATM','农村商业银行ATM','香港恒生银行ATM','东亚银行ATM','花旗银行ATM','渣打银行ATM','汇丰银行ATM','荷兰银行ATM','美国运通银行ATM','瑞士友邦银行ATM','美国银行ATM','蒙特利尔银行ATM','纽约银行ATM','苏格兰皇家银行ATM','法国兴业银行ATM','德意志银行ATM','日本三菱东京日联银行ATM','巴克莱银行ATM','摩根大通银行ATM','中国邮政储蓄银行ATM','香港星展银行ATM','南洋商业银行ATM','上海商业银行ATM','永亨银行ATM','香港永隆银行ATM','创兴银行ATM','大新银行ATM','中信银行(国际)ATM','大众银行(香港)ATM','北京农商银行ATM','上海农商银行ATM','广州农商银行ATM','深圳农村商业银行ATM','保险公司','中国人民保险公司','中国人寿保险公司','中国平安保险公司','中国再保险公司','中国太平洋保险','新华人寿保险公司','华泰财产保险股份有限公司','泰康人寿保险公司','证券公司','证券营业厅','财务公司','公司企业','知名企业','公司','广告装饰','建筑公司','医药公司','机械电子','冶金化工','网络科技','商业贸易','电信公司','矿产公司','工厂','其它农林牧渔基地','渔场','农场','林场','牧场','家禽养殖基地','蔬菜基地','水果基地','花卉苗圃基地','道路附属设施','警示信息','摄像头','测速设施','铁路道口','违章停车','收费站','高速收费站','国省道收费站','桥洞收费站','高速服务区','高速加油站服务区','高速停车区','红绿灯','路牌信息','地名地址信息','普通地名','国家名','省级地名','直辖市级地名','地市级地名','区县级地名','乡镇级地名','街道级地名','村庄级地名','村组级地名','自然地名','海湾海峡','岛屿','山','河流','湖泊','交通地名','道路名','路口名','环岛名','高速路出口','高速路入口','立交桥','桥','城市快速路出口','城市快速路入口','隧道','铁路','门牌信息','地名门牌','道路门牌','楼栋号','城市中心','标志性建筑物','热点地名','公共设施','报刊亭','公用电话','公共厕所','男洗手间','女洗手间','残障洗手间无障碍洗手间','婴儿换洗间哺乳室母婴室','紧急避难场所','事件活动','公众活动','节日庆典','展会展览','体育赛事','文艺演出','大型会议','运营活动','商场活动','突发事件','自然灾害','事故灾难','城市新闻','公共卫生事件','公共社会事件','室内设施','通行设施','建筑物门','建筑物正门','临街院门','临街院正门','虚拟门']
# TODO 3.城市，多个用逗号隔开
city = ['洪山区']

# TODO 4.输出数据坐标系,1为高德GCJ20坐标系，2WGS84坐标系，3百度BD09坐标系
coord = 2

# TODO 5. 输出数据文件格式,1为默认xls格式，2为csv格式
data_file_format = 2

############################################以下不需要动#######################################################################


poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        print(result)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break

        hand(poilist, result)
        i = i + 1
    return poilist


# 数据写入excel
def write_to_excel(poilist, cityname, classfield):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)

    # 第一行(列标题)
    sheet.write(0, 0, 'lon')
    sheet.write(0, 1, 'lat')
    sheet.write(0, 2, 'name')
    sheet.write(0, 3, 'address')
    sheet.write(0, 4, 'pname')
    sheet.write(0, 5, 'cityname')
    sheet.write(0, 6, 'business_area')
    sheet.write(0, 7, 'type')

    for i in range(len(poilist)):
        location = poilist[i].get('location')
        name = poilist[i].get('name')
        address = poilist[i].get('address')
        pname = poilist[i].get('pname')
        cityname = poilist[i].get('cityname')
        business_area = poilist[i].get('business_area')
        type = poilist[i].get('type')
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]

        if (coord == 2):
            result = gcj02_to_wgs84(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        if (coord == 3):
            result = gcj02_to_bd09(float(lng), float(lat))
            lng = result[0]
            lat = result[1]

        # 每一行写入
        sheet.write(i + 1, 0, lng)
        sheet.write(i + 1, 1, lat)
        sheet.write(i + 1, 2, name)
        sheet.write(i + 1, 3, address)
        sheet.write(i + 1, 4, pname)
        sheet.write(i + 1, 5, cityname)
        sheet.write(i + 1, 6, business_area)
        sheet.write(i + 1, 7, type)


    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'data' + os.sep + 'poi-' + cityname + "-" + classfield + ".xls")


# 数据写入csv文件中
def write_to_csv(poilist, cityname, classfield):
    data_csv = {}
    lons, lats, names, addresss, pnames, citynames, business_areas, types = [], [], [], [], [], [], [], []

    for i in range(len(poilist)):
        print('===================')
        print(poilist[i])
        location = poilist[i].get('location')
        name = poilist[i].get('name')
        address = poilist[i].get('address')
        pname = poilist[i].get('pname')
        cityname = poilist[i].get('cityname')
        business_area = poilist[i].get('business_area')
        type = poilist[i].get('type')
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]

        if (coord == 2):
            result = gcj02_to_wgs84(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        if (coord == 3):
            result = gcj02_to_bd09(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        lons.append(lng)
        lats.append(lat)
        names.append(name)
        addresss.append(address)
        pnames.append(pname)
        citynames.append(cityname)
        if business_area == []:
            business_area = ''
        business_areas.append(business_area)
        types.append(type)
    data_csv['lon'], data_csv['lat'], data_csv['name'], data_csv['address'], data_csv['pname'], \
    data_csv['cityname'], data_csv['business_area'], data_csv['type'] = \
        lons, lats, names, addresss, pnames, citynames, business_areas, types

    df = pd.DataFrame(data_csv)

    folder_name = 'poi-' + cityname + "-" + classfield
    folder_name_full = 'data' + os.sep + folder_name + os.sep
    if os.path.exists(folder_name_full) is False:
        os.makedirs(folder_name_full)

    file_name = 'poi-' + cityname + "-" + classfield + ".csv"
    file_path = folder_name_full + file_name

    df.to_csv(file_path, index=False, encoding='utf_8_sig')
    return folder_name_full, file_name


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    print('============请求url:' + req_url)
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


def get_areas(code):
    '''
    获取城市的所有区域
    :param code:
    :return:
    '''

    print('获取城市的所有区域：code: ' + str(code).strip())
    data = get_distrinctNoCache(code)

    print('get_distrinct result:' + data)

    data = json.loads(data)

    districts = data['districts'][0]['districts']
    # 判断是否是直辖市
    # 北京市、上海市、天津市、重庆市。
    if (code.startswith('重庆') or code.startswith('上海') or code.startswith('北京') or code.startswith('天津')):
        districts = data['districts'][0]['districts'][0]['districts']

    i = 0
    area = ""
    for district in districts:
        name = district['name']
        adcode = district['adcode']
        i = i + 1
        area = area + "," + adcode

    print(area)
    print(str(area).strip(','))
    return str(area).strip(',')


def get_data(city, keyword):
    '''
    根据城市名以及POI类型爬取数据
    :param city:
    :param keyword:
    :return:
    '''
    isNeedAreas = True
    if isNeedAreas:
        area = get_areas(city)
    all_pois = []
    if area != None and area != "":
        area_list = str(area).split(",")
        if area_list == 0:
            area_list = str(area).split("，")

        for area in area_list:
            pois_area = getpois(area, keyword)
            print('当前城区：' + str(area) + ', 分类：' + str(keyword) + ", 总的有" + str(len(pois_area)) + "条数据")
            all_pois.extend(pois_area)
        print("所有城区的数据汇总，总数为：" + str(len(all_pois)))
        if data_file_format == 2:
            # 写入CSV
            file_folder, file_name = write_to_csv(all_pois, city, keyword)
            # 写入SHP
            #trans_point_to_shp(file_folder, file_name, 0, 1)
            return
        return write_to_excel(all_pois, city, keyword)
    else:
        pois_area = getpois(city, keyword)
        if data_file_format == 2:
            # 写入CSV
            file_folder, file_name = write_to_csv(all_pois, city, keyword)
            # 写入SHP
            #trans_point_to_shp(file_folder, file_name, 0, 1)
            return
        return write_to_excel(pois_area, city, keyword)

    return None


def get_distrinctNoCache(code):
    '''
    获取中国城市行政区划
    :return:
    '''

    url = "https://restapi.amap.com/v3/config/district?subdistrict=2&extensions=all&key=" + amap_web_key

    req_url = url + "&keywords=" + quote(code)

    print(req_url)

    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    print(code, data)
    return data


if __name__ == '__main__':

    for ct in city:
        for type in keyword:
            get_data(ct, type)
    print('总的', len(city), '个城市, ', len(keyword), '个分类数据全部爬取完成!')

