package com.cugb.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.cugb.common.Result;
import com.cugb.entity.City;
import com.cugb.service.CityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/city")
@CrossOrigin(origins = "*")
public class CityController {
    
    @Autowired
    private CityService cityService;
    
    @GetMapping("/list")
    public Result<List<City>> getAllCities() {
        List<City> cities = cityService.getAllCities();
        return Result.success(cities);
    }
    
    @GetMapping("/{cityCode}")
    public Result<City> getCityByCode(@PathVariable String cityCode) {
        City city = cityService.getCityByCode(cityCode);
        return Result.success(city);
    }
    
    /**
     * 分页查询城市列表，支持模糊搜索
     * @param page 页码，默认1
     * @param size 每页大小，默认20
     * @param keyword 搜索关键词（可选）
     * @return 分页结果
     */
    @GetMapping("/page")
    public Result<Map<String, Object>> getCityPage(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "20") Integer size,
            @RequestParam(required = false) String keyword) {
        
        IPage<City> cityPage = cityService.getCityPage(page, size, keyword);
        
        Map<String, Object> result = new HashMap<>();
        result.put("records", cityPage.getRecords());
        result.put("total", cityPage.getTotal());
        result.put("pages", cityPage.getPages());
        result.put("current", cityPage.getCurrent());
        result.put("size", cityPage.getSize());
        
        return Result.success(result);
    }
}
