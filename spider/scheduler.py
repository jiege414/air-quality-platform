import schedule
import time
import logging
from air_quality_spider import AirQualitySpider
from pm25im_spider import PM25imSpider
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
        self.spider = AirQualitySpider()  # 原有模拟数据爬虫（备用）
        self.pm25im_spider = PM25imSpider()  # PM25.im 真实数据爬虫（主用）
        self.predictor = AQIPredictor()
    
    def job_fetch_realtime_pm25im(self):
        """定时任务：使用 PM25.im 获取实时数据"""
        logger.info("执行定时任务：使用 PM25.im 获取实时空气质量数据")
        try:
            result = self.pm25im_spider.run()
            if result > 0:
                logger.info(f"PM25.im 数据获取成功，共 {result} 条")
            else:
                logger.warning("PM25.im 数据获取失败，尝试使用备用爬虫")
                self.spider.run_realtime_spider()
        except Exception as e:
            logger.error(f"PM25.im 获取失败: {str(e)}，使用备用爬虫")
            try:
                self.spider.run_realtime_spider()
            except Exception as e2:
                logger.error(f"备用爬虫也失败: {str(e2)}")
    
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
        logger.info("=" * 60)
        logger.info("启动爬虫调度器")
        logger.info("主数据源: PM25.im (真实数据)")
        logger.info("备用数据源: 模拟数据生成")
        logger.info("=" * 60)
        
        # 每小时使用 PM25.im 获取实时数据
        schedule.every().hour.do(self.job_fetch_realtime_pm25im)
        
        # 每天 02:00 获取历史数据（使用模拟数据补充）
        schedule.every().day.at("02:00").do(self.job_fetch_history)
        
        # 每天 06:00 运行预测
        schedule.every().day.at("06:00").do(self.job_prediction)
        
        logger.info("定时任务配置:")
        logger.info("  - 每小时: 获取实时数据 (PM25.im)")
        logger.info("  - 每天 02:00: 获取历史数据")
        logger.info("  - 每天 06:00: 运行 ARIMA 预测")
        logger.info("=" * 60)
        logger.info("调度器已启动，按 Ctrl+C 停止")
        
        # 立即执行一次
        self.job_fetch_realtime_pm25im()
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
