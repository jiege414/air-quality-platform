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
        
        # 目标城市列表（扩展到主要城市，覆盖所有省份）
        self.target_cities = [
            # 直辖市
            '北京', '上海', '天津', '重庆',
            # 河北省
            '石家庄', '唐山', '保定', '邯郸',
            # 山西省
            '太原', '大同', '晋中', '运城',
            # 内蒙古
            '呼和浩特', '包头', '鄂尔多斯', '赤峰',
            # 辽宁省
            '沈阳', '大连', '鞍山', '抚顺',
            # 吉林省
            '长春', '吉林', '四平',
            # 黑龙江省
            '哈尔滨', '大庆', '齐齐哈尔', '牡丹江',
            # 江苏省
            '南京', '苏州', '无锡', '徐州', '常州', '南通',
            # 浙江省
            '杭州', '宁波', '温州', '嘉兴', '绍兴', '台州',
            # 安徽省
            '合肥', '芜湖', '蚌埠', '淮南',
            # 福建省
            '福州', '厦门', '泉州', '漳州',
            # 江西省
            '南昌', '赣州', '九江', '上饶',
            # 山东省
            '济南', '青岛', '烟台', '潍坊', '临沂', '淄博',
            # 河南省
            '郑州', '洛阳', '新乡', '南阳', '开封',
            # 湖北省
            '武汉', '宜昌', '襄阳', '荆州',
            # 湖南省
            '长沙', '株洲', '湘潭', '岳阳', '衡阳',
            # 广东省
            '广州', '深圳', '佛山', '东莞', '珠海', '惠州', '中山', '江门',
            # 广西
            '南宁', '桂林', '柳州', '北海',
            # 海南省
            '海口市', '三亚市',
            # 四川省
            '成都', '绵阳', '德阳', '南充', '宜宾',
            # 贵州省
            '贵阳', '遵义', '六盘水',
            # 云南省
            '昆明', '大理州', '曲靖', '玉溪',
            # 西藏
            '拉萨', '日喀则',
            # 陕西省
            '西安', '咸阳', '宝鸡', '渭南',
            # 甘肃省
            '兰州', '天水', '酒泉', '张掖',
            # 青海省
            '西宁', '海东',
            # 宁夏
            '银川', '石嘴山',
            # 新疆
            '乌鲁木齐', '克拉玛依', '吐鲁番', '哈密',
        ]
        
        # 城市代码映射
        self.city_code_map = {
            # 直辖市
            '北京': '110000', '上海': '310000', '天津': '120000', '重庆': '500000',
            # 河北省
            '石家庄': '130100', '唐山': '130200', '保定': '130600', '邯郸': '130400',
            # 山西省
            '太原': '140100', '大同': '140200', '晋中': '140700', '运城': '140800',
            # 内蒙古
            '呼和浩特': '150100', '包头': '150200', '鄂尔多斯': '150600', '赤峰': '150400',
            # 辽宁省
            '沈阳': '210100', '大连': '210200', '鞍山': '210300', '抚顺': '210400',
            # 吉林省
            '长春': '220100', '吉林': '220200', '四平': '220300',
            # 黑龙江省
            '哈尔滨': '230100', '大庆': '230600', '齐齐哈尔': '230200', '牡丹江': '231000',
            # 江苏省
            '南京': '320100', '苏州': '320500', '无锡': '320200', '徐州': '320300', '常州': '320400', '南通': '320600',
            # 浙江省
            '杭州': '330100', '宁波': '330200', '温州': '330300', '嘉兴': '330400', '绍兴': '330600', '台州': '331000',
            # 安徽省
            '合肥': '340100', '芜湖': '340200', '蚌埠': '340300', '淮南': '340400',
            # 福建省
            '福州': '350100', '厦门': '350200', '泉州': '350500', '漳州': '350600',
            # 江西省
            '南昌': '360100', '赣州': '360700', '九江': '360400', '上饶': '361100',
            # 山东省
            '济南': '370100', '青岛': '370200', '烟台': '370600', '潍坊': '370700', '临沂': '371300', '淄博': '370300',
            # 河南省
            '郑州': '410100', '洛阳': '410300', '新乡': '410700', '南阳': '411300', '开封': '410200',
            # 湖北省
            '武汉': '420100', '宜昌': '420500', '襄阳': '420600', '荆州': '421000',
            # 湖南省
            '长沙': '430100', '株洲': '430200', '湘潭': '430300', '岳阳': '430600', '衡阳': '430400',
            # 广东省
            '广州': '440100', '深圳': '440300', '佛山': '440600', '东莞': '441900', '珠海': '440400', '惠州': '441300', '中山': '442000', '江门': '440700',
            # 广西
            '南宁': '450100', '桂林': '450300', '柳州': '450200', '北海': '450500',
            # 海南省
            '海口市': '460100', '三亚市': '460200',
            # 四川省
            '成都': '510100', '绵阳': '510700', '德阳': '510600', '南充': '511300', '宜宾': '511500',
            # 贵州省
            '贵阳': '520100', '遵义': '520300', '六盘水': '520200',
            # 云南省
            '昆明': '530100', '大理州': '532900', '曲靖': '530300', '玉溪': '530400',
            # 西藏
            '拉萨': '540100', '日喀则': '540200',
            # 陕西省
            '西安': '610100', '咸阳': '610400', '宝鸡': '610300', '渭南': '610500',
            # 甘肃省
            '兰州': '620100', '天水': '620500', '酒泉': '620900', '张掖': '620700',
            # 青海省
            '西宁': '630100', '海东': '630200',
            # 宁夏
            '银川': '640100', '石嘴山': '640200',
            # 新疆
            '乌鲁木齐': '650100', '克拉玛依': '650200', '吐鲁番': '650400', '哈密': '650500',
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
