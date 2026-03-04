package com.cugb.service.impl;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.cugb.entity.City;
import com.cugb.mapper.AirQualityMapper;
import com.cugb.mapper.CityMapper;
import com.cugb.service.CityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class CityServiceImpl extends ServiceImpl<CityMapper, City> implements CityService {
    
    @Autowired
    private AirQualityMapper airQualityMapper;
    
    @Override
    public List<City> getAllCities() {
        // 从air_quality表中获取城市列表
        List<Map<String, Object>> cityMaps = airQualityMapper.selectAllCities();
        return convertToCityList(cityMaps);
    }
    
    @Override
    public City getCityByCode(String cityCode) {
        return this.lambdaQuery().eq(City::getCityCode, cityCode).one();
    }
    
    @Override
    public IPage<City> getCityPage(Integer page, Integer size, String keyword) {
        // 从air_quality表中获取城市列表（支持搜索）
        List<Map<String, Object>> cityMaps;
        if (StringUtils.hasText(keyword)) {
            cityMaps = airQualityMapper.searchCities(keyword);
        } else {
            cityMaps = airQualityMapper.selectAllCities();
        }
        
        // 手动分页
        List<City> allCities = convertToCityList(cityMaps);
        int total = allCities.size();
        int start = (page - 1) * size;
        int end = Math.min(start + size, total);
        
        List<City> records = start < total ? allCities.subList(start, end) : new ArrayList<>();
        
        Page<City> resultPage = new Page<>(page, size);
        resultPage.setRecords(records);
        resultPage.setTotal(total);
        
        return resultPage;
    }
    
    private List<City> convertToCityList(List<Map<String, Object>> cityMaps) {
        List<City> cities = new ArrayList<>();
        for (Map<String, Object> map : cityMaps) {
            City city = new City();
            city.setCityCode((String) map.get("cityCode"));
            city.setCityName((String) map.get("cityName"));
            cities.add(city);
        }
        return cities;
    }
}
