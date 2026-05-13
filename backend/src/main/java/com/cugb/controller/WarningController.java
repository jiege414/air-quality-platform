package com.cugb.controller;

import com.cugb.common.Result;
import com.cugb.entity.WarningRecord;
import com.cugb.service.WarningService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/warning")
@CrossOrigin(origins = "*")
public class WarningController {
    
    @Autowired
    private WarningService warningService;
    
    @GetMapping("/unhandled")
    public Result<List<WarningRecord>> getUnhandledWarnings() {
        List<WarningRecord> warnings = warningService.getUnhandledWarnings();
        return Result.success(warnings);
    }
    
    @PostMapping("/predict")
    public Result<Map<String, Object>> predictAndGenerateWarning(@RequestBody Map<String, String> params) {
        String cityCode = params.get("cityCode");
        Map<String, Object> result = warningService.predictAndGenerateWarning(cityCode);
        return Result.success(result);
    }
    
    @PostMapping("/handle/{warningId}")
    public Result<Boolean> handleWarning(@PathVariable Long warningId) {
        boolean success = warningService.handleWarning(warningId);
        return Result.success(success);
    }
    
    @PostMapping("/batch-handle")
    public Result<Integer> batchHandleWarnings(@RequestBody Map<String, String> params) {
        String startDate = params.get("startDate");
        String endDate = params.get("endDate");
        int count = warningService.batchHandleWarnings(startDate, endDate);
        return Result.success(count);
    }
    
    @GetMapping("/today-count")
    public Result<Integer> getTodayWarningCount() {
        int count = warningService.getTodayWarningCount();
        return Result.success(count);
    }
}
