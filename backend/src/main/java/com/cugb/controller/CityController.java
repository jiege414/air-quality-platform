package com.cugb.controller;

import com.cugb.common.Result;
import com.cugb.entity.City;
import com.cugb.service.CityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

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
}
