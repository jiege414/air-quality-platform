package com.cugb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("warning_record")
public class WarningRecord {
    
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String cityCode;
    
    private String cityName;
    
    private LocalDate warningDate;
    
    private Integer predictedAqi;
    
    private String warningLevel;
    
    private String warningMessage;
    
    private Integer isHandled;
    
    private LocalDateTime createTime;
}
