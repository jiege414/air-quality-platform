# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'air_quality',
    'charset': 'utf8mb4'
}

# Redis配置
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': None
}

# 爬虫配置
SPIDER_CONFIG = {
    'cnemc_url': 'https://www.cnemc.cn/',
    'timeout': 30,
    'retry_times': 3
}

# 城市列表（扩展到80个主要城市，覆盖所有省份）
CITIES = [
    # 直辖市
    {'code': '110000', 'name': '北京', 'province': '北京市'},
    {'code': '310000', 'name': '上海', 'province': '上海市'},
    {'code': '120000', 'name': '天津', 'province': '天津市'},
    {'code': '500000', 'name': '重庆', 'province': '重庆市'},
    # 河北省
    {'code': '130100', 'name': '石家庄', 'province': '河北省'},
    {'code': '130200', 'name': '唐山', 'province': '河北省'},
    {'code': '130600', 'name': '保定', 'province': '河北省'},
    {'code': '130400', 'name': '邯郸', 'province': '河北省'},
    # 山西省
    {'code': '140100', 'name': '太原', 'province': '山西省'},
    {'code': '140200', 'name': '大同', 'province': '山西省'},
    {'code': '140700', 'name': '晋中', 'province': '山西省'},
    {'code': '140800', 'name': '运城', 'province': '山西省'},
    # 内蒙古
    {'code': '150100', 'name': '呼和浩特', 'province': '内蒙古'},
    {'code': '150200', 'name': '包头', 'province': '内蒙古'},
    {'code': '150600', 'name': '鄂尔多斯', 'province': '内蒙古'},
    {'code': '150400', 'name': '赤峰', 'province': '内蒙古'},
    # 辽宁省
    {'code': '210100', 'name': '沈阳', 'province': '辽宁省'},
    {'code': '210200', 'name': '大连', 'province': '辽宁省'},
    {'code': '210300', 'name': '鞍山', 'province': '辽宁省'},
    {'code': '210400', 'name': '抚顺', 'province': '辽宁省'},
    # 吉林省
    {'code': '220100', 'name': '长春', 'province': '吉林省'},
    {'code': '220200', 'name': '吉林', 'province': '吉林省'},
    {'code': '220300', 'name': '四平', 'province': '吉林省'},
    # 黑龙江省
    {'code': '230100', 'name': '哈尔滨', 'province': '黑龙江省'},
    {'code': '230600', 'name': '大庆', 'province': '黑龙江省'},
    {'code': '230200', 'name': '齐齐哈尔', 'province': '黑龙江省'},
    {'code': '231000', 'name': '牡丹江', 'province': '黑龙江省'},
    # 江苏省
    {'code': '320100', 'name': '南京', 'province': '江苏省'},
    {'code': '320500', 'name': '苏州', 'province': '江苏省'},
    {'code': '320200', 'name': '无锡', 'province': '江苏省'},
    {'code': '320300', 'name': '徐州', 'province': '江苏省'},
    {'code': '320400', 'name': '常州', 'province': '江苏省'},
    {'code': '320600', 'name': '南通', 'province': '江苏省'},
    # 浙江省
    {'code': '330100', 'name': '杭州', 'province': '浙江省'},
    {'code': '330200', 'name': '宁波', 'province': '浙江省'},
    {'code': '330300', 'name': '温州', 'province': '浙江省'},
    {'code': '330400', 'name': '嘉兴', 'province': '浙江省'},
    {'code': '330600', 'name': '绍兴', 'province': '浙江省'},
    {'code': '331000', 'name': '台州', 'province': '浙江省'},
    # 安徽省
    {'code': '340100', 'name': '合肥', 'province': '安徽省'},
    {'code': '340200', 'name': '芜湖', 'province': '安徽省'},
    {'code': '340300', 'name': '蚌埠', 'province': '安徽省'},
    {'code': '340400', 'name': '淮南', 'province': '安徽省'},
    # 福建省
    {'code': '350100', 'name': '福州', 'province': '福建省'},
    {'code': '350200', 'name': '厦门', 'province': '福建省'},
    {'code': '350500', 'name': '泉州', 'province': '福建省'},
    {'code': '350600', 'name': '漳州', 'province': '福建省'},
    # 江西省
    {'code': '360100', 'name': '南昌', 'province': '江西省'},
    {'code': '360700', 'name': '赣州', 'province': '江西省'},
    {'code': '360400', 'name': '九江', 'province': '江西省'},
    {'code': '361100', 'name': '上饶', 'province': '江西省'},
    # 山东省
    {'code': '370100', 'name': '济南', 'province': '山东省'},
    {'code': '370200', 'name': '青岛', 'province': '山东省'},
    {'code': '370600', 'name': '烟台', 'province': '山东省'},
    {'code': '370700', 'name': '潍坊', 'province': '山东省'},
    {'code': '371300', 'name': '临沂', 'province': '山东省'},
    {'code': '370300', 'name': '淄博', 'province': '山东省'},
    # 河南省
    {'code': '410100', 'name': '郑州', 'province': '河南省'},
    {'code': '410300', 'name': '洛阳', 'province': '河南省'},
    {'code': '410700', 'name': '新乡', 'province': '河南省'},
    {'code': '411300', 'name': '南阳', 'province': '河南省'},
    {'code': '410200', 'name': '开封', 'province': '河南省'},
    # 湖北省
    {'code': '420100', 'name': '武汉', 'province': '湖北省'},
    {'code': '420500', 'name': '宜昌', 'province': '湖北省'},
    {'code': '420600', 'name': '襄阳', 'province': '湖北省'},
    {'code': '421000', 'name': '荆州', 'province': '湖北省'},
    # 湖南省
    {'code': '430100', 'name': '长沙', 'province': '湖南省'},
    {'code': '430200', 'name': '株洲', 'province': '湖南省'},
    {'code': '430300', 'name': '湘潭', 'province': '湖南省'},
    {'code': '430600', 'name': '岳阳', 'province': '湖南省'},
    {'code': '430400', 'name': '衡阳', 'province': '湖南省'},
    # 广东省
    {'code': '440100', 'name': '广州', 'province': '广东省'},
    {'code': '440300', 'name': '深圳', 'province': '广东省'},
    {'code': '440600', 'name': '佛山', 'province': '广东省'},
    {'code': '441900', 'name': '东莞', 'province': '广东省'},
    {'code': '440400', 'name': '珠海', 'province': '广东省'},
    {'code': '441300', 'name': '惠州', 'province': '广东省'},
    {'code': '442000', 'name': '中山', 'province': '广东省'},
    {'code': '440700', 'name': '江门', 'province': '广东省'},
    # 广西
    {'code': '450100', 'name': '南宁', 'province': '广西'},
    {'code': '450300', 'name': '桂林', 'province': '广西'},
    {'code': '450200', 'name': '柳州', 'province': '广西'},
    {'code': '450500', 'name': '北海', 'province': '广西'},
    # 海南省
    {'code': '460100', 'name': '海口', 'province': '海南省'},
    {'code': '460200', 'name': '三亚', 'province': '海南省'},
    # 四川省
    {'code': '510100', 'name': '成都', 'province': '四川省'},
    {'code': '510700', 'name': '绵阳', 'province': '四川省'},
    {'code': '510600', 'name': '德阳', 'province': '四川省'},
    {'code': '511300', 'name': '南充', 'province': '四川省'},
    {'code': '511500', 'name': '宜宾', 'province': '四川省'},
    # 贵州省
    {'code': '520100', 'name': '贵阳', 'province': '贵州省'},
    {'code': '520300', 'name': '遵义', 'province': '贵州省'},
    {'code': '520200', 'name': '六盘水', 'province': '贵州省'},
    # 云南省
    {'code': '530100', 'name': '昆明', 'province': '云南省'},
    {'code': '532900', 'name': '大理', 'province': '云南省'},
    {'code': '530300', 'name': '曲靖', 'province': '云南省'},
    {'code': '530400', 'name': '玉溪', 'province': '云南省'},
    # 西藏
    {'code': '540100', 'name': '拉萨', 'province': '西藏'},
    {'code': '540200', 'name': '日喀则', 'province': '西藏'},
    # 陕西省
    {'code': '610100', 'name': '西安', 'province': '陕西省'},
    {'code': '610400', 'name': '咸阳', 'province': '陕西省'},
    {'code': '610300', 'name': '宝鸡', 'province': '陕西省'},
    {'code': '610500', 'name': '渭南', 'province': '陕西省'},
    # 甘肃省
    {'code': '620100', 'name': '兰州', 'province': '甘肃省'},
    {'code': '620500', 'name': '天水', 'province': '甘肃省'},
    {'code': '620900', 'name': '酒泉', 'province': '甘肃省'},
    {'code': '620700', 'name': '张掖', 'province': '甘肃省'},
    # 青海省
    {'code': '630100', 'name': '西宁', 'province': '青海省'},
    {'code': '630200', 'name': '海东', 'province': '青海省'},
    # 宁夏
    {'code': '640100', 'name': '银川', 'province': '宁夏'},
    {'code': '640200', 'name': '石嘴山', 'province': '宁夏'},
    # 新疆
    {'code': '650100', 'name': '乌鲁木齐', 'province': '新疆'},
    {'code': '650200', 'name': '克拉玛依', 'province': '新疆'},
    {'code': '650400', 'name': '吐鲁番', 'province': '新疆'},
    {'code': '650500', 'name': '哈密', 'province': '新疆'},
]
