package com.cugb.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.cugb.entity.AirQuality;
import com.cugb.mapper.AirQualityMapper;
import com.cugb.service.AirQualityService;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class AirQualityServiceImpl extends ServiceImpl<AirQualityMapper, AirQuality> implements AirQualityService {
    
    @Override
    public List<AirQuality> getHistoryData(String cityCode, LocalDate startDate, LocalDate endDate) {
        return baseMapper.selectByCityAndDateRange(cityCode, startDate, endDate);
    }
    
    @Override
    public Map<String, Object> getCityRanking(String type, Integer limit) {
        Map<String, Object> result = new HashMap<>();
        LocalDate today = LocalDate.now();
        List<AirQuality> list;
        
        if ("worst".equals(type)) {
            list = baseMapper.selectByDateOrderByAqiDesc(today);
        } else {
            list = baseMapper.selectByDateOrderByAqiAsc(today);
        }
        
        if (limit != null && limit > 0 && list.size() > limit) {
            list = list.subList(0, limit);
        }
        
        List<String> cityNames = new ArrayList<>();
        List<Integer> aqiValues = new ArrayList<>();
        List<String> qualityList = new ArrayList<>();
        
        for (AirQuality aq : list) {
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
    public Map<String, Object> compareCities(List<String> cityCodes, LocalDate startDate, LocalDate endDate) {
        Map<String, Object> result = new HashMap<>();
        List<String> dates = new ArrayList<>();
        Map<String, List<Integer>> cityAqiMap = new HashMap<>();
        
        for (String cityCode : cityCodes) {
            List<AirQuality> data = getHistoryData(cityCode, startDate, endDate);
            List<Integer> aqiList = new ArrayList<>();
            
            for (AirQuality aq : data) {
                String dateStr = aq.getDate().toString();
                if (!dates.contains(dateStr)) {
                    dates.add(dateStr);
                }
                aqiList.add(aq.getAqi());
            }
            
            cityAqiMap.put(cityCode, aqiList);
        }
        
        result.put("dates", dates);
        result.put("cityData", cityAqiMap);
        
        return result;
    }
    
    @Override
    public boolean saveAirQualityData(List<AirQuality> dataList) {
        return this.saveBatch(dataList);
    }
}
