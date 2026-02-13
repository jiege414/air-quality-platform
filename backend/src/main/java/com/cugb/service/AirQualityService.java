package com.cugb.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.cugb.entity.AirQuality;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

public interface AirQualityService extends IService<AirQuality> {
    
    List<AirQuality> getHistoryData(String cityCode, LocalDate startDate, LocalDate endDate);
    
    Map<String, Object> getCityRanking(String type, Integer limit);
    
    Map<String, Object> compareCities(List<String> cityCodes, LocalDate startDate, LocalDate endDate);
    
    boolean saveAirQualityData(List<AirQuality> dataList);
}
