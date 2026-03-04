package com.cugb.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.cugb.entity.AirQuality;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

public interface AirQualityService extends IService<AirQuality> {
    
    List<AirQuality> getHistoryData(String cityCode, LocalDate startDate, LocalDate endDate);
    
    /**
     * 获取城市历史数据，包含缺失日期标记
     * @param cityCode 城市代码
     * @param startDate 开始日期
     * @param endDate 结束日期
     * @return 包含日期范围所有天的数据，缺失的日期标记为 null
     */
    List<Map<String, Object>> getHistoryDataWithMissingDates(String cityCode, LocalDate startDate, LocalDate endDate);
    
    Map<String, Object> getCityRanking(String type, Integer limit);
    
    Map<String, Object> compareCities(List<String> cityCodes, LocalDate startDate, LocalDate endDate);
    
    boolean saveAirQualityData(List<AirQuality> dataList);
}
