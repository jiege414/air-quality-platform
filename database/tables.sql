-- 使用数据库
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
