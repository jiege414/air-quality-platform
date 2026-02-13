import schedule
import time
import logging
from air_quality_spider import AirQualitySpider
from prediction import AQIPredictor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SpiderScheduler:
    def __init__(self):
        self.spider = AirQualitySpider()
        self.predictor = AQIPredictor()
    
    def job_fetch_realtime(self):
        """定时任务：获取实时数据"""
        logger.info("执行定时任务：获取实时空气质量数据")
        try:
            self.spider.run_realtime_spider()
        except Exception as e:
            logger.error(f"获取实时数据失败: {str(e)}")
    
    def job_fetch_history(self):
        """定时任务：获取历史数据"""
        logger.info("执行定时任务：获取历史空气质量数据")
        try:
            self.spider.run_history_spider(days=1)
        except Exception as e:
            logger.error(f"获取历史数据失败: {str(e)}")
    
    def job_prediction(self):
        """定时任务：运行预测"""
        logger.info("执行定时任务：运行AQI预测")
        try:
            self.predictor.run_prediction_for_all_cities(threshold=150)
        except Exception as e:
            logger.error(f"预测失败: {str(e)}")
    
    def run(self):
        """启动调度器"""
        logger.info("启动爬虫调度器...")
        
        schedule.every(2).hours.do(self.job_fetch_realtime)
        
        schedule.every().day.at("02:00").do(self.job_fetch_history)
        
        schedule.every().day.at("06:00").do(self.job_prediction)
        
        logger.info("调度器已启动，按Ctrl+C停止")
        
        self.job_fetch_realtime()
        self.job_fetch_history()
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == '__main__':
    scheduler = SpiderScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        logger.info("调度器已停止")
