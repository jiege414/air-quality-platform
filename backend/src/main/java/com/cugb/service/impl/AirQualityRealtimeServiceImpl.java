package com.cugb.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.cugb.entity.AirQualityRealtime;
import com.cugb.mapper.AirQualityRealtimeMapper;
import com.cugb.service.AirQualityRealtimeService;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class AirQualityRealtimeServiceImpl extends ServiceImpl<AirQualityRealtimeMapper, AirQualityRealtime> implements AirQualityRealtimeService {
    
    @Override
    public Map<String, Object> getRealtimeRanking(String type, Integer limit) {
        Map<String, Object> result = new HashMap<>();
        List<AirQualityRealtime> list;
        
        // 默认限制为10，如果传入了limit则使用传入的值
        int queryLimit = (limit != null && limit > 0) ? limit : 10;
        
        if ("worst".equals(type)) {
            list = baseMapper.selectTop10ByAqiDesc(queryLimit);
        } else {
            list = baseMapper.selectTop10ByAqiAsc(queryLimit);
        }
        
        List<String> cityNames = new ArrayList<>();
        List<Integer> aqiValues = new ArrayList<>();
        List<String> qualityList = new ArrayList<>();
        
        for (AirQualityRealtime aq : list) {
            cityNames.add(aq.getCityName());
            aqiValues.add(aq.getAqi());
            qualityList.add(aq.getQuality());
        }
        
        result.put("cityNames", cityNames);
        result.put("aqiValues", aqiValues);
        result.put("qualityList", qualityList);
        
        return result;
    }
    
    @Override
    public List<AirQualityRealtime> getAllRealtimeData() {
        return this.list();
    }
    
    @Override
    public boolean saveRealtimeData(List<AirQualityRealtime> dataList) {
        return this.saveBatch(dataList);
    }
}
