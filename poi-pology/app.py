#! /usr/local/bin/python3
# coding: utf-8
# __author__ = "Liu jiao"
# __date__ = 2019/10/16 16:11


from urllib.parse import quote
import json
import os
from transCoordinateSystem import gcj02_to_wgs84, gcj02_to_bd09
import area_boundary as  area_boundary
import city_grid as city_grid
import time
import collections
import pandas as pd
from requests.adapters import HTTPAdapter
import requests

#from shp import trans_point_to_shp


'''
版本更新说明：
2020.06.19:
    1.清除了poi数据写入shp文件相关操作

'''

#################################################需要修改###########################################################

## TODO 1.划分的网格距离，0.02-0.05最佳，建议如果是数量比较多的用0.01或0.02，如餐厅，企业。数据量少的用0.05或者更大，如大学
pology_split_distance = 0.02

## TODO 2. 城市编码，参见高德城市编码表，注意需要用adcode列的编码
city_code = '370100'

## TODO 3. POI类型编码，类型名或者编码都行，具体参见《高德地图POI分类编码表.xlsx》
# typs = ['汽车服务相关','加油站','中国石化','中国石油','壳牌','美孚','加德士','东方','中石油碧辟','中石化碧辟','道达尔','埃索','中化道达尔','其它能源站','加气站','汽车养护','加水站','洗车场','汽车俱乐部','汽车救援','汽车配件销售','汽车租赁','汽车租赁还车','二手车交易','充电站','汽车销售','大众销售','上海大众销售','一汽-大众销售','斯柯达销售','进口大众销售','宾利销售','兰博基尼销售','本田销售','广汽本田销售','东风本田销售','本田讴歌销售','奥迪销售','一汽-大众奥迪销售','通用销售','凯迪拉克销售','别克销售','雪佛兰销售','欧宝销售','萨博销售','沃克斯豪尔销售','土星销售','大宇销售','宝马销售','宝马MINI销售','劳斯莱斯销售','日产销售','东风日产销售','郑州日产销售','英菲尼迪销售','雷诺销售','梅赛德斯-奔驰销售','迈巴赫销售','精灵销售','丰田销售','一汽丰田销售','广汽丰田销售','雷克萨斯销售','大发销售','斯巴鲁销售','雪铁龙销售','东风雪铁龙销售','东风标致销售','DS销售','三菱销售','广汽三菱销售','菲亚特销售','阿尔法-罗密欧销售','法拉利销售','玛莎拉蒂销售','现代销售','进口现代销售','北京现代销售','起亚销售','进口起亚销售','东风悦达起亚销售','福特销售','马自达销售','林肯销售','水星销售','捷豹销售','路虎销售','保时捷销售','东风销售','吉利销售','沃尔沃汽车销售','奇瑞销售','克莱斯勒销售','吉普销售','道奇销售','荣威销售','名爵销售','江淮销售','红旗销售','长安汽车销售','海马汽车销售','北京汽车销售','长城汽车销售','魏派汽车销售','纳智捷销售','广汽传祺销售','货车销售','东风货车销售','中国重汽销售','一汽解放销售','福田卡车销售','陕西重汽销售','北奔重汽销售','江淮货车销售','华菱星马销售','成都大运汽车销售','梅赛德斯-奔驰卡车销售','德国曼恩销售','斯堪尼亚销售','沃尔沃卡车销售','观致销售','汽车维修','汽车综合维修','大众维修','上海大众维修','一汽-大众维修','斯柯达维修','进口大众维修','宾利维修','兰博基尼维修','本田维修','广汽本田维修','东风本田维修','本田讴歌维修','奥迪维修','一汽-大众奥迪维修','通用维修','凯迪拉克维修','别克维修','雪佛兰维修','欧宝维修','萨博维修','沃克斯豪尔维修','土星维修','大宇维修','宝马维修','宝马MINI维修','劳斯莱斯维修','日产维修','英菲尼迪维修','东风日产维修','郑州日产维修','雷诺维修','梅赛德斯-奔驰维修','迈巴赫维修','精灵维修','丰田维修','一汽丰田维修','广汽丰田维修','雷克萨斯维修','大发维修','斯巴鲁维修','雪铁龙维修','东风标致维修','东风雪铁龙维修','DS维修','三菱维修','广汽三菱维修','菲亚特维修','阿尔法-罗密欧维修','法拉利维修','玛莎拉蒂维修','现代维修','进口现代维修','北京现代维修','起亚维修','进口起亚维修','东风悦达起亚维修','福特维修','马自达维修','林肯维修','水星维修','捷豹维修','路虎维修','保时捷维修','东风维修','吉利维修','沃尔沃汽车维修','奇瑞维修','克莱斯勒维修','吉普维修','道奇维修','荣威维修','名爵维修','江淮维修','红旗维修','长安汽车维修','海马汽车维修','北京汽车维修','长城汽车维修','魏派汽车维修','纳智捷维修','广汽传祺维修','货车维修','东风货车维修','中国重汽维修','一汽解放维修','福田卡车维修','陕西重汽维修','北奔重汽维修','江淮货车维修','华菱星马维修','成都大运汽车维修','梅赛德斯-奔驰卡车维修','德国曼恩维修','斯堪尼亚维修','沃尔沃卡车维修','观致维修','摩托车服务相关','摩托车销售','宝马摩托车销售','摩托车维修','宝马摩托车维修','餐饮相关','中餐厅','综合酒楼','四川菜(川菜)','广东菜(粤菜)','山东菜(鲁菜)','江苏菜','浙江菜','上海菜','湖南菜(湘菜)','安徽菜(徽菜)','福建菜','北京菜','湖北菜(鄂菜)','东北菜','云贵菜','西北菜','老字号','火锅店','特色地方风味餐厅','海鲜酒楼','中式素菜馆','清真菜馆','台湾菜','潮州菜','外国餐厅','西餐厅(综合风味)','日本料理','韩国料理','法式菜品餐厅','意式菜品餐厅','泰国越南菜品餐厅','地中海风格菜品','美式风味','印度风味','英国式菜品餐厅','牛扒店(扒房)','俄国菜','葡国菜','德国菜','巴西菜','墨西哥菜','其它亚洲菜','快餐厅','肯德基','麦当劳','必胜客','永和豆浆','茶餐厅','大家乐','大快活','美心','吉野家','仙跡岩','呷哺呷哺','休闲餐饮场所','咖啡厅','星巴克咖啡','上岛咖啡','Pacific Coffee Company','巴黎咖啡店','茶艺馆','冷饮店','糕饼店','甜品店','购物相关场所','商场','购物中心','普通商场','免税品店','便民商店便利店','7-ELEVEn便利店','OK便利店','家电电子卖场','综合家电商场','国美','大中','苏宁','手机销售','数码电子','丰泽','苏宁镭射','超市','家乐福','沃尔玛','华润','北京华联','上海华联','麦德龙','乐天玛特','华堂','卜蜂莲花','屈臣氏','惠康超市','百佳超市','万宁超市','花鸟鱼虫市场','花卉市场','宠物市场','家居建材市场','家具建材综合市场','家具城','建材五金市场','厨卫市场','布艺市场','灯具瓷器市场','综合市场','小商品市场','旧货市场','农副产品市场','果品市场','蔬菜市场','水产海鲜市场','文化用品店','体育用品店','李宁专卖店','耐克专卖店','阿迪达斯专卖店','锐步专卖店','彪马专卖店','高尔夫用品店','户外用品','特色商业街','步行街','服装鞋帽皮具店','品牌服装店','品牌鞋店','品牌皮具店','品牌箱包店','专营店','古玩字画店','珠宝首饰工艺品','钟表店','眼镜店','书店','音像店','儿童用品店','自行车专卖店','礼品饰品店','烟酒专卖店','宠物用品店','摄影器材店','宝马生活方式','土特产专卖店','特殊买卖场所','拍卖行','典当行','其它个人用品店','莎莎','生活服务场所','旅行社','信息咨询中心','服务中心','旅馆问讯','行李查询行李问询','售票处','飞机票代售点','火车票代售点','长途汽车票代售点','船票代售点','公交卡月票代售点','公园景点售票处','邮局','邮政速递','物流速递','物流仓储场地','电讯营业厅','中国电信营业厅','中国移动营业厅','中国联通营业厅','中国铁通营业厅','中国卫通营业厅','和记电讯','数码通电讯','电讯盈科','中国移动香港','事务所','律师事务所','会计师事务所','评估事务所','审计事务所','认证事务所','专利事务所','人才市场','自来水营业厅','电力营业厅','美容美发店','维修站点','摄影冲印','洗浴推拿场所','洗衣店','中介机构','搬家公司','彩票彩券销售点','马会投注站','丧葬设施','陵园','公墓','殡仪馆','婴儿服务场所','婴儿游泳馆','体育休闲服务场所','运动场所','综合体育馆','保龄球馆','网球场','篮球场馆','足球场','滑雪场','溜冰场','户外健身场所','海滨浴场','游泳馆','健身中心','乒乓球馆','台球厅','壁球场','马术俱乐部','赛马场','橄榄球场','羽毛球场','跆拳道场馆','高尔夫相关','高尔夫球场','高尔夫练习场','娱乐场所','夜总会','KTV','迪厅','酒吧','游戏厅','棋牌室','博彩中心','网吧','度假疗养场所','度假村','疗养院','休闲场所','游乐场','垂钓园','采摘园','露营地','水上活动中心','影剧院相关','电影院','音乐厅','剧场','医疗保健服务场所','综合医院','三级甲等医院','卫生院','专科医院','整形美容','口腔医院','眼科医院','耳鼻喉医院','胸科医院','骨科医院','肿瘤医院','脑科医院','妇科医院','精神病医院','传染病医院','诊所','急救中心','疾病预防','医药保健相关','药房','医疗保健用品','动物医疗场所','宠物诊所','兽医站','住宿服务相关','宾馆酒店','奢华酒店','五星级宾馆','四星级宾馆','三星级宾馆','经济型连锁酒店','旅馆招待所','青年旅舍','旅游景点','公园广场','公园','动物园','植物园','水族馆','城市广场','公园内部设施','风景名胜','世界遗产','国家级景点','省级景点','纪念馆','寺庙道观','教堂','回教寺','海滩','观景点','商务住宅相关','产业园区','楼宇相关','商务写字楼','工业大厦建筑物','商住两用楼宇','住宅区','别墅','住宅小区','宿舍','社区中心','政府及社会团体相关','政府机关相关','国家级机关及事业单位','省直辖市级政府及事业单位','地市级政府及事业单位','区县级政府及事业单位','乡镇级政府及事业单位','乡镇以下级政府及事业单位','外地政府办','外国机构相关','外国使领馆','国际组织办事处','民主党派','社会团体相关','共青团','少先队','妇联','残联','红十字会','消费者协会','行业协会','慈善机构','教会','公检法机关','公安警察','检察院','法院','消防机关','公证鉴定机构','社会治安机构','交通车辆管理相关','交通管理机构','车辆管理机构','验车场','交通执法站','车辆通行证办理处','货车相关检查站','工商税务机构','工商部门','国税机关','地税机关','科教文化场所','博物馆','奥迪博物馆','梅赛德斯-奔驰博物馆','展览馆','室内展位','会展中心','美术馆','图书馆','科技馆','天文馆','文化宫','档案馆','文艺团体','传媒机构','电视台','电台','报社','杂志社','出版社','学校','高等院校','中学','小学','幼儿园','成人教育','职业技术学校','学校内部设施','科研机构','培训机构','驾校','交通服务相关','机场相关','候机室','摆渡车站','飞机场','机场出发到达','直升机场','机场货运处','火车站','候车室','进站口检票口','出站口','站台','售票','退票','改签','公安制证','票务相关','货运火车站','港口码头','客运港','车渡口','人渡口','货运港口码头','长途汽车站','地铁站','出入口','轻轨站','公交车站相关','旅游专线车站','普通公交站','机场巴士','班车站','停车场相关','换乘停车场','公共停车场','专用停车场','路边停车场','停车场入口','停车场出口','停车场出入口','过境口岸','出租车','轮渡站','索道站','金融保险机构','银行','中国人民银行','国家开发银行','中国进出口银行','中国银行','中国工商银行','中国建设银行','中国农业银行','交通银行','招商银行','华夏银行','中信银行','中国民生银行','中国光大银行','上海银行','上海浦东发展银行','平安银行','兴业银行','北京银行','广发银行','农村商业银行','香港恒生银行','东亚银行','花旗银行','渣打银行','汇丰银行','荷兰银行','美国运通银行','瑞士友邦银行','美国银行','蒙特利尔银行','纽约银行','苏格兰皇家银行','法国兴业银行','德意志银行','日本三菱东京日联银行','巴克莱银行','摩根大通银行','中国邮政储蓄银行','香港星展银行','南洋商业银行','上海商业银行','永亨银行','香港永隆银行','创兴银行','大新银行','中信银行(国际)','大众银行(香港)','北京农商银行','上海农商银行','广州农商银行','深圳农村商业银行','银行相关','自动提款机','中国银行ATM','中国工商银行ATM','中国建设银行ATM','中国农业银行ATM','交通银行ATM','招商银行ATM','华夏银行ATM','中信银行ATM','中国民生银行ATM','中国光大银行ATM','上海银行ATM','上海浦东发展银行ATM','平安银行ATM','兴业银行ATM','北京银行ATM','广发银行ATM','农村商业银行ATM','香港恒生银行ATM','东亚银行ATM','花旗银行ATM','渣打银行ATM','汇丰银行ATM','荷兰银行ATM','美国运通银行ATM','瑞士友邦银行ATM','美国银行ATM','蒙特利尔银行ATM','纽约银行ATM','苏格兰皇家银行ATM','法国兴业银行ATM','德意志银行ATM','日本三菱东京日联银行ATM','巴克莱银行ATM','摩根大通银行ATM','中国邮政储蓄银行ATM','香港星展银行ATM','南洋商业银行ATM','上海商业银行ATM','永亨银行ATM','香港永隆银行ATM','创兴银行ATM','大新银行ATM','中信银行(国际)ATM','大众银行(香港)ATM','北京农商银行ATM','上海农商银行ATM','广州农商银行ATM','深圳农村商业银行ATM','保险公司','中国人民保险公司','中国人寿保险公司','中国平安保险公司','中国再保险公司','中国太平洋保险','新华人寿保险公司','华泰财产保险股份有限公司','泰康人寿保险公司','证券公司','证券营业厅','财务公司','公司企业','知名企业','公司','广告装饰','建筑公司','医药公司','机械电子','冶金化工','网络科技','商业贸易','电信公司','矿产公司','工厂','其它农林牧渔基地','渔场','农场','林场','牧场','家禽养殖基地','蔬菜基地','水果基地','花卉苗圃基地','道路附属设施','警示信息','摄像头','测速设施','铁路道口','违章停车','收费站','高速收费站','国省道收费站','桥洞收费站','高速服务区','高速加油站服务区','高速停车区','红绿灯','路牌信息','地名地址信息','普通地名','国家名','省级地名','直辖市级地名','地市级地名','区县级地名','乡镇级地名','街道级地名','村庄级地名','村组级地名','自然地名','海湾海峡','岛屿','山','河流','湖泊','交通地名','道路名','路口名','环岛名','高速路出口','高速路入口','立交桥','桥','城市快速路出口','城市快速路入口','隧道','铁路','门牌信息','地名门牌','道路门牌','楼栋号','城市中心','标志性建筑物','热点地名','公共设施','报刊亭','公用电话','公共厕所','男洗手间','女洗手间','残障洗手间无障碍洗手间','婴儿换洗间哺乳室母婴室','紧急避难场所','事件活动','公众活动','节日庆典','展会展览','体育赛事','文艺演出','大型会议','运营活动','商场活动','突发事件','自然灾害','事故灾难','城市新闻','公共卫生事件','公共社会事件','室内设施','通行设施','建筑物门','建筑物正门','临街院门','临街院正门','虚拟门'
# ]  # ['企业', '公园', '广场', '风景名胜', '小学']

## TODO 4. 高德开放平台密钥
gaode_key = ['27575d4349354309657877df2346fc63', 'b2324012020e39c37fd55fcd2050aded']

# TODO 5.输出数据坐标系,1为高德GCJ20坐标系，2WGS84坐标系，3百度BD09坐标系
coord = 2

############################################以下不需要动#######################################################################


poi_pology_search_url = 'https://restapi.amap.com/v3/place/polygon'

buffer_keys = collections.deque(maxlen=len(gaode_key))


def init_queen():
    for i in range(len(gaode_key)):
        buffer_keys.append(gaode_key[i])
    print('当前可供使用的高德密钥：', buffer_keys)


# 根据城市名称和分类关键字获取poi数据
def getpois(grids, keywords):
    if buffer_keys.maxlen == 0:
        print('密钥已经用尽，程序退出！！！！！！！！！！！！！！！')
        exit(0)
    amap_key = buffer_keys[0]  # 总是获取队列中的第一个密钥

    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(grids, keywords, i, amap_key)
        print("当前爬取结果:", result)
        if result != None:
            result = json.loads(result)  # 将字符串转换为json
            try:
                if result['count'] == '0':
                    break
            except Exception as e:
                print('出现异常：', e)

            if result['infocode'] == '10001' or result['infocode'] == '10003':
                print(result)
                print('无效的密钥！！！！！！！！！！！！！，重新切换密钥进行爬取')
                buffer_keys.remove(buffer_keys[0])
                try:
                    amap_key = buffer_keys[0]  # 总是获取队列中的第一个密钥
                except Exception as e:
                    print('密钥已经用尽，程序退出...')
                    exit(0)
                result = getpoi_page(grids, keywords, i, amap_key)
                result = json.loads(result)
            hand(poilist, result)
        i = i + 1
    return poilist


# 数据写入csv文件中
def write_to_csv(poilist, citycode, classfield, coord):
    data_csv = {}
    lons, lats, names, addresss, pnames, citynames, business_areas, types, typecodes, ids, type_1s, type_2s, type_3s, type_4s = [], [], [], [], [], [], [], [], [], [], [], [], [], []

    if len(poilist) == 0:
        print("处理完成，当前citycode:" + str(citycode), ", classfield为：", str(classfield) + "，数据为空，，，结束.......")
        return None, None

    for i in range(len(poilist)):
        location = poilist[i].get('location')
        name = poilist[i].get('name')
        address = poilist[i].get('address')
        pname = poilist[i].get('pname')
        cityname = poilist[i].get('cityname')
        business_area = poilist[i].get('business_area')
        type = poilist[i].get('type')
        typecode = poilist[i].get('typecode')
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]
        id = poilist[i].get('id')

        if (coord == 2):
            result = gcj02_to_wgs84(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        if (coord == 3):
            result = gcj02_to_bd09(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        type_1, type_2, type_3, type_4 = '','','',''
        if str(type) != None and str(type) != '':
            type_strs = type.split(';')
            for i in range(len(type_strs)):
                ty = type_strs[i]
                if i == 0:
                    type_1 = ty
                elif i == 1:
                    type_2 = ty
                elif i == 2:
                    type_3 = ty
                elif i == 3:
                    type_4 = ty

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
        typecodes.append(typecode)
        ids.append(id)
        type_1s.append(type_1)
        type_2s.append(type_2)
        type_3s.append(type_3)
        type_4s.append(type_4)
    data_csv['lon'], data_csv['lat'], data_csv['name'], data_csv['address'], data_csv['pname'], \
    data_csv['cityname'], data_csv['business_area'], data_csv['type'], data_csv['typecode'], data_csv['id'], data_csv[
        'type1'], data_csv['type2'], data_csv['type3'], data_csv['type4'] = \
        lons, lats, names, addresss, pnames, citynames, business_areas, types, typecodes, ids, type_1s, type_2s, type_3s, type_4s

    df = pd.DataFrame(data_csv)

    folder_name = 'poi-' + citycode + "-" + classfield
    folder_name_full = 'data' + os.sep + folder_name + os.sep
    if os.path.exists(folder_name_full) is False:
        os.makedirs(folder_name_full)
    file_name = 'poi-' + citycode + "-" + classfield + ".csv"
    file_path = folder_name_full + file_name
    df.to_csv(file_path, index=False, encoding='utf_8_sig')
    print('写入成功')
    return folder_name_full, file_name


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(grids, types, page, key):
    polygon = str(grids[0]) + "," + str(grids[1]) + "|" + str(grids[2]) + "," + str(grids[3])
    req_url = poi_pology_search_url + "?key=" + key + '&extensions=all' + '&polygon=' + polygon + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    print('请求url：', req_url)

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    try:
        data = s.get(req_url, timeout=5)
        return data.text
    except requests.exceptions.RequestException as e:
        data = s.get(req_url, timeout=5)
        return data.text
    return None


def get_drids(min_lng, max_lat, max_lng, min_lat, keyword, key, pology_split_distance, all_grids):
    grids_lib = city_grid.generate_grids(min_lng, max_lat, max_lng, min_lat, pology_split_distance)

    print('划分后的网格数：', len(grids_lib))
    print(grids_lib)

    # 3. 根据生成的网格爬取数据，验证网格大小是否合适，如果不合适的话，需要继续切分网格
    for grid in grids_lib:
        one_pology_data = getpoi_page(grid, keyword, 1, key)
        data = json.loads(one_pology_data)
        print(data)

        while int(data['count']) > 890:
            get_drids(grid[0], grid[1], grid[2], grid[3], keyword, key, pology_split_distance / 2, all_grids)


        all_grids.append(grid)
    return all_grids


def get_data(city, keyword, coord):
    # 1. 获取城市边界的最大、最小经纬度
    amap_key = buffer_keys[0]  # 总是获取队列中的第一个密钥
    max_lng, min_lng, max_lat, min_lat = area_boundary.getlnglat(city, amap_key)

    print('当前城市：', city, "max_lng, min_lng, max_lat, min_lat：", max_lng, min_lng, max_lat, min_lat)

    # 2. 生成网格切片格式：

    grids_lib = city_grid.generate_grids(min_lng, max_lat, max_lng, min_lat, pology_split_distance)

    print('划分后的网格数：', len(grids_lib))
    print(grids_lib)

    all_data = []
    begin_time = time.time()

    print('==========================正式开始爬取啦！！！！！！！！！！！================================')

    for grid in grids_lib:
        # grid格式：[112.23, 23.23, 112.24, 23.22]
        one_pology_data = getpois(grid, keyword)

        print('===================================当前矩形范围：', grid, '总共：',
              str(len(one_pology_data)) + "条数据.............................")

        all_data.extend(one_pology_data)

    end_time = time.time()
    print('全部：', str(len(grids_lib)) + '个矩形范围', '总的', str(len(all_data)), '条数据, 耗时：', str(end_time - begin_time),
          '正在写入CSV文件中')
    file_folder, file_name = write_to_csv(all_data, city, keyword, coord)
    # 写入shp
    #if file_folder is not None:
        #trans_point_to_shp(file_folder, file_name, 0, 1, pology_split_distance, keyword)


if __name__ == '__main__':
    # 初始化密钥队列
    init_queen()
    get_data(city_code, type, coord)
