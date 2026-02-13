package com.cugb.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.cugb.entity.City;
import com.cugb.mapper.CityMapper;
import com.cugb.service.CityService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CityServiceImpl extends ServiceImpl<CityMapper, City> implements CityService {
    
    @Override
    public List<City> getAllCities() {
        return this.list();
    }
    
    @Override
    public City getCityByCode(String cityCode) {
        return this.lambdaQuery().eq(City::getCityCode, cityCode).one();
    }
}
