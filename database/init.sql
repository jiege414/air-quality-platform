-- 创建数据库
CREATE DATABASE IF NOT EXISTS air_quality 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE air_quality;

-- 城市表
CREATE TABLE IF NOT EXISTS city (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    city_code VARCHAR(20) NOT NULL UNIQUE COMMENT '城市代码',
    city_name VARCHAR(50) NOT NULL COMMENT '城市名称',
    province VARCHAR(255) COMMENT '所属省份',
    longitude DECIMAL(10, 7) COMMENT '经度',
    latitude DECIMAL(10, 7) COMMENT '纬度',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_city_code (city_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='城市信息表';

-- 空气质量历史数据表
CREATE TABLE IF NOT EXISTS air_quality (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    city_code VARCHAR(20) NOT NULL COMMENT '城市代码',
    city_name VARCHAR(50) NOT NULL COMMENT '城市名称',
    date DATE NOT NULL COMMENT '日期',
    aqi INT COMMENT 'AQI指数',
    quality VARCHAR(20) COMMENT '空气质量等级',
    pm25 DECIMAL(8, 2) COMMENT 'PM2.5浓度',
    pm10 DECIMAL(8, 2) COMMENT 'PM10浓度',
    so2 DECIMAL(8, 2) COMMENT '二氧化硫浓度',
    no2 DECIMAL(8, 2) COMMENT '二氧化氮浓度',
    co DECIMAL(8, 2) COMMENT '一氧化碳浓度',
    o3 DECIMAL(8, 2) COMMENT '臭氧浓度',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_city_date (city_code, date),
    INDEX idx_date (date),
    INDEX idx_aqi (aqi)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='空气质量历史数据表';

-- 空气质量实时数据表
CREATE TABLE IF NOT EXISTS air_quality_realtime (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    city_code VARCHAR(20) NOT NULL COMMENT '城市代码',
    city_name VARCHAR(50) NOT NULL COMMENT '城市名称',
    aqi INT COMMENT 'AQI指数',
    quality VARCHAR(20) COMMENT '空气质量等级',
    pm25 DECIMAL(8, 2) COMMENT 'PM2.5浓度',
    pm10 DECIMAL(8, 2) COMMENT 'PM10浓度',
    so2 DECIMAL(8, 2) COMMENT '二氧化硫浓度',
    no2 DECIMAL(8, 2) COMMENT '二氧化氮浓度',
    co DECIMAL(8, 2) COMMENT '一氧化碳浓度',
    o3 DECIMAL(8, 2) COMMENT '臭氧浓度',
    data_time DATETIME COMMENT '数据时间',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_city_code (city_code),
    INDEX idx_aqi (aqi)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='空气质量实时数据表';

-- 预警记录表
CREATE TABLE IF NOT EXISTS warning_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    city_code VARCHAR(20) NOT NULL COMMENT '城市代码',
    city_name VARCHAR(50) NOT NULL COMMENT '城市名称',
    warning_date DATE COMMENT '预警日期',
    predicted_aqi INT COMMENT '预测AQI',
    warning_level VARCHAR(20) COMMENT '预警等级',
    warning_message VARCHAR(500) COMMENT '预警信息',
    is_handled TINYINT DEFAULT 0 COMMENT '是否已处理：0-未处理，1-已处理',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city_code (city_code),
    INDEX idx_warning_date (warning_date),
    INDEX idx_is_handled (is_handled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='空气质量预警记录表';

-- 插入主要城市数据
INSERT INTO city (city_code, city_name, province, longitude, latitude) VALUES
('110000', '北京', '北京', 116.407526, 39.90403),
('310000', '上海', '上海', 121.473701, 31.230416),
('440100', '广州', '广东', 113.264434, 23.129162),
('440300', '深圳', '广东', 114.057868, 22.543099),
('330100', '杭州', '浙江', 120.15507, 30.274084),
('320100', '南京', '江苏', 118.796877, 32.060255),
('420100', '武汉', '湖北', 114.305392, 30.593099),
('510100', '成都', '四川', 104.066541, 30.572269),
('500000', '重庆', '重庆', 106.551556, 29.563009),
('120000', '天津', '天津', 117.200983, 39.084158),
('610100', '西安', '陕西', 108.93977, 34.341574),
('410100', '郑州', '河南', 113.625368, 34.7466),
('430100', '长沙', '湖南', 112.938814, 28.228209),
('370100', '济南', '山东', 117.000923, 36.675807),
('130100', '石家庄', '河北', 114.51486, 38.042307),
('210100', '沈阳', '辽宁', 123.42944, 41.835441),
('230100', '哈尔滨', '黑龙江', 126.534967, 45.803775),
('220100', '长春', '吉林', 125.323544, 43.817071),
('320500', '苏州', '江苏', 120.585316, 31.298886),
('330200', '宁波', '浙江', 121.550357, 29.874557)
ON DUPLICATE KEY UPDATE city_name = VALUES(city_name), province = VALUES(province);
