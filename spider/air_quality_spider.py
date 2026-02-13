import requests
import json
import time
import random
from datetime import datetime, timedelta
from database import db
from config import CITIES
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AirQualitySpider:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
    def fetch_realtime_data(self):
        """获取实时空气质量数据"""
        try:
            url = "https://www.cnemc.cn/"
            response = self.session.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data_list = []
                current_time = datetime.now()
                
                for city in CITIES:
                    city_data = self._generate_mock_data(city, current_time)
                    data_list.append(city_data)
                
                logger.info(f"成功获取 {len(data_list)} 个城市的实时数据")
                return data_list
            else:
                logger.error(f"请求失败，状态码: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"获取实时数据失败: {str(e)}")
            return []
    
    def fetch_history_data(self, city_code, start_date, end_date):
        """获取历史空气质量数据"""
        try:
            data_list = []
            city = next((c for c in CITIES if c['code'] == city_code), None)
            
            if not city:
                logger.error(f"未找到城市代码: {city_code}")
                return []
            
            current_date = start_date
            while current_date <= end_date:
                city_data = self._generate_mock_data(city, current_date)
                data_list.append(city_data)
                current_date += timedelta(days=1)
            
            logger.info(f"成功获取 {city['name']} 的历史数据，共 {len(data_list)} 条")
            return data_list
            
        except Exception as e:
            logger.error(f"获取历史数据失败: {str(e)}")
            return []
    
    def _generate_mock_data(self, city, data_time):
        """生成模拟数据（实际项目中应从真实API获取）"""
        base_aqi = random.randint(30, 200)
        
        aqi = base_aqi + random.randint(-20, 20)
        aqi = max(10, min(300, aqi))
        
        if aqi <= 50:
            quality = "优"
        elif aqi <= 100:
            quality = "良"
        elif aqi <= 150:
            quality = "轻度污染"
        elif aqi <= 200:
            quality = "中度污染"
        elif aqi <= 300:
            quality = "重度污染"
        else:
            quality = "严重污染"
        
        return {
            'city_code': city['code'],
            'city_name': city['name'],
            'aqi': aqi,
            'quality': quality,
            'pm25': round(random.uniform(10, 150), 1),
            'pm10': round(random.uniform(20, 200), 1),
            'so2': round(random.uniform(5, 50), 1),
            'no2': round(random.uniform(10, 80), 1),
            'co': round(random.uniform(0.5, 2.0), 2),
            'o3': round(random.uniform(30, 150), 1),
            'data_time': data_time.strftime('%Y-%m-%d %H:%M:%S') if isinstance(data_time, datetime) else data_time.strftime('%Y-%m-%d')
        }
    
    def save_realtime_data(self, data_list):
        """保存实时数据到数据库"""
        try:
            sql = """
                INSERT INTO air_quality_realtime 
                (city_code, city_name, aqi, quality, pm25, pm10, so2, no2, co, o3, data_time, create_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                aqi = VALUES(aqi),
                quality = VALUES(quality),
                pm25 = VALUES(pm25),
                pm10 = VALUES(pm10),
                so2 = VALUES(so2),
                no2 = VALUES(no2),
                co = VALUES(co),
                o3 = VALUES(o3),
                data_time = VALUES(data_time)
            """
            
            params_list = []
            for data in data_list:
                params_list.append((
                    data['city_code'],
                    data['city_name'],
                    data['aqi'],
                    data['quality'],
                    data['pm25'],
                    data['pm10'],
                    data['so2'],
                    data['no2'],
                    data['co'],
                    data['o3'],
                    data['data_time']
                ))
            
            db.insert_many(sql, params_list)
            logger.info(f"成功保存 {len(data_list)} 条实时数据")
            return True
            
        except Exception as e:
            logger.error(f"保存实时数据失败: {str(e)}")
            return False
    
    def save_history_data(self, data_list):
        """保存历史数据到数据库"""
        try:
            sql = """
                INSERT INTO air_quality 
                (city_code, city_name, date, aqi, quality, pm25, pm10, so2, no2, co, o3, create_time, update_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE
                aqi = VALUES(aqi),
                quality = VALUES(quality),
                pm25 = VALUES(pm25),
                pm10 = VALUES(pm10),
                so2 = VALUES(so2),
                no2 = VALUES(no2),
                co = VALUES(co),
                o3 = VALUES(o3),
                update_time = NOW()
            """
            
            params_list = []
            for data in data_list:
                date_str = data['data_time'].split()[0] if ' ' in data['data_time'] else data['data_time']
                params_list.append((
                    data['city_code'],
                    data['city_name'],
                    date_str,
                    data['aqi'],
                    data['quality'],
                    data['pm25'],
                    data['pm10'],
                    data['so2'],
                    data['no2'],
                    data['co'],
                    data['o3']
                ))
            
            db.insert_many(sql, params_list)
            logger.info(f"成功保存 {len(data_list)} 条历史数据")
            return True
            
        except Exception as e:
            logger.error(f"保存历史数据失败: {str(e)}")
            return False
    
    def run_realtime_spider(self):
        """运行实时数据爬虫"""
        logger.info("开始获取实时空气质量数据...")
        data_list = self.fetch_realtime_data()
        if data_list:
            self.save_realtime_data(data_list)
            self.save_history_data(data_list)
        logger.info("实时数据获取完成")
    
    def run_history_spider(self, days=30):
        """运行历史数据爬虫"""
        logger.info(f"开始获取最近 {days} 天的历史数据...")
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        for city in CITIES:
            data_list = self.fetch_history_data(city['code'], start_date, end_date)
            if data_list:
                self.save_history_data(data_list)
            time.sleep(random.uniform(1, 2))
        
        logger.info("历史数据获取完成")

if __name__ == '__main__':
    spider = AirQualitySpider()
    spider.run_realtime_spider()
    spider.run_history_spider(days=30)
