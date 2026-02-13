package com.cugb.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.cugb.entity.AirQualityRealtime;

import java.util.List;
import java.util.Map;

public interface AirQualityRealtimeService extends IService<AirQualityRealtime> {
    
    Map<String, Object> getRealtimeRanking(String type, Integer limit);
    
    List<AirQualityRealtime> getAllRealtimeData();
    
    boolean saveRealtimeData(List<AirQualityRealtime> dataList);
}
