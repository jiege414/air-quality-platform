package com.cugb.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.cugb.entity.City;

import java.util.List;

public interface CityService extends IService<City> {
    
    List<City> getAllCities();
    
    City getCityByCode(String cityCode);
}
