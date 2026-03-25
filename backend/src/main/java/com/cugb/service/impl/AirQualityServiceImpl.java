package com.cugb.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.cugb.entity.AirQuality;
import com.cugb.mapper.AirQualityMapper;
import com.cugb.service.AirQualityService;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class AirQualityServiceImpl extends ServiceImpl<AirQualityMapper, AirQuality> implements AirQualityService {
    
    @Override
    public List<AirQuality> getHistoryData(String cityCode, LocalDate startDate, LocalDate endDate) {
        return baseMapper.selectByCityAndDateRange(cityCode, startDate, endDate);
    }
    
    @Override
    public List<Map<String, Object>> getHistoryDataWithMissingDates(String cityCode, LocalDate startDate, LocalDate endDate) {
        // 1. 获取实际存在的数据
        List<AirQuality> existingData = baseMapper.selectByCityAndDateRange(cityCode, startDate, endDate);
        
        // 2. 将实际数据转换为 Map，key 为日期字符串
        Map<String, AirQuality> dataMap = existingData.stream()
            .collect(Collectors.toMap(
                aq -> aq.getDate().toString(),
                aq -> aq,
                (existing, replacement) -> existing
            ));
        
        // 3. 生成日期范围内的所有日期
        List<Map<String, Object>> result = new ArrayList<>();
        long daysBetween = ChronoUnit.DAYS.between(startDate, endDate);
        
        for (int i = 0; i <= daysBetween; i++) {
            LocalDate currentDate = startDate.plusDays(i);
            String dateStr = currentDate.toString();
            
            Map<String, Object> dayData = new HashMap<>();
            dayData.put("date", dateStr);
            
            AirQuality aq = dataMap.get(dateStr);
            if (aq != null) {
                // 有数据
                dayData.put("hasData", true);
                dayData.put("aqi", aq.getAqi());
                dayData.put("quality", aq.getQuality());
                dayData.put("pm25", aq.getPm25());
                dayData.put("pm10", aq.getPm10());
                dayData.put("so2", aq.getSo2());
                dayData.put("no2", aq.getNo2());
                dayData.put("co", aq.getCo());
                dayData.put("o3", aq.getO3());
                dayData.put("cityName", aq.getCityName());
                dayData.put("cityCode", aq.getCityCode());
            } else {
                // 无数据，标记为缺失
                dayData.put("hasData", false);
                dayData.put("aqi", null);
                dayData.put("quality", null);
                dayData.put("pm25", null);
                dayData.put("pm10", null);
                dayData.put("so2", null);
                dayData.put("no2", null);
                dayData.put("co", null);
                dayData.put("o3", null);
                dayData.put("cityName", null);
                dayData.put("cityCode", cityCode);
            }
            
            result.add(dayData);
        }
        
        return result;
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
        Map<String, List<Map<String, Object>>> cityDataMap = new HashMap<>();
        int totalMissingDays = 0;
        
        // 生成日期范围内的所有日期
        long daysBetween = ChronoUnit.DAYS.between(startDate, endDate);
        for (int i = 0; i <= daysBetween; i++) {
            dates.add(startDate.plusDays(i).toString());
        }
        
        for (String cityCode : cityCodes) {
            // 使用带缺失数据标记的方法获取数据
            List<Map<String, Object>> cityDataList = getHistoryDataWithMissingDates(cityCode, startDate, endDate);
            cityDataMap.put(cityCode, cityDataList);
            
            // 统计缺失数据天数
            for (Map<String, Object> dayData : cityDataList) {
                if (!(Boolean) dayData.get("hasData")) {
                    totalMissingDays++;
                }
            }
        }
        
        // 转换为前端需要的格式
        Map<String, List<Integer>> cityAqiMap = new HashMap<>();
        for (String cityCode : cityCodes) {
            List<Map<String, Object>> cityDataList = cityDataMap.get(cityCode);
            List<Integer> aqiList = cityDataList.stream()
                .map(dayData -> dayData.get("aqi") != null ? (Integer) dayData.get("aqi") : 0)
                .collect(Collectors.toList());
            cityAqiMap.put(cityCode, aqiList);
        }
        
        result.put("dates", dates);
        result.put("cityData", cityAqiMap);
        result.put("missingDataCount", totalMissingDays);
        result.put("cityDataDetails", cityDataMap);
        
        return result;
    }
    
    @Override
    public boolean saveAirQualityData(List<AirQuality> dataList) {
        return this.saveBatch(dataList);
    }
}
