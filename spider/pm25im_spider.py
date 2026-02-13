"""
PM25.im 网站爬虫
从 https://pm25.im/board/ 获取空气质量数据
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
import logging
from datetime import datetime
from database import db

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PM25imSpider:
    """PM25.im 网站爬虫"""
    
    def __init__(self):
        self.url = "https://pm25.im/board/"
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        # 目标城市列表（20个主要城市）
        self.target_cities = [
            '北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都', 
            '重庆', '天津', '西安', '郑州', '长沙', '济南', '石家庄', 
            '沈阳', '哈尔滨', '长春', '苏州', '宁波'
        ]
        
        # 城市代码映射
        self.city_code_map = {
            '北京': '110000', '上海': '310000', '广州': '440100', '深圳': '440300',
            '杭州': '330100', '南京': '320100', '武汉': '420100', '成都': '510100',
            '重庆': '500000', '天津': '120000', '西安': '610100', '郑州': '410100',
            '长沙': '430100', '济南': '370100', '石家庄': '130100', '沈阳': '210100',
            '哈尔滨': '230100', '长春': '220100', '苏州': '320500', '宁波': '330200'
        }
    
    def fetch_data(self):
        """
        从 PM25.im 获取空气质量数据
        
        Returns:
            list: 城市空气质量数据列表
        """
        logger.info("正在从 PM25.im 获取数据...")
        
        try:
            response = self.session.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 解析数据
            return self._parse_board_data(soup)
            
        except Exception as e:
            logger.error(f"获取数据失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def _parse_board_data(self, soup):
        """
        解析排行榜数据
        网站结构：
        - .local: 城市名称列表
        - .pm25: PM2.5 数值列表
        - .pm10: PM10 数值列表
        - .usaqi: AQI 数值列表
        """
        results = []
        
        # 获取所有城市名称
        local_div = soup.find('div', class_='local')
        pm25_div = soup.find('div', class_='pm25')
        pm10_div = soup.find('div', class_='pm10')
        usaqi_div = soup.find('div', class_='usaqi')
        
        if not all([local_div, pm25_div, pm10_div, usaqi_div]):
            logger.error("无法找到数据容器")
            return []
        
        # 提取城市名称
        city_links = local_div.find_all('a')
        cities = [link.get_text().strip() for link in city_links]
        
        # 提取 PM2.5 数值
        pm25_spans = pm25_div.find_all('span', class_='pm25num')
        pm25_values = [span.get_text().strip() for span in pm25_spans]
        
        # 提取 PM10 数值
        pm10_spans = pm10_div.find_all('span', class_='pm10num')
        pm10_values = [span.get_text().strip() for span in pm10_spans]
        
        # 提取 AQI 数值和等级
        aqi_spans = usaqi_div.find_all('span', class_='aqi')
        aqi_data = []
        for span in aqi_spans:
            strong = span.find('strong')
            b = span.find('b')
            if strong and b:
                aqi_data.append({
                    'aqi': strong.get_text().strip(),
                    'level': b.get_text().strip()
                })
        
        logger.info(f"解析到 {len(cities)} 个城市的数据")
        
        # 只保留目标城市
        for i, city in enumerate(cities):
            if city in self.target_cities and i < len(pm25_values) and i < len(aqi_data):
                try:
                    pm25 = float(pm25_values[i]) if pm25_values[i] else 0
                    pm10 = float(pm10_values[i]) if i < len(pm10_values) and pm10_values[i] else 0
                    aqi = int(aqi_data[i]['aqi']) if aqi_data[i]['aqi'].isdigit() else 0
                    level = aqi_data[i]['level']
                    
                    # 直接使用网站的美标AQI，不再转换
                    # 美标AQI与国标的对应关系略有不同，但数值接近
                    result = {
                        'city_code': self.city_code_map.get(city, ''),
                        'city_name': city,
                        'aqi': aqi,  # 直接使用美标AQI
                        'pm25': pm25,
                        'pm10': pm10,
                        'quality': level,  # 使用网站提供的等级
                        'data_time': datetime.now()
                    }
                    results.append(result)
                    logger.info(f"解析到 {city}: PM2.5={pm25}, AQI={aqi}, 等级={level}")
                    
                except (ValueError, IndexError) as e:
                    logger.warning(f"解析 {city} 数据失败: {str(e)}")
                    continue
        
        return results
    
    def save_to_database(self, data_list):
        """保存数据到数据库"""
        if not data_list:
            logger.warning("没有数据需要保存")
            return 0
        
        success_count = 0
        
        try:
            # 清空实时数据表
            db.execute("DELETE FROM air_quality_realtime")
            
            # 插入新数据
            sql = """
                INSERT INTO air_quality_realtime 
                (city_code, city_name, aqi, quality, pm25, pm10, so2, no2, co, o3, data_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            for data in data_list:
                params = (
                    data['city_code'],
                    data['city_name'],
                    data['aqi'],
                    data['quality'],
                    data['pm25'],
                    data.get('pm10', 0),
                    data.get('so2', 0),
                    data.get('no2', 0),
                    data.get('co', 0),
                    data.get('o3', 0),
                    data['data_time']
                )
                
                try:
                    db.execute(sql, params)
                    success_count += 1
                except Exception as e:
                    logger.error(f"保存 {data['city_name']} 数据失败: {str(e)}")
            
            logger.info(f"成功保存 {success_count}/{len(data_list)} 条数据到数据库")
            return success_count
            
        except Exception as e:
            logger.error(f"数据库操作失败: {str(e)}")
            return 0
    
    def run(self):
        """运行爬虫"""
        logger.info("=" * 50)
        logger.info("开始运行 PM25.im 爬虫")
        logger.info("=" * 50)
        
        data_list = self.fetch_data()
        
        if data_list:
            saved_count = self.save_to_database(data_list)
            logger.info(f"爬虫运行完成，共保存 {saved_count} 条数据")
            return saved_count
        else:
            logger.error("未获取到任何数据")
            return 0


if __name__ == '__main__':
    spider = PM25imSpider()
    spider.run()
