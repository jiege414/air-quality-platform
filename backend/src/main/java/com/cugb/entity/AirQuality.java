package com.cugb.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("air_quality")
public class AirQuality {
    
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String cityCode;
    
    private String cityName;
    
    private LocalDate date;
    
    private Integer aqi;
    
    private String quality;
    
    private Double pm25;
    
    private Double pm10;
    
    private Double so2;
    
    private Double no2;
    
    private Double co;
    
    private Double o3;
    
    private LocalDateTime createTime;
    
    private LocalDateTime updateTime;
}
