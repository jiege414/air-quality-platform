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

# 城市列表（主要城市）
CITIES = [
    {'code': '110000', 'name': '北京', 'province': '北京市'},
    {'code': '310000', 'name': '上海', 'province': '上海市'},
    {'code': '440100', 'name': '广州', 'province': '广东省'},
    {'code': '440300', 'name': '深圳', 'province': '广东省'},
    {'code': '330100', 'name': '杭州', 'province': '浙江省'},
    {'code': '320100', 'name': '南京', 'province': '江苏省'},
    {'code': '420100', 'name': '武汉', 'province': '湖北省'},
    {'code': '510100', 'name': '成都', 'province': '四川省'},
    {'code': '500000', 'name': '重庆', 'province': '重庆市'},
    {'code': '120000', 'name': '天津', 'province': '天津市'},
    {'code': '610100', 'name': '西安', 'province': '陕西省'},
    {'code': '410100', 'name': '郑州', 'province': '河南省'},
    {'code': '430100', 'name': '长沙', 'province': '湖南省'},
    {'code': '370100', 'name': '济南', 'province': '山东省'},
    {'code': '130100', 'name': '石家庄', 'province': '河北省'},
    {'code': '210100', 'name': '沈阳', 'province': '辽宁省'},
    {'code': '230100', 'name': '哈尔滨', 'province': '黑龙江省'},
    {'code': '220100', 'name': '长春', 'province': '吉林省'},
    {'code': '320500', 'name': '苏州', 'province': '江苏省'},
    {'code': '330200', 'name': '宁波', 'province': '浙江省'},
]
