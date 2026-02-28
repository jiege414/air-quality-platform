package com.cugb.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.cugb.entity.City;
import com.cugb.mapper.AirQualityRealtimeMapper;
import com.cugb.mapper.CityMapper;
import com.cugb.service.CityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class CityServiceImpl extends ServiceImpl<CityMapper, City> implements CityService {
    
    @Autowired
    private AirQualityRealtimeMapper airQualityRealtimeMapper;
    
    @Override
    public List<City> getAllCities() {
        // 先从city表查询
        List<City> cities = this.list();
        
        // 如果city表为空，从实时数据表获取城市列表
        if (cities == null || cities.isEmpty()) {
            List<String> cityNames = airQualityRealtimeMapper.selectAllCityNames();
            cities = new ArrayList<>();
            for (String cityName : cityNames) {
                City city = new City();
                city.setCityName(cityName);
                // 生成一个临时的cityCode（使用城市名称的hashCode）
                city.setCityCode(String.valueOf(Math.abs(cityName.hashCode())));
                cities.add(city);
            }
        }
        
        return cities;
    }
    
    @Override
    public City getCityByCode(String cityCode) {
        return this.lambdaQuery().eq(City::getCityCode, cityCode).one();
    }
}
