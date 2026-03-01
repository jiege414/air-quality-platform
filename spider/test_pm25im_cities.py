"""
测试脚本：获取 PM25.im 网站上所有可用的城市
"""
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_all_cities():
    """获取 PM25.im 上所有城市"""
    url = "https://pm25.im/board/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取所有城市名称
        local_div = soup.find('div', class_='local')
        if local_div:
            city_links = local_div.find_all('a')
            cities = [link.get_text().strip() for link in city_links]
            
            logger.info(f"总共发现 {len(cities)} 个城市")
            
            # 按字母排序并打印
            cities_sorted = sorted(set(cities))
            
            print("\n=== PM25.im 网站上的所有城市 ===\n")
            for i, city in enumerate(cities_sorted, 1):
                print(f"{i:3d}. {city}")
            
            return cities_sorted
        else:
            logger.error("无法找到城市数据")
            return []
            
    except Exception as e:
        logger.error(f"获取数据失败: {str(e)}")
        return []

if __name__ == '__main__':
    cities = get_all_cities()
    
    # 保存到文件
    if cities:
        with open('pm25im_cities.txt', 'w', encoding='utf-8') as f:
            f.write(f"# PM25.im 网站上的所有城市 (共 {len(cities)} 个)\n\n")
            for city in cities:
                f.write(f"{city}\n")
        print(f"\n城市列表已保存到 pm25im_cities.txt")
