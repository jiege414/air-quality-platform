-- 使用数据库
USE air_quality;

-- 插入主要城市数据
INSERT INTO city (city_code, city_name, province, longitude, latitude) VALUES
('110000', 'Beijing', 'Beijing', 116.407526, 39.90403),
('310000', 'Shanghai', 'Shanghai', 121.473701, 31.230416),
('440100', 'Guangzhou', 'Guangdong', 113.264434, 23.129162),
('440300', 'Shenzhen', 'Guangdong', 114.057868, 22.543099),
('330100', 'Hangzhou', 'Zhejiang', 120.15507, 30.274084),
('320100', 'Nanjing', 'Jiangsu', 118.796877, 32.060255),
('420100', 'Wuhan', 'Hubei', 114.305392, 30.593099),
('510100', 'Chengdu', 'Sichuan', 104.066541, 30.572269),
('500000', 'Chongqing', 'Chongqing', 106.551556, 29.563009),
('120000', 'Tianjin', 'Tianjin', 117.200983, 39.084158),
('610100', 'Xian', 'Shaanxi', 108.93977, 34.341574),
('410100', 'Zhengzhou', 'Henan', 113.625368, 34.7466),
('430100', 'Changsha', 'Hunan', 112.938814, 28.228209),
('370100', 'Jinan', 'Shandong', 117.000923, 36.675807),
('130100', 'Shijiazhuang', 'Hebei', 114.51486, 38.042307),
('210100', 'Shenyang', 'Liaoning', 123.42944, 41.835441),
('230100', 'Haerbin', 'Heilongjiang', 126.534967, 45.803775),
('220100', 'Changchun', 'Jilin', 125.323544, 43.817071),
('320500', 'Suzhou', 'Jiangsu', 120.585316, 31.298886),
('330200', 'Ningbo', 'Zhejiang', 121.550357, 29.874557);
