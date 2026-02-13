package com.cugb.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.cugb.entity.AirQuality;
import com.cugb.entity.WarningRecord;
import com.cugb.mapper.WarningRecordMapper;
import com.cugb.service.AirQualityService;
import com.cugb.service.WarningService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class WarningServiceImpl extends ServiceImpl<WarningRecordMapper, WarningRecord> implements WarningService {
    
    @Autowired
    private AirQualityService airQualityService;
    
    @Value("${warning.threshold:150}")
    private Integer warningThreshold;
    
    @Override
    public List<WarningRecord> getUnhandledWarnings() {
        return baseMapper.selectUnhandledWarnings();
    }
    
    @Override
    public Map<String, Object> predictAndGenerateWarning(String cityCode) {
        Map<String, Object> result = new HashMap<>();
        
        LocalDate endDate = LocalDate.now();
        LocalDate startDate = endDate.minusDays(30);
        
        List<AirQuality> historyData = airQualityService.getHistoryData(cityCode, startDate, endDate);
        
        if (historyData.size() < 7) {
            result.put("success", false);
            result.put("message", "历史数据不足，无法进行预测");
            return result;
        }
        
        int predictedAqi = linearRegressionPredict(historyData);
        
        String warningLevel;
        String warningMessage;
        
        if (predictedAqi >= 300) {
            warningLevel = "严重";
            warningMessage = "预测未来AQI将达到严重污染水平，请避免户外活动";
        } else if (predictedAqi >= 200) {
            warningLevel = "重度";
            warningMessage = "预测未来AQI将达到重度污染水平，请减少户外活动";
        } else if (predictedAqi >= 150) {
            warningLevel = "中度";
            warningMessage = "预测未来AQI将达到中度污染水平，敏感人群请注意防护";
        } else if (predictedAqi >= 100) {
            warningLevel = "轻度";
            warningMessage = "预测未来AQI将达到轻度污染水平";
        } else {
            warningLevel = "优良";
            warningMessage = "预测未来空气质量良好";
        }
        
        if (predictedAqi >= warningThreshold) {
            WarningRecord record = new WarningRecord();
            record.setCityCode(cityCode);
            record.setCityName(historyData.get(historyData.size() - 1).getCityName());
            record.setWarningDate(LocalDate.now().plusDays(1));
            record.setPredictedAqi(predictedAqi);
            record.setWarningLevel(warningLevel);
            record.setWarningMessage(warningMessage);
            record.setIsHandled(0);
            
            this.save(record);
            
            result.put("success", true);
            result.put("warning", record);
        } else {
            result.put("success", true);
            result.put("message", "预测AQI为" + predictedAqi + "，无需预警");
        }
        
        result.put("predictedAqi", predictedAqi);
        return result;
    }
    
    private int linearRegressionPredict(List<AirQuality> historyData) {
        int n = Math.min(historyData.size(), 14);
        double sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
        
        for (int i = 0; i < n; i++) {
            double x = i;
            double y = historyData.get(historyData.size() - n + i).getAqi();
            sumX += x;
            sumY += y;
            sumXY += x * y;
            sumX2 += x * x;
        }
        
        double slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        double intercept = (sumY - slope * sumX) / n;
        
        double prediction = slope * n + intercept;
        
        return (int) Math.round(prediction);
    }
    
    @Override
    public boolean handleWarning(Long warningId) {
        WarningRecord record = this.getById(warningId);
        if (record != null) {
            record.setIsHandled(1);
            return this.updateById(record);
        }
        return false;
    }
}
