from flask import Flask, request, jsonify
from prediction import AQIPredictor
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
predictor = AQIPredictor()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        city_code = data.get('cityCode')
        days = data.get('days', 1)
        
        if not city_code:
            return jsonify({
                'success': False,
                'message': '缺少城市代码参数'
            }), 400
        
        predictions = predictor.arima_predict(city_code, days=days)
        
        if predictions is None:
            return jsonify({
                'success': False,
                'message': '预测失败，历史数据不足'
            }), 500
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'cityCode': city_code
        })
        
    except Exception as e:
        logger.error(f'预测API调用失败: {str(e)}')
        return jsonify({
            'success': False,
            'message': f'预测失败: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    logger.info('启动预测API服务，端口: 5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
