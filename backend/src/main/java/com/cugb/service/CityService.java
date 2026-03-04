package com.cugb.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.cugb.entity.City;

import java.util.List;

public interface CityService extends IService<City> {
    
    List<City> getAllCities();
    
    City getCityByCode(String cityCode);
    
    /**
     * 分页查询城市列表，支持模糊搜索
     * @param page 页码
     * @param size 每页大小
     * @param keyword 搜索关键词（城市名或城市代码）
     * @return 分页结果
     */
    IPage<City> getCityPage(Integer page, Integer size, String keyword);
}
