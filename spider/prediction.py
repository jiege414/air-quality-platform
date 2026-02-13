import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from database import db
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AQIPredictor:
    def __init__(self):
        self.model = None
    
    def get_history_data(self, city_code, days=30):
        """获取历史AQI数据"""
        try:
            sql = """
                SELECT date, aqi 
                FROM air_quality 
                WHERE city_code = %s 
                AND date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
                ORDER BY date ASC
            """
            data = db.fetchall(sql, (city_code, days))
            
            if len(data) < 7:
                logger.warning(f"城市 {city_code} 的历史数据不足，仅有 {len(data)} 条")
                return None
            
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            return df
            
        except Exception as e:
            logger.error(f"获取历史数据失败: {str(e)}")
            return None
    
    def linear_regression_predict(self, city_code, days=1):
        """使用线性回归预测未来AQI"""
        try:
            df = self.get_history_data(city_code, days=14)
            if df is None:
                return None
            
            y = df['aqi'].values
            x = np.arange(len(y))
            
            n = len(x)
            sum_x = np.sum(x)
            sum_y = np.sum(y)
            sum_xy = np.sum(x * y)
            sum_x2 = np.sum(x * x)
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / n
            
            predictions = []
            for i in range(1, days + 1):
                pred = slope * (n + i - 1) + intercept
                predictions.append(max(10, int(pred)))
            
            return predictions
            
        except Exception as e:
            logger.error(f"线性回归预测失败: {str(e)}")
            return None
    
    def arima_predict(self, city_code, days=1):
        """使用ARIMA模型预测未来AQI"""
        try:
            df = self.get_history_data(city_code, days=30)
            if df is None or len(df) < 7:
                return None
            
            series = df['aqi']
            
            try:
                model = ARIMA(series, order=(2, 1, 2))
                fitted_model = model.fit()
                
                forecast = fitted_model.forecast(steps=days)
                predictions = [max(10, int(pred)) for pred in forecast]
                
                return predictions
                
            except Exception as e:
                logger.warning(f"ARIMA模型拟合失败，使用线性回归: {str(e)}")
                return self.linear_regression_predict(city_code, days)
            
        except Exception as e:
            logger.error(f"ARIMA预测失败: {str(e)}")
            return None
    
    def generate_warning(self, city_code, city_name, predicted_aqi):
        """生成预警记录"""
        try:
            if predicted_aqi >= 300:
                warning_level = "严重"
                warning_message = f"预测未来AQI将达到{predicted_aqi}，严重污染，请避免户外活动"
            elif predicted_aqi >= 200:
                warning_level = "重度"
                warning_message = f"预测未来AQI将达到{predicted_aqi}，重度污染，请减少户外活动"
            elif predicted_aqi >= 150:
                warning_level = "中度"
                warning_message = f"预测未来AQI将达到{predicted_aqi}，中度污染，敏感人群请注意防护"
            elif predicted_aqi >= 100:
                warning_level = "轻度"
                warning_message = f"预测未来AQI将达到{predicted_aqi}，轻度污染"
            else:
                return None
            
            sql = """
                INSERT INTO warning_record 
                (city_code, city_name, warning_date, predicted_aqi, warning_level, warning_message, is_handled, create_time)
                VALUES (%s, %s, DATE_ADD(CURDATE(), INTERVAL 1 DAY), %s, %s, %s, 0, NOW())
            """
            
            db.execute(sql, (city_code, city_name, predicted_aqi, warning_level, warning_message))
            logger.info(f"为城市 {city_name} 生成预警: {warning_level}污染，预测AQI={predicted_aqi}")
            
            return {
                'city_code': city_code,
                'city_name': city_name,
                'predicted_aqi': predicted_aqi,
                'warning_level': warning_level,
                'warning_message': warning_message
            }
            
        except Exception as e:
            logger.error(f"生成预警记录失败: {str(e)}")
            return None
    
    def run_prediction_for_all_cities(self, threshold=150):
        """为所有城市运行预测并生成预警"""
        from config import CITIES
        
        logger.info("开始为所有城市进行AQI预测...")
        warnings = []
        
        for city in CITIES:
            city_code = city['code']
            city_name = city['name']
            
            predictions = self.arima_predict(city_code, days=2)
            
            if predictions:
                for i, pred_aqi in enumerate(predictions):
                    if pred_aqi >= threshold:
                        warning = self.generate_warning(city_code, city_name, pred_aqi)
                        if warning:
                            warnings.append(warning)
                        break
                
                logger.info(f"城市 {city_name} 未来2天预测AQI: {predictions}")
            
            import time
            time.sleep(0.5)
        
        logger.info(f"预测完成，共生成 {len(warnings)} 条预警")
        return warnings

if __name__ == '__main__':
    predictor = AQIPredictor()
    predictor.run_prediction_for_all_cities(threshold=150)
