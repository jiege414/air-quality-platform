package com.cugb.controller;

import com.cugb.common.Result;
import com.cugb.entity.AirQualityRealtime;
import com.cugb.service.AirQualityRealtimeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/air-quality-realtime")
@CrossOrigin(origins = "*")
public class AirQualityRealtimeController {
    
    @Autowired
    private AirQualityRealtimeService airQualityRealtimeService;
    
    @GetMapping("/ranking")
    public Result<Map<String, Object>> getRealtimeRanking(
            @RequestParam(defaultValue = "worst") String type,
            @RequestParam(defaultValue = "10") Integer limit) {
        Map<String, Object> ranking = airQualityRealtimeService.getRealtimeRanking(type, limit);
        return Result.success(ranking);
    }
    
    @GetMapping("/list")
    public Result<List<AirQualityRealtime>> getAllRealtimeData() {
        List<AirQualityRealtime> data = airQualityRealtimeService.getAllRealtimeData();
        return Result.success(data);
    }
}
