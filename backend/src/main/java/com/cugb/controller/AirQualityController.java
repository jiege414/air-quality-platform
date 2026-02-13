package com.cugb.controller;

import com.cugb.common.Result;
import com.cugb.entity.AirQuality;
import com.cugb.service.AirQualityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/air-quality")
@CrossOrigin(origins = "*")
public class AirQualityController {
    
    @Autowired
    private AirQualityService airQualityService;
    
    @GetMapping("/history")
    public Result<List<AirQuality>> getHistoryData(
            @RequestParam String cityCode,
            @RequestParam @DateTimeFormat(pattern = "yyyy-MM-dd") LocalDate startDate,
            @RequestParam @DateTimeFormat(pattern = "yyyy-MM-dd") LocalDate endDate) {
        List<AirQuality> data = airQualityService.getHistoryData(cityCode, startDate, endDate);
        return Result.success(data);
    }
    
    @GetMapping("/ranking")
    public Result<Map<String, Object>> getCityRanking(
            @RequestParam(defaultValue = "worst") String type,
            @RequestParam(defaultValue = "10") Integer limit) {
        Map<String, Object> ranking = airQualityService.getCityRanking(type, limit);
        return Result.success(ranking);
    }
    
    @PostMapping("/compare")
    public Result<Map<String, Object>> compareCities(
            @RequestBody Map<String, Object> params) {
        @SuppressWarnings("unchecked")
        List<String> cityCodes = (List<String>) params.get("cityCodes");
        String startDateStr = (String) params.get("startDate");
        String endDateStr = (String) params.get("endDate");
        
        LocalDate startDate = LocalDate.parse(startDateStr);
        LocalDate endDate = LocalDate.parse(endDateStr);
        
        Map<String, Object> result = airQualityService.compareCities(cityCodes, startDate, endDate);
        return Result.success(result);
    }
}
