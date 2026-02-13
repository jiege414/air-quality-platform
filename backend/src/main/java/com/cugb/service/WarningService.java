package com.cugb.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.cugb.entity.WarningRecord;

import java.util.List;
import java.util.Map;

public interface WarningService extends IService<WarningRecord> {
    
    List<WarningRecord> getUnhandledWarnings();
    
    Map<String, Object> predictAndGenerateWarning(String cityCode);
    
    boolean handleWarning(Long warningId);
}
